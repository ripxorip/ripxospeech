#include "tusb.h"
#include "cdc.h"
#include "pc_protocol.h"

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

void cdc_process() {
    // connected and there are data available
    if ( tud_cdc_available() )
    {
        uint32_t recv = tud_cdc_read(cdc_rx_buf, sizeof(cdc_rx_buf));
        if (recv) {
            for (uint32_t i = 0; i < recv; i++)
            {
                uint32_t protocol_data_to_be_sent = pc_protocol_process_incoming_byte(cdc_rx_buf[i], cdc_tx_buf);
                if (protocol_data_to_be_sent)
                {
                    tud_cdc_write(cdc_tx_buf, protocol_data_to_be_sent);
                    tud_cdc_write_flush();
                }
            }
        }

    }
}
