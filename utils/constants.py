
IP_ADDR = {
    "lab": "100.100.250.30",
    "engine_talon": "100.97.216.58",
    "engine_win11_swe": "100.106.115.19",
    "work": "100.101.164.159",
    "station": "100.121.51.47",
}

CLIENTS = ["work", "station"]
SERVERS = ["lab", "engine_talon", "engine_win11_swe"]

VOICE_BOX_CLIENT_PORT="5000"

GST_SOUND_PORT="5137"

LINUX_USER="ripxorip"
TMUX_SESSION_NAME="ripxospeech"

HID_COMMANDS = {
    "stop": 0x01,
    "start_talon_command": 0x02,
    "start_talon_dictation": 0x03,
    "start_win11_swe": 0x04,
    "start_gdocs": 0x05
}