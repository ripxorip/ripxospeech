# This backend is used together with an embedded Linux device such as the Raspberry Pi 4.
# The device uses the use the USB gadget kernel module simulate keyboard input.

# OBSOLOTE - Just kept for reference

import os

class HID_Backend:
    def __init__(self, read_cb):
        self.read_cb = read_cb
        self.hid_fd = os.open('/dev/hidg0', os.O_RDONLY)

    def write(self, report):
        with open('/dev/hidg0', 'rb+') as fd:
            fd.write(report.encode())

    def read_thread(self):
        """Read data from HID device."""
        while True:
            # read data from HID device
            hid_data = os.read(self.hid_fd, 1024)
            # Print the data as hex with a space between each byte
            print('Got data: ', end='')
            print(' '.join(format(x, '02x') for x in hid_data))
            command = hid_data[0]
            self.read_cb(command)