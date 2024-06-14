#include <string.h>
#include <pthread.h>
#include "rt_receiver.h"
#include "rt_ring_buffer.h"

static struct {
    int buffer_size;
    rt_stream_packet_t packet;
    ring_buffer_t *buffer;
    pthread_mutex_t lock;
} internal = {0};

void rt_rcv_init(int buffer_size) {
    internal.buffer_size = buffer_size;
    internal.buffer = create_ring_buffer(buffer_size);
    pthread_mutex_init(&internal.lock, NULL);
}

void rt_rcv_add_packet(rt_stream_packet_t *packet) {
    pthread_mutex_lock(&internal.lock);
    memcpy(&internal.packet, packet, sizeof(rt_stream_packet_t));
    pthread_mutex_unlock(&internal.lock);
}

/* Audio device requests one frame */
void rt_rcv_get_samples(int16_t *samples, int n_frames, int n_channels) {
    int16_t *dst = samples;
    for (int i = 0; i < n_frames; i++) {
        for (int c = 0; c < n_channels; c++) {
            *dst++ = internal.packet.samples[i];
        }
    }
}