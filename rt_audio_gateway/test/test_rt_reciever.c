#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "rt_receiver.h"

#define ASSERT(expr, msg) \
    ((expr) \
    ? (void)0 \
    : (fprintf(stderr, "%s:%d: Assertion failed: %s. %s\n", __FILE__, __LINE__, #expr, msg), exit(EXIT_FAILURE)))

int main() {
    rt_rcv_init();
    ASSERT(1, "rt_rcv_init() failed");
    return 0;
}