#include "bsp/board.h"
#include "tusb.h"
#include "hid.h"
#include "app.h"

enum {
    ITF_KEYBOARD = 0,
    ITF_MOUSE = 1 // TODO
};

// Invoked when received GET_REPORT control request
// Application must fill buffer report's content and return its length.
// Return zero will cause the stack to STALL request
uint16_t tud_hid_get_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{
    // TODO not Implemented
    (void) itf;
    (void) report_id;
    (void) report_type;
    (void) buffer;
    (void) reqlen;

    return 0;
}

// Invoked when received SET_REPORT control request or
// received data on OUT endpoint ( Report ID = 0, Type = 0 )
void tud_hid_set_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize)
{
    // TODO set LED based on CAPLOCK, NUMLOCK etc...
    (void) itf;
    (void) report_id;
    (void) report_type;
    (void) buffer;
    (void) bufsize;
}

void hid_process()
{
    hid_keyboard_report_t report;
    if (tud_hid_n_ready(0)) {
        if (app_read_hid_report(&report)) {
            tud_hid_n_report(0, 0, &report, sizeof(report));
        }
    }
}
