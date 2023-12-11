#include <pico/stdlib.h>

#include "usb.h"
#include "hid.h"
#include "cdc.h"
#include "frame.h"
#include "pc_protocol.h"
#include "controller.h"
#include "keyboard.h"
#include <stdio.h>


int main(void)
{
    stdio_init_all();
    controller_init();
    pc_protocol_init();
    usb_init();
    while (1)
    {
        absolute_time_t before = get_absolute_time();

        if (controller_get_enabled())
        {
            /* TODO Run keyboard logic after the algorithm has been
             * implemented here */
        }

        /* Check for PC UART data */
        cdc_process();
        /* Proceed with HID & housekeeping */
        hid_process(); // FIXME these functions will be called by the controller task instead
                       // Could cause trouble since it is calling from another thread? Probably not..
        usb_housekeeping();

        absolute_time_t after = get_absolute_time();
        printf("%lld\n", absolute_time_diff_us(before, after));
    }
    return 0;
}
