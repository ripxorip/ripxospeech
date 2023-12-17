#include "app.h"
#include "cdc.h"
#include "pico/bootrom.h"
#include "hid.h"
#include "tusb.h"

#define FIFO_SIZE 2048

typedef struct {
    hid_keyboard_report_t buffer[FIFO_SIZE];
    int front;
    int rear;
} hid_report_fifo_t;

hid_report_fifo_t fifo_inst = {0};

void fifo_init() {
    fifo_inst.front = 0;
    fifo_inst.rear = 0;
}

int fifo_is_empty() {
    return fifo_inst.front == fifo_inst.rear;
}

int fifo_is_full() {
    return (fifo_inst.rear + 1) % FIFO_SIZE == fifo_inst.front;
}

bool push_hid_report_to_fifo(hid_keyboard_report_t *report) {
    bool result;
    if (!fifo_is_full(&fifo_inst)) {
        fifo_inst.buffer[fifo_inst.rear] = *report;
        fifo_inst.rear = (fifo_inst.rear + 1) % FIFO_SIZE;
        result = true;
    } else {
        result = false;
    }
    return result;
}

bool pull_hid_report_from_fifo(hid_keyboard_report_t *report) {
    if (!fifo_is_empty(&fifo_inst)) {
        *report = fifo_inst.buffer[fifo_inst.front];
        fifo_inst.front = (fifo_inst.front + 1) % FIFO_SIZE;
        return true;
    } else {
        return false;
    }
}

void app_init() {
    fifo_init();
}

bool app_read_hid_report(hid_keyboard_report_t *report) {
    return pull_hid_report_from_fifo(report);
}

void app_handle_incoming_bytes(uint8_t *bytes, uint8_t len)
{
    /* Handle special commands */
    if (len == 1)
    {
        if (bytes[0] == 0x55)
        {
            cdc_debug_print("Test command!\n");
        }
        if (bytes[0] == 0x66)
        {
            //  reset the device so I can upload new firmware
            reset_usb_boot(0, 0);
        }
    }
    /* TODO Handle HID commands (debug printing for now) */
    else {
        if (len >= sizeof(hid_keyboard_report_t))
        {
#if 0 // Enable for debug printing
            for (int i = 0; i < len; i++)
            {
                tud_cdc_write(&bytes[i], 1u);
            }
            tud_cdc_write_flush();
#endif
            hid_keyboard_report_t report;
            memcpy(&report, bytes, sizeof(hid_keyboard_report_t));
            push_hid_report_to_fifo(&report);
        }
    }
}