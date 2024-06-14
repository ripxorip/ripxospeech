#ifndef RT_RECEIVER
#define RT_RECEIVER

#include <stdint.h>
#include "stream_packet.h"

void rt_rcv_init(int buffer_size);
void rt_rcv_add_packet(rt_stream_packet_t *packet);
void rt_rcv_get_samples(int16_t *samples, int n_frames, int n_channels);

#endif /* RT_RECEIVER */
