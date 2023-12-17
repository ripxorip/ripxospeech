#ifndef APP
#define APP

#include <stdint.h>
#include <stdbool.h>
#include "tusb.h"

void app_handle_incoming_bytes(uint8_t *bytes, uint8_t len);
bool app_read_hid_report(hid_keyboard_report_t *report);
void app_init();

#endif /* APP */
