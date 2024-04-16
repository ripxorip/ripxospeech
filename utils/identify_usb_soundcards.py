import subprocess
import json
import time
import wave
import re

class SoundCardIdentifier:
    def __init__(self):
        self.devices = []

    def run(self):
        self.enumerate()
        self.find_master()

    def find_master(self):
        max_vals = []
        for d in self.devices:
            proposed_master = d
            # Slaves is the other devices in the list
            slaves = [x for x in self.devices if x != proposed_master]
            master_cmd = f"speaker-test -t sine -D {proposed_master['alsa']} -c 2 -l 1"
            slave_one_arecord_cmd = f"arecord -D {slaves[0]['alsa']} -f cd -d 4 -t wav -c 1 /tmp/slave1.wav"
            slave_two_arecord_cmd = f"arecord -D {slaves[1]['alsa']} -f cd -d 4 -t wav -c 1 /tmp/slave2.wav"
            print(slave_one_arecord_cmd)
            print(f"\n\n**Testing master: {proposed_master['alsa']}\n\n")
            # Start the commands non-blocking
            subprocess.Popen(master_cmd, shell=True)
            subprocess.Popen(slave_one_arecord_cmd, shell=True)
            subprocess.Popen(slave_two_arecord_cmd, shell=True)
            # Wait for the commands to finish
            time.sleep(5)
            # Parse the WAV files and find the maximum sample
            slave_max = []
            for slave_file in ['/tmp/slave1.wav', '/tmp/slave2.wav']:
                with wave.open(slave_file, 'rb') as wav_file:
                    samples = [int.from_bytes(wav_file.readframes(1), 'little', signed=True) for _ in range(wav_file.getnframes())]
                    max_sample = max(abs(sample) for sample in samples)
                    slave_max.append(max_sample)
            max_vals.append((proposed_master, slave_max))
        # Find the master with the highest slave max
        max_master = max(max_vals, key=lambda x: sum(x[1]))[0]

        base_str = """
        <hostdev mode='subsystem' type='usb' managed='no'>
            <source>
                <address bus='{bus}' device='{device}'/>
            </source>
        </hostdev>
        """

        print("\n\n\n** Master device: **")
        print(max_master)
        print("** Slave devices: **")
        self.slaves = []
        for d in self.devices:
            if d != max_master:
                print(d)
                self.slaves.append(d)

        with open('/tmp/ripxospeech_slave_one.xml', 'w') as f:
            f.write(base_str.format(bus=slaves[0]['usb']['bus'], device=slaves[0]['usb']['dev']))

        with open('/tmp/ripxospeech_slave_two.xml', 'w') as f:
            f.write(base_str.format(bus=slaves[1]['usb']['bus'], device=slaves[1]['usb']['dev']))

        with open('/tmp/ripxospeech_master.xml', 'w') as f:
            f.write(base_str.format(bus=max_master['usb']['bus'], device=max_master['usb']['dev']))

    def correlate_bus_port_to_device(self, bus, port):
        bus = int(bus)
        print(f"Bus: {bus}, Port: {port}")
        # Get the result of lsusb -t
        res = subprocess.run(["lsusb", "-t"], stdout=subprocess.PIPE)
        res = res.stdout.decode('utf-8')
        busFound = False
        portPartOnefound = False
        portPartTwoFound = False
        portPartOne = port.split(".")[0]
        portPartTwo = port.split(".")[1]
        for l in res.split("\n"):
            if not busFound:
                if l.startswith("/:  Bus "):
                    pattern = r"/:  Bus (\d+)"
                    busNum = int(re.search(pattern, l).group(1))
                    if busNum == bus:
                        busFound = True
            elif not portPartOnefound:
                if l.startswith("    |__ Port "):
                    pattern = r"    \|__ Port (\d+)"
                    portNum = int(re.search(pattern, l).group(1))
                    if portNum == int(portPartOne):
                        portPartOnefound = True
            elif not portPartTwoFound:
                if l.startswith("        |__ Port "):
                    pattern = r"        \|__ Port (\d+)"
                    portNum = int(re.search(pattern, l).group(1))
                    if portNum == int(portPartTwo):
                        portPartTwoFound = True
                        pattern = r"        \|__ Port \d+: Dev (\d+)"
                        devNum = int(re.search(pattern, l).group(1))
                        return {"bus": bus, "dev": devNum}

    def enumerate(self):
        # Parse output of pw-dump as json
        # Run pw-dump and parse output
        res = subprocess.run(["pw-dump"], stdout=subprocess.PIPE)
        # Parse output as json
        res = json.loads(res.stdout)
        # Pretty print json
        for i in res:
            if (i["type"] == "PipeWire:Interface:Device" and ("C-Media Electronics" in i["info"]["props"]["alsa.long_card_name"])):
                u = i["info"]["props"]["device.sysfs.path"]
                u = u.split("/")
                u = u[7]
                su = u.split("-")
                bus = su[0]
                port =su[1]
                usb_bus_dev = self.correlate_bus_port_to_device(bus, port)
                d = {'alsa': i["info"]["props"]["api.alsa.path"], 'usb': usb_bus_dev}
                self.devices.append(d)

def main():
    si = SoundCardIdentifier()
    si.run()

if __name__ == "__main__":
    main()