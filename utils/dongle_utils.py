import os
import subprocess
import time

def get_dongle_serial_port():
    dongle_name = "Ripxospeech_Dongle"
    ret = subprocess.check_output(["ls", "/dev"]).decode("utf-8").strip().splitlines()
    # Find which tty device is the USB device
    for r in ret:
        if "ttyACM" in r:
            # Get the device path
            dev_path = "/dev/" + r
            # Get the device information using udevadm
            info = subprocess.check_output(["udevadm", "info", "--name=" + dev_path, "--query=all"]).decode("utf-8")
            # Check if the information contains the USB ID
            if dongle_name in info:
                return dev_path
    print('Error: Could not find any ports associated with: {}'.format(dongle_name))
    return None

def put_dongle_in_bootloader():
    # Get the serial port of the dongle
    dev_path = get_dongle_serial_port()
    if dev_path == None:
        return
    print("Found dongle at: {}".format(dev_path))
    # Put the dongle in bootloader mode by opening the serial port and sending 0x66
    os.system("echo -ne '\\x66' | sudo tee {}".format(dev_path))

def flash_dongle(firmware_path):
    put_dongle_in_bootloader()
    time.sleep(3)
    # Flash the dongle
    os.system("sudo picotool load {}".format(firmware_path))
    os.system("sudo picotool reboot")

if __name__ == "__main__":
    flash_dongle("build/ripxospeech_controller_firmware.uf2")