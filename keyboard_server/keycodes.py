x11_key_code_to_name = {
    0x09: "KEY_ESC",
    0x0A: "KEY_1",
    0x0B: "KEY_2",
    0x0C: "KEY_3",
    0x0D: "KEY_4",
    0x0E: "KEY_5",
    0x0F: "KEY_6",
    0x10: "KEY_7",
    0x11: "KEY_8",
    0x12: "KEY_9",
    0x13: "KEY_0",
    0x14: "KEY_MINUS",
    0x15: "KEY_EQUAL",
    0x16: "KEY_BACKSPACE",
    0x17: "KEY_TAB",
    0x18: "KEY_Q",
    0x19: "KEY_W",
    0x1A: "KEY_E",
    0x1B: "KEY_R",
    0x1C: "KEY_T",
    0x1D: "KEY_Y",
    0x1E: "KEY_U",
    0x1F: "KEY_I",
    0x20: "KEY_O",
    0x21: "KEY_P",
    0x22: "KEY_LEFTBRACE",
    0x23: "KEY_RIGHTBRACE",
    0x24: "KEY_ENTER",
    0x25: "KEY_LEFTCTRL",
    0x26: "KEY_A",
    0x27: "KEY_S",
    0x28: "KEY_D",
    0x29: "KEY_F",
    0x2A: "KEY_G",
    0x2B: "KEY_H",
    0x2C: "KEY_J",
    0x2D: "KEY_K",
    0x2E: "KEY_L",
    0x2F: "KEY_SEMICOLON",
    0x30: "KEY_APOSTROPHE",
    0x31: "KEY_GRAVE",
    0x32: "KEY_LEFTSHIFT",
    0x33: "KEY_BACKSLASH",
    0x34: "KEY_Z",
    0x35: "KEY_X",
    0x36: "KEY_C",
    0x37: "KEY_V",
    0x38: "KEY_B",
    0x39: "KEY_N",
    0x3A: "KEY_M",
    0x3B: "KEY_COMMA",
    0x3C: "KEY_DOT",
    0x3D: "KEY_SLASH",
    0x3E: "KEY_RIGHTSHIFT",
    0x3F: "KEY_KPASTERISK",
    0x40: "KEY_LEFTALT",
    0x41: "KEY_SPACE",
    0x42: "KEY_CAPSLOCK",
    0x43: "KEY_F1",
    0x44: "KEY_F2",
    0x45: "KEY_F3",
    0x46: "KEY_F4",
    0x47: "KEY_F5",
    0x48: "KEY_F6",
    0x49: "KEY_F7",
    0x4A: "KEY_F8",
    0x4B: "KEY_F9",
    0x4C: "KEY_F10",
    0x4D: "KEY_NUMLOCK",
    0x4E: "KEY_SCROLLLOCK",
    0x4F: "KEY_KP7",
    0x50: "KEY_KP8",
    0x51: "KEY_KP9",
    0x52: "KEY_KPMINUS",
    0x53: "KEY_KP4",
    0x54: "KEY_KP5",
    0x55: "KEY_KP6",
    0x56: "KEY_KPPLUS",
    0x57: "KEY_KP1",
    0x58: "KEY_KP2",
    0x59: "KEY_KP3",
    0x5A: "KEY_KP0",
    0x5B: "KEY_KPDOT",
    0x5D: "KEY_ZENKAKUHANKAKU",
    0x5E: "KEY_102ND",
    0x5F: "KEY_F11",
    0x60: "KEY_F12",
    0x61: "KEY_RO",
    0x62: "KEY_KATAKANA",
    0x63: "KEY_HIRAGANA",
    0x64: "KEY_HENKAN",
    0x65: "KEY_KATAKANAHIRAGANA",
    0x66: "KEY_MUHENKAN",
    0x67: "KEY_KPJPCOMMA",
    0x68: "KEY_KPENTER",
    0x69: "KEY_RIGHTCTRL",
    0x6A: "KEY_KPSLASH",
    0x6B: "KEY_SYSRQ",
    0x6C: "KEY_RIGHTALT",
    0x6D: "KEY_LINEFEED",
    0x6E: "KEY_HOME",
    0x6F: "KEY_UP",
    0x70: "KEY_PAGEUP",
    0x71: "KEY_LEFT",
    0x72: "KEY_RIGHT",
    0x73: "KEY_END",
    0x74: "KEY_DOWN",
    0x75: "KEY_PAGEDOWN",
    0x76: "KEY_INSERT",
    0x77: "KEY_DELETE",
    0x78: "KEY_MACRO",
    0x79: "KEY_MUTE",
    0x7A: "KEY_VOLUMEDOWN",
    0x7B: "KEY_VOLUMEUP",
    0x7C: "KEY_POWER",
    0x7D: "KEY_KPEQUAL",
    0x7E: "KEY_KPPLUSMINUS",
    0x7F: "KEY_PAUSE",
    0x80: "KEY_SCALE",
    0x81: "KEY_KPCOMMA",
    0x82: "KEY_HANGUEL",
    0x83: "KEY_HANJA",
    0x84: "KEY_YEN",
    0x85: "KEY_LEFTMETA",
    0x86: "KEY_RIGHTMETA",
    0x87: "KEY_COMPOSE",
    0xca: "SPEC_KEY_Ä",
    0xcc: "SPEC_KEY_Å",
    0xe6: "SPEC_KEY_Ö"
}

key_name_to_hid_report_code = {
    "KEY_NONE": 0x00,
    "KEY_ERR_OVF": 0x01,
    "KEY_A": 0x04,
    "KEY_B": 0x05,
    "KEY_C": 0x06,
    "KEY_D": 0x07,
    "KEY_E": 0x08,
    "KEY_F": 0x09,
    "KEY_G": 0x0a,
    "KEY_H": 0x0b,
    "KEY_I": 0x0c,
    "KEY_J": 0x0d,
    "KEY_K": 0x0e,
    "KEY_L": 0x0f,
    "KEY_M": 0x10,
    "KEY_N": 0x11,
    "KEY_O": 0x12,
    "KEY_P": 0x13,
    "KEY_Q": 0x14,
    "KEY_R": 0x15,
    "KEY_S": 0x16,
    "KEY_T": 0x17,
    "KEY_U": 0x18,
    "KEY_V": 0x19,
    "KEY_W": 0x1a,
    "KEY_X": 0x1b,
    "KEY_Y": 0x1c,
    "KEY_Z": 0x1d,
    "KEY_1": 0x1e,
    "KEY_2": 0x1f,
    "KEY_3": 0x20,
    "KEY_4": 0x21,
    "KEY_5": 0x22,
    "KEY_6": 0x23,
    "KEY_7": 0x24,
    "KEY_8": 0x25,
    "KEY_9": 0x26,
    "KEY_0": 0x2,
    "KEY_ENTER": 0x28,
    "KEY_ESC": 0x29,
    "KEY_BACKSPACE": 0x2a,
    "KEY_TAB": 0x2b,
    "KEY_SPACE": 0x2c,
    "KEY_MINUS": 0x2d,
    "KEY_EQUAL": 0x2e,
    "KEY_LEFTBRACE": 0x2f,
    "KEY_RIGHTBRACE": 0x30,
    "KEY_BACKSLASH": 0x31,
    "KEY_HASHTILDE": 0x32,
    "KEY_SEMICOLON": 0x33,
    "KEY_APOSTROPHE": 0x34,
    "KEY_GRAVE": 0x35,
    "KEY_COMMA": 0x36,
    "KEY_DOT": 0x37,
    "KEY_SLASH": 0x38,
    "KEY_CAPSLOCK": 0x3,
    "KEY_F1": 0x3a,
    "KEY_F2": 0x3b,
    "KEY_F3": 0x3c,
    "KEY_F4": 0x3d,
    "KEY_F5": 0x3e,
    "KEY_F6": 0x3f,
    "KEY_F7": 0x40,
    "KEY_F8": 0x41,
    "KEY_F9": 0x42,
    "KEY_F10": 0x43,
    "KEY_F11": 0x44,
    "KEY_F12": 0x4,
    "KEY_SYSRQ": 0x46,
    "KEY_SCROLLLOCK": 0x47,
    "KEY_PAUSE": 0x48,
    "KEY_INSERT": 0x49,
    "KEY_HOME": 0x4a,
    "KEY_PAGEUP": 0x4b,
    "KEY_DELETE": 0x4c,
    "KEY_END": 0x4d,
    "KEY_PAGEDOWN": 0x4e,
    "KEY_RIGHT": 0x4f,
    "KEY_LEFT": 0x50,
    "KEY_DOWN": 0x51,
    "KEY_UP": 0x52,
    "KEY_NUMLOCK": 0x53,
    "KEY_KPSLASH": 0x54,
    "KEY_KPASTERISK": 0x55,
    "KEY_KPMINUS": 0x56,
    "KEY_KPPLUS": 0x57,
    "KEY_KPENTER": 0x58,
    "KEY_KP1": 0x59,
    "KEY_KP2": 0x5a,
    "KEY_KP3": 0x5b,
    "KEY_KP4": 0x5c,
    "KEY_KP5": 0x5d,
    "KEY_KP6": 0x5e,
    "KEY_KP7": 0x5f,
    "KEY_KP8": 0x60,
    "KEY_KP9": 0x61,
    "KEY_KP0": 0x62,
    "KEY_KPDOT": 0x6,
    "KEY_102ND": 0x64,
    "KEY_COMPOSE": 0x65,
    "KEY_POWER": 0x66,
    "KEY_KPEQUAL": 0x6,
    "KEY_F13": 0x68,
    "KEY_F14": 0x69,
    "KEY_F15": 0x6a,
    "KEY_F16": 0x6b,
    "KEY_F17": 0x6c,
    "KEY_F18": 0x6d,
    "KEY_F19": 0x6e,
    "KEY_F20": 0x6f,
    "KEY_F21": 0x70,
    "KEY_F22": 0x71,
    "KEY_F23": 0x72,
    "KEY_F24": 0x7,
    "KEY_OPEN": 0x74,
    "KEY_HELP": 0x75,
    "KEY_PROPS": 0x76,
    "KEY_FRONT": 0x77,
    "KEY_STOP": 0x78,
    "KEY_AGAIN": 0x79,
    "KEY_UNDO": 0x7a,
    "KEY_CUT": 0x7b,
    "KEY_COPY": 0x7c,
    "KEY_PASTE": 0x7d,
    "KEY_FIND": 0x7e,
    "KEY_MUTE": 0x7f,
    "KEY_VOLUMEUP": 0x80,
    "KEY_VOLUMEDOWN": 0x8,
    "KEY_KPCOMMA": 0x8,
    "KEY_RO": 0x87,
    "KEY_KATAKANAHIRAGANA": 0x88,
    "KEY_YEN": 0x89,
    "KEY_HENKAN": 0x8a,
    "KEY_MUHENKAN": 0x8b,
    "KEY_KPJPCOMMA": 0x8,
    "KEY_HANGEUL": 0x90,
    "KEY_HANJA": 0x91,
    "KEY_KATAKANA": 0x92,
    "KEY_HIRAGANA": 0x93,
    "KEY_ZENKAKUHANKAKU": 0x9,
    "KEY_KPLEFTPAREN": 0xb6,
    "KEY_KPRIGHTPAREN": 0xb,
    "KEY_LEFTCTRL": 0xe0,
    "KEY_LEFTSHIFT": 0xe1,
    "KEY_LEFTALT": 0xe2,
    "KEY_LEFTMETA": 0xe3,
    "KEY_RIGHTCTRL": 0xe4,
    "KEY_RIGHTSHIFT": 0xe5,
    "KEY_RIGHTALT": 0xe6,
    "KEY_RIGHTMETA": 0xe7,
    "KEY_MEDIA_PLAYPAUSE": 0xe,
    "KEY_MEDIA_STOPCD": 0xe,
    "KEY_MEDIA_PREVIOUSSONG": 0xe,
    "KEY_MEDIA_NEXTSONG": 0xe,
    "KEY_MEDIA_EJECTCD": 0xe,
    "KEY_MEDIA_VOLUMEUP": 0xe,
    "KEY_MEDIA_VOLUMEDOWN": 0xe,
    "KEY_MEDIA_MUTE": 0xe,
    "KEY_MEDIA_WWW": 0xf,
    "KEY_MEDIA_BACK": 0xf,
    "KEY_MEDIA_FORWARD": 0xf,
    "KEY_MEDIA_STOP": 0xf,
    "KEY_MEDIA_FIND": 0xf,
    "KEY_MEDIA_SCROLLUP": 0xf,
    "KEY_MEDIA_SCROLLDOWN": 0xf,
    "KEY_MEDIA_EDIT": 0xf,
    "KEY_MEDIA_SLEEP": 0xf,
    "KEY_MEDIA_COFFEE": 0xf,
    "KEY_MEDIA_REFRESH": 0xf,
    "KEY_MEDIA_CALC": 0xfb
}

# TODO Currently done with copilot, needs extra verification
def qwerty_to_colemak_dh(key):
    if key == "KEY_Q":
        return "KEY_Q"
    elif key == "KEY_W":
        return "KEY_W"
    elif key == "KEY_E":
        return "KEY_K"
    elif key == "KEY_R":
        return "KEY_S"
    elif key == "KEY_T":
        return "KEY_F"
    elif key == "KEY_Y":
        return "KEY_O"
    elif key == "KEY_U":
        return "KEY_I"
    elif key == "KEY_I":
        return "KEY_L"
    elif key == "KEY_O":
        return "KEY_SEMICOLON"
    elif key == "KEY_P":
        return "KEY_R"
    elif key == "KEY_LEFTBRACE":
        return "KEY_LEFTBRACE"
    elif key == "KEY_RIGHTBRACE":
        return "KEY_RIGHTBRACE"
    elif key == "KEY_A":
        return "KEY_A"
    elif key == "KEY_S":
        return "KEY_D"
    elif key == "KEY_D":
        return "KEY_C"
    elif key == "KEY_F":
        return "KEY_E"
    elif key == "KEY_G":
        return "KEY_G"
    elif key == "KEY_H":
        return "KEY_M"
    elif key == "KEY_J":
        return "KEY_Y"
    elif key == "KEY_K":
        return "KEY_N"
    elif key == "KEY_L":
        return "KEY_U"
    elif key == "KEY_SEMICOLON":
        return "KEY_O"
    elif key == "KEY_APOSTROPHE":
        return "KEY_APOSTROPHE"
    elif key == "KEY_Z":
        return "KEY_B"
    elif key == "KEY_X":
        return "KEY_Z"
    elif key == "KEY_C":
        return "KEY_X"
    elif key == "KEY_V":
        return "KEY_V"
    elif key == "KEY_B":
        return "KEY_T"
    elif key == "KEY_N":
        return "KEY_J"
    elif key == "KEY_M":
        return "KEY_H"
    elif key == "KEY_COMMA":
        return "KEY_COMMA"
    elif key == "KEY_DOT":
        return "KEY_DOT"
    elif key == "KEY_SLASH":
        return "KEY_SLASH"
    elif key == "KEY_BACKSLASH":
        return "KEY_BACK"
    else:
        return key

keyname_to_linux_event_code = {
    'KEY_0': 11,
    'KEY_1': 2,
    'KEY_102ND': 86,
    'KEY_2': 3,
    'KEY_3': 4,
    'KEY_4': 5,
    'KEY_5': 6,
    'KEY_6': 7,
    'KEY_7': 8,
    'KEY_8': 9,
    'KEY_9': 10,
    'KEY_A': 30,
    'KEY_AGAIN': 129,
    'KEY_ALTERASE': 222,
    'KEY_APOSTROPHE': 40,
    'KEY_B': 48,
    'KEY_BACKSLASH': 43,
    'KEY_BACKSPACE': 14,
    'KEY_BASSBOOST': 209,
    'KEY_BATTERY': 236,
    'KEY_BLUETOOTH': 237,
    'KEY_BRIGHTNESSDOWN': 224,
    'KEY_BRIGHTNESSUP': 225,
    'KEY_BRIGHTNESS_ZERO': 'KEY_BRIGHTNESS_AUTO',
    'KEY_C': 46,
    'KEY_CAMERA': 212,
    'KEY_CAPSLOCK': 58,
    'KEY_CHAT': 216,
    'KEY_CLOSECD': 160,
    'KEY_COMMA': 51,
    'KEY_COMPOSE': 127,
    'KEY_COMPUTER': 157,
    'KEY_CONNECT': 218,
    'KEY_CYCLEWINDOWS': 154,
    'KEY_D': 32,
    'KEY_DASHBOARD': 'KEY_ALL_APPLICATIONS',
    'KEY_DELETE': 111,
    'KEY_DELETEFILE': 146,
    'KEY_DIRECTION': 'KEY_ROTATE_DISPLAY',
    'KEY_DOCUMENTS': 235,
    'KEY_DOT': 52,
    'KEY_DOWN': 108,
    'KEY_E': 18,
    'KEY_EDIT': 176,
    'KEY_EJECTCD': 161,
    'KEY_EJECTCLOSECD': 162,
    'KEY_EMAIL': 215,
    'KEY_END': 107,
    'KEY_ENTER': 28,
    'KEY_EQUAL': 13,
    'KEY_ESC': 1,
    'KEY_F': 33,
    'KEY_F1': 59,
    'KEY_F10': 68,
    'KEY_F11': 87,
    'KEY_F12': 88,
    'KEY_F13': 183,
    'KEY_F14': 184,
    'KEY_F15': 185,
    'KEY_F16': 186,
    'KEY_F17': 187,
    'KEY_F18': 188,
    'KEY_F19': 189,
    'KEY_F2': 60,
    'KEY_F20': 190,
    'KEY_F21': 191,
    'KEY_F22': 192,
    'KEY_F23': 193,
    'KEY_F24': 194,
    'KEY_F3': 61,
    'KEY_F4': 62,
    'KEY_F5': 63,
    'KEY_F6': 64,
    'KEY_F7': 65,
    'KEY_F8': 66,
    'KEY_F9': 67,
    'KEY_FASTFORWARD': 208,
    'KEY_FRONT': 132,
    'KEY_G': 34,
    'KEY_GRAVE': 41,
    'KEY_H': 35,
    'KEY_HANGEUL': 122,
    'KEY_HANGUEL': 'KEY_HANGEUL',
    'KEY_HANJA': 123,
    'KEY_HENKAN': 92,
    'KEY_HIRAGANA': 91,
    'KEY_HOME': 102,
    'KEY_HP': 211,
    'KEY_I': 23,
    'KEY_INSERT': 110,
    'KEY_ISO': 170,
    'KEY_J': 36,
    'KEY_K': 37,
    'KEY_KATAKANA': 90,
    'KEY_KATAKANAHIRAGANA': 93,
    'KEY_KBDILLUMDOWN': 229,
    'KEY_KBDILLUMTOGGLE': 228,
    'KEY_KBDILLUMUP': 230,
    'KEY_KP0': 82,
    'KEY_KP1': 79,
    'KEY_KP2': 80,
    'KEY_KP3': 81,
    'KEY_KP4': 75,
    'KEY_KP5': 76,
    'KEY_KP6': 77,
    'KEY_KP7': 71,
    'KEY_KP8': 72,
    'KEY_KP9': 73,
    'KEY_KPASTERISK': 55,
    'KEY_KPCOMMA': 121,
    'KEY_KPDOT': 83,
    'KEY_KPENTER': 96,
    'KEY_KPEQUAL': 117,
    'KEY_KPJPCOMMA': 95,
    'KEY_KPLEFTPAREN': 179,
    'KEY_KPMINUS': 74,
    'KEY_KPPLUS': 78,
    'KEY_KPPLUSMINUS': 118,
    'KEY_KPRIGHTPAREN': 180,
    'KEY_KPSLASH': 98,
    'KEY_L': 38,
    'KEY_LEFT': 105,
    'KEY_LEFTALT': 56,
    'KEY_LEFTBRACE': 26,
    'KEY_LEFTCTRL': 29,
    'KEY_LEFTMETA': 125,
    'KEY_LEFTSHIFT': 42,
    'KEY_LINEFEED': 101,
    'KEY_M': 50,
    'KEY_MACRO': 112,
    'KEY_MAIL': 155,
    'KEY_MEDIA': 226,
    'KEY_MINUS': 12,
    'KEY_MOVE': 175,
    'KEY_MSDOS': 151,
    'KEY_MUHENKAN': 94,
    'KEY_MUTE': 113,
    'KEY_N': 49,
    'KEY_NEXTSONG': 163,
    'KEY_NUMLOCK': 69,
    'KEY_O': 24,
    'KEY_P': 25,
    'KEY_PAGEDOWN': 109,
    'KEY_PAGEUP': 104,
    'KEY_PAUSE': 119,
    'KEY_PAUSECD': 201,
    'KEY_PLAY': 207,
    'KEY_PLAYCD': 200,
    'KEY_PLAYPAUSE': 164,
    'KEY_PREVIOUSSONG': 165,
    'KEY_PROG1': 148,
    'KEY_PROG2': 149,
    'KEY_PROG3': 202,
    'KEY_PROG4': 203,
    'KEY_Q': 16,
    'KEY_QUESTION': 214,
    'KEY_R': 19,
    'KEY_RECORD': 167,
    'KEY_RESERVED': 0,
    'KEY_REWIND': 168,
    'KEY_RIGHT': 106,
    'KEY_RIGHTALT': 100,
    'KEY_RIGHTBRACE': 27,
    'KEY_RIGHTCTRL': 97,
    'KEY_RIGHTMETA': 126,
    'KEY_RIGHTSHIFT': 54,
    'KEY_RO': 89,
    'KEY_S': 31,
    'KEY_SCREENLOCK': 'KEY_COFFEE',
    'KEY_SCROLLDOWN': 178,
    'KEY_SCROLLLOCK': 70,
    'KEY_SCROLLUP': 177,
    'KEY_SEARCH': 217,
    'KEY_SEMICOLON': 39,
    'KEY_SENDFILE': 145,
    'KEY_SETUP': 141,
    'KEY_SHOP': 221,
    'KEY_SLASH': 53,
    'KEY_SOUND': 213,
    'KEY_SPACE': 57,
    'KEY_SPORT': 220,
    'KEY_STOPCD': 166,
    'KEY_SUSPEND': 205,
    'KEY_SYSRQ': 99,
    'KEY_T': 20,
    'KEY_TAB': 15,
    'KEY_U': 22,
    'KEY_UNKNOWN': 240,
    'KEY_UP': 103,
    'KEY_UWB': 239,
    'KEY_V': 47,
    'KEY_VOLUMEDOWN': 114,
    'KEY_VOLUMEUP': 115,
    'KEY_W': 17,
    'KEY_WIMAX': 'KEY_WWAN',
    'KEY_WLAN': 238,
    'KEY_X': 45,
    'KEY_XFER': 147,
    'KEY_Y': 21,
    'KEY_YEN': 124,
    'KEY_Z': 44,
    'KEY_ZENKAKUHANKAKU': 85
}