#ifndef RING_BUFFER
#define RING_BUFFER

#include <stdlib.h>
#include <string.h>
#include "stream_packet.h"

typedef struct {
    rt_stream_packet_t *buffer;
    int head;
    int tail;
    int size;
} ring_buffer_t;

ring_buffer_t* create_ring_buffer(int size);
void delete_ring_buffer(ring_buffer_t *ring_buffer);

int ring_buffer_push(ring_buffer_t *ring_buffer, rt_stream_packet_t *data);
int ring_buffer_pop(ring_buffer_t *ring_buffer, rt_stream_packet_t *data);
void ring_buffer_clear(ring_buffer_t *ring_buffer);

#endif /* RING_BUFFER */
