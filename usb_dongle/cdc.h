#ifndef __CDC_H__
#define __CDC_H__

#include <stdint.h>

/* Returns number of bytes read (buf shall be atleast 64 bytes long) */
void cdc_process();

#endif // !__CDC_H__
