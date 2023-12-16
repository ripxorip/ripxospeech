#include <pico/stdlib.h>

#include "usb.h"
#include "hid.h"
#include "cdc.h"
#include <stdio.h>


int main(void)
{
    stdio_init_all();
    usb_init();
    while (1)
    {
        absolute_time_t before = get_absolute_time();

        /* Check for PC UART data */
        cdc_process();
        /* Proceed with HID & housekeeping */
        hid_process(); // FIXME these functions will be called by the controller task instead
                       // Could cause trouble since it is calling from another thread? Probably not..
        usb_housekeeping();
    }
    return 0;
}
