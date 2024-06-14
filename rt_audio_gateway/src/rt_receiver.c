#include <string.h>
#include <pthread.h>
#include "rt_receiver.h"
#include "rt_ring_buffer.h"
#include <stdio.h>

#define ENABLE_LOGGING 1 // Change to 0 to disable logging

#define LOG(msg) do { if (ENABLE_LOGGING) printf("%s\n", msg); } while (0)

static struct {
    int buffer_size;
    ring_buffer_t *buffer;
    pthread_mutex_t lock;
} internal = {0};

void rt_rcv_init(int buffer_size) {
    internal.buffer_size = buffer_size;
    internal.buffer = create_ring_buffer(buffer_size);
    pthread_mutex_init(&internal.lock, NULL);
}

void rt_rcv_add_packet(rt_stream_packet_t *packet) {
    int res;

    pthread_mutex_lock(&internal.lock);
    res = ring_buffer_push(internal.buffer, packet);
    pthread_mutex_unlock(&internal.lock);

    if (res == -1) {
        /* Overrun */
        ring_buffer_clear(internal.buffer);
        LOG("Buffer overrun");
    }
}

/* Audio device requests one frame */
void rt_rcv_get_samples(int16_t *samples, int n_frames, int n_channels) {
    int16_t *dst = samples;
    /* Packet to send */
    rt_stream_packet_t packet;

    int res;

    pthread_mutex_lock(&internal.lock);
    res = ring_buffer_pop(internal.buffer, &packet);
    pthread_mutex_unlock(&internal.lock);

    if (res == -1) {
        /* Underrun */
        LOG("Buffer underrun");
        memset(samples, 0, n_frames * n_channels * sizeof(int16_t));
        return;
    }

    for (int i = 0; i < n_frames; i++) {
        for (int c = 0; c < n_channels; c++) {
            *dst++ = packet.samples[i];
        }
    }
}