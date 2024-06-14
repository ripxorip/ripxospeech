#include "rt_ring_buffer.h"

ring_buffer_t* create_ring_buffer(int size) {
    ring_buffer_t *ring_buffer = malloc(sizeof(ring_buffer_t));
    ring_buffer->buffer = malloc(sizeof(rt_stream_packet_t) * size);
    ring_buffer->head = 0;
    ring_buffer->tail = 0;
    ring_buffer->size = size;
    return ring_buffer;
}

void delete_ring_buffer(ring_buffer_t *ring_buffer) {
    free(ring_buffer->buffer);
    free(ring_buffer);
}

int ring_buffer_push(ring_buffer_t *ring_buffer, rt_stream_packet_t *data) {
    int next_head = (ring_buffer->head + 1) % ring_buffer->size;
    if (next_head == ring_buffer->tail) {
        // Buffer is full
        return -1;
    }
    ring_buffer->buffer[ring_buffer->head] = *data;
    ring_buffer->head = next_head;
    return 0;
}

int ring_buffer_pop(ring_buffer_t *ring_buffer, rt_stream_packet_t *data) {
    if (ring_buffer->head == ring_buffer->tail) {
        // Buffer is empty
        return -1;
    }
    *data = ring_buffer->buffer[ring_buffer->tail];
    ring_buffer->tail = (ring_buffer->tail + 1) % ring_buffer->size;
    return 0;
}

void ring_buffer_clear(ring_buffer_t *ring_buffer) {
    ring_buffer->head = ring_buffer->tail = 0;
    /* Zero out the buffer */
    memset(ring_buffer->buffer, 0, sizeof(rt_stream_packet_t) * ring_buffer->size);
}