#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "rt_receiver.h"
#include "rt_ring_buffer.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define ASSERT(expr, msg) \
    ((expr) \
    ? (void)0 \
    : (fprintf(stderr, "❌  %s:%d: Assertion failed: %s. %s\n", __FILE__, __LINE__, #expr, msg), exit(EXIT_FAILURE)))

static struct {
    int num_frames;
    int16_t *test_sine;
} internal = {0};

void generate_sine_s16(int16_t *samples, int num_samples) {
    for (int i = 0; i < num_samples; i++) {
        samples[i] = (uint16_t)(32767.0 * sin(2.0 * M_PI * i / num_samples));
    }
}

void create_packet(rt_stream_packet_t *packet, int seq) {
    packet->n_samples = RT_STREAM_PACKET_FRAME_SIZE;
    packet->seq = seq;
    packet->timestamp = 0;
    for (int i = 0; i < RT_STREAM_PACKET_FRAME_SIZE; i++) {
        packet->samples[i] = internal.test_sine[seq*RT_STREAM_PACKET_FRAME_SIZE + i];
    }
}

void init() {
    internal.num_frames = 2048;
    internal.test_sine = malloc(internal.num_frames*RT_STREAM_PACKET_FRAME_SIZE*sizeof(int16_t));
    generate_sine_s16(internal.test_sine, internal.num_frames*RT_STREAM_PACKET_FRAME_SIZE);
}

void test_ring_buffer()
{
    printf("::Test ring buffer::\n");
    ring_buffer_t *ring_buffer = create_ring_buffer(6);
    rt_stream_packet_t packet;
    packet.seq = 1;
    ASSERT(ring_buffer_push(ring_buffer, &packet) == 0, "ring_buffer_push() failed");
    ASSERT(ring_buffer_pop(ring_buffer, &packet) == 0, "ring_buffer_pop() failed");
    ASSERT(packet.seq == 1, "ring_buffer_push() failed");

    packet.seq = 1;
    ASSERT(ring_buffer_push(ring_buffer, &packet) == 0, "ring_buffer_push() failed");
    packet.seq = 2;
    ASSERT(ring_buffer_push(ring_buffer, &packet) == 0, "ring_buffer_push() failed");
    packet.seq = 3;
    ASSERT(ring_buffer_push(ring_buffer, &packet) == 0, "ring_buffer_push() failed");

    ASSERT(ring_buffer_pop(ring_buffer, &packet) == 0, "ring_buffer_pop() failed");
    ASSERT(packet.seq == 1, "ring_buffer_push() failed");

    ASSERT(ring_buffer_pop(ring_buffer, &packet) == 0, "ring_buffer_pop() failed");
    ASSERT(packet.seq == 2, "ring_buffer_push() failed");

    ASSERT(ring_buffer_pop(ring_buffer, &packet) == 0, "ring_buffer_pop() failed");
    ASSERT(packet.seq == 3, "ring_buffer_push() failed");

    ASSERT(ring_buffer_pop(ring_buffer, &packet) == -1, "ring_buffer_pop() failed");


    printf(":: ✅ Ring buffer test passed::\n\n");
}

void test_when_in_sync() {
    printf("::Test when in sync::\n");
    const int num_frames = 128;
    const int buffer_size = 3;
    rt_rcv_init(buffer_size);
    rt_stream_packet_t packet;

    // Allocate memory for the a facke audio device
    int16_t *audio_device_data = malloc(RT_STREAM_PACKET_FRAME_SIZE*sizeof(int16_t));

    for (int i = 0; i < num_frames; i++) {
        create_packet(&packet, i);
        rt_rcv_add_packet(&packet);
        if (i >= 1)
        {
            rt_rcv_get_samples(audio_device_data, RT_STREAM_PACKET_FRAME_SIZE, 1);
            ASSERT(memcmp(audio_device_data, internal.test_sine + (RT_STREAM_PACKET_FRAME_SIZE * (i-1)), RT_STREAM_PACKET_FRAME_SIZE * sizeof(int16_t)) == 0, "rt_rcv_get_samples() returned incorrect data");
        }
    }
    printf(":: ✅ Test when in sync passed::\n\n");
}

int main() {
    init();
    test_ring_buffer();
    test_when_in_sync();
    return 0;
}