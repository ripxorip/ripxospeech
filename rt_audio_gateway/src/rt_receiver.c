#include <string.h>
#include "rt_receiver.h"

static struct {
    rt_stream_packet_t packet;
} internal = {0};

void rt_rcv_init() {
    (void)internal;
}

void rt_rcv_add_packet(rt_stream_packet_t *packet) {
    memcpy(&internal.packet, packet, sizeof(rt_stream_packet_t));
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