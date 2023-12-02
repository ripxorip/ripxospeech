# This backend is used together with an embedded device such as the rp2040.
# Each report is sent to the device over serial and the device sends the corresponding HID report
# to the host as a keyboard. The communication from the backend comes from UDP/IP instead of hid packets