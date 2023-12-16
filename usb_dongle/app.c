#include "app.h"
#include "cdc.h"
#include "pico/bootrom.h"
#include "hid.h"

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
    /* TODO Handle HID commands */
    else {
        cdc_debug_print("Got a keyboard HID!\n");
    }
}