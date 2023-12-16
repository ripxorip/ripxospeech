#include "tusb.h"
#include "cdc.h"
#include "app.h"

static uint8_t cdc_rx_buf[64];
static uint8_t cdc_tx_buf[64];

// Invoked when cdc when line state changed e.g connected/disconnected
void tud_cdc_line_state_cb(uint8_t itf, bool dtr, bool rts)
{
    (void) itf;
    (void) rts;

    // TODO set some indicator
    if ( dtr )
    {
        // Terminal connected
    }else
    {
        // Terminal disconnected
    }
}
//
// Invoked when CDC interface received data from host
void tud_cdc_rx_cb(uint8_t itf)
{
    (void) itf;
}

void cdc_debug_print(const char *str) {
    memcpy(cdc_tx_buf, str, strlen(str));
    uint32_t len = strlen(str);

    cdc_tx_buf[strlen(str) + 1] = '\0';
    len += 1;

    tud_cdc_write(cdc_tx_buf, len);
    tud_cdc_write_flush();
}

void cdc_process() {
    //  only run is function every thousands time
    // connected and there are data available
    if ( tud_cdc_available() )
    {
        uint32_t recv = tud_cdc_read(cdc_rx_buf, sizeof(cdc_rx_buf));
        if (recv) {
            app_handle_incoming_bytes(cdc_rx_buf, recv);
        }
    }
}
