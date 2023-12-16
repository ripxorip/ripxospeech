#include "app.h"
#include "cdc.h"
#include "pico/bootrom.h"
#include "hid.h"
#include "tusb.h"

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
            tud_hid_n_report(0, 0, &report, sizeof(hid_keyboard_report_t));
        }
    }
}