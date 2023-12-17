#include "usb.h"
#include "bsp/board.h"
#include "tusb.h"

// Invoked when device is mounted
void tud_mount_cb(void)
{
    //blink_interval_ms = BLINK_MOUNTED;
}

// Invoked when device is unmounted
void tud_umount_cb(void)
{
    //blink_interval_ms = BLINK_NOT_MOUNTED;
}

// Invoked when usb bus is suspended
// remote_wakeup_en : if host allow us  to perform remote wakeup
// Within 7ms, device must draw an average of current less than 2.5 mA from bus
void tud_suspend_cb(bool remote_wakeup_en)
{
    (void) remote_wakeup_en;
    //blink_interval_ms = BLINK_SUSPENDED;
}

// Invoked when usb bus is resumed
void tud_resume_cb(void)
{
    //blink_interval_ms = BLINK_MOUNTED;
}

void usb_init()
{
    board_init();
    tusb_init();
}

void usb_housekeeping() {
    tud_task();
}
