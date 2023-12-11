#include "bsp/board.h"
#include "tusb.h"
#include "hid.h"

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
    // Poll every 10ms
    const uint32_t interval_ms = 10;
    static uint32_t start_ms = 0;

    if ( board_millis() - start_ms < interval_ms) return; // not enough time
    start_ms += interval_ms;

    uint32_t const btn = board_button_read();

    // Remote wakeup
    if ( tud_suspended() && btn )
    {
        // Wake up host if we are in suspend mode
        // and REMOTE_WAKEUP feature is enabled by host
        tud_remote_wakeup();
    }

    /*------------- Keyboard -------------*/
    if ( tud_hid_n_ready(ITF_KEYBOARD) )
    {
        // use to avoid send multiple consecutive zero report for keyboard
        static bool has_key = false;

        if ( btn )
        {
            uint8_t keycode[6] = { 0 };
            keycode[0] = HID_KEY_A;

            tud_hid_n_keyboard_report(ITF_KEYBOARD, 0, 0, keycode);

            has_key = true;
        }else
        {
            // send empty key report if previously has key pressed
            if (has_key) tud_hid_n_keyboard_report(ITF_KEYBOARD, 0, 0, NULL);
            has_key = false;
        }
    }

    /*------------- Mouse -------------*/
    if ( tud_hid_n_ready(ITF_MOUSE) )
    {
        if ( btn )
        {
            int8_t const delta = 5;

            // no button, right + down, no scroll pan
            tud_hid_n_mouse_report(ITF_MOUSE, 0, 0x00, delta, delta, 0, 0);
        }
    }
}
