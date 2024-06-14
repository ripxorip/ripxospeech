#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "rt_receiver.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define ASSERT(expr, msg) \
    ((expr) \
    ? (void)0 \
    : (fprintf(stderr, "❌  %s:%d: Assertion failed: %s. %s\n", __FILE__, __LINE__, #expr, msg), exit(EXIT_FAILURE)))

void generate_sine_s16(int16_t *samples, int num_samples) {
    for (int i = 0; i < num_samples; i++) {
        samples[i] = (uint16_t)(32767.0 * sin(2.0 * M_PI * i / num_samples));
    }
}

void test_when_in_sync() {
    printf("::Test when in sync::\n");
    const int num_frames = 128;
    const int buffer_size = 0;
    rt_rcv_init(buffer_size);

    // Allocate memory for a sine consisting of 128 frames
    int16_t *test_sine = malloc(num_frames*RT_STREAM_PACKET_FRAME_SIZE*sizeof(int16_t));
    generate_sine_s16(test_sine, num_frames*RT_STREAM_PACKET_FRAME_SIZE);

    // Allocate memory for the a facke audio device
    int16_t *audio_device_data = malloc(RT_STREAM_PACKET_FRAME_SIZE*sizeof(int16_t));

    for (int i = 0; i < num_frames; i++) {
        rt_stream_packet_t packet = {
            .n_samples = RT_STREAM_PACKET_FRAME_SIZE,
            .seq = i,
            .timestamp = 0,
        };
        for (int j = 0; j < RT_STREAM_PACKET_FRAME_SIZE; j++) {
            packet.samples[j] = test_sine[i*RT_STREAM_PACKET_FRAME_SIZE + j];
        }

        rt_rcv_add_packet(&packet);
        rt_rcv_get_samples(audio_device_data, RT_STREAM_PACKET_FRAME_SIZE, 1);

        /* Verify that the audio_device_data data is the same as was previously added */
        ASSERT(memcmp(audio_device_data, test_sine + (RT_STREAM_PACKET_FRAME_SIZE * i), RT_STREAM_PACKET_FRAME_SIZE * sizeof(int16_t)) == 0, "rt_rcv_get_samples() returned incorrect data");
    }
    printf(":: ✅ Test when in sync passed::\n");
    free(test_sine);
}

int main() {
    test_when_in_sync();
    return 0;
}