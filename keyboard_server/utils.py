import socket
from utils.constants import *
from keyboard_server.keycodes import *

def get_x11_keycode_from_name(name):
    ret = None
    for key, value in x11_key_code_to_name.items():
        if value == name:
            ret = key
            break
    return ret

def process_altgr_modifiers(chunk):
    ret = chunk
    indices = [i for i, x in enumerate(chunk) if x[0] == get_x11_keycode_from_name("KEY_RIGHTALT")]
    if len(indices) == 0:
        return ret
    for i in indices:
        if i+1 < len(chunk):
            if chunk[i+1][0] == get_x11_keycode_from_name("KEY_R"):
                ret[i] = (get_x11_keycode_from_name("SPEC_KEY_Ä"), 0)
                ret[i+1] = (0, 0)
            elif chunk[i+1][0] == get_x11_keycode_from_name("KEY_A"):
                ret[i] = (get_x11_keycode_from_name("SPEC_KEY_Å"), 0)
                ret[i+1] = (0, 0)
            elif chunk[i+1][0] == get_x11_keycode_from_name("KEY_O"):
                ret[i] = (get_x11_keycode_from_name("SPEC_KEY_Ö"), 0)
                ret[i+1] = (0, 0)
    filt = []
    for i in range(len(ret)):
        if ret[i] == (0, 0):
            continue
        filt.append(ret[i])
    ret = filt
    return ret

def process_shift_modifiers(chunk):
    ret = chunk
    # Get the indices of all shift key presses
    indices = [i for i, x in enumerate(chunk) if x == "key_leftshift" or x == "key_rightshift"]
    for i in indices:
        if i+1 < len(chunk):
            ret[i] = ''
            ret[i + 1] = ret[i + 1].upper()
    filt = []
    for i in range(len(ret)):
        if ret[i] == '':
            continue
        filt.append(ret[i])
    ret = filt
    return ret

def filter_keyup_events(chunk):
    ret = []
    for c in chunk:
        if c[1] == 0:
            ret.append(c)
    return ret

def convert_chunk_to_text(chunk):
    ret = ""
    c = filter_keyup_events(chunk)
    c = process_altgr_modifiers(c)
    c = [x11_key_code_to_name[x[0]].lower() for x in c]
    # Find shift key presses
    c = process_shift_modifiers(c)
    for k in c:
        # Handle special keys, case means that it has been shifted
        if k == "key_space":
            ret += " "
        elif k == "KEY_SLASH":
            ret += "?"
        elif k == "KEY_1":
            ret += "!"
        elif k == "key_dot":
            ret += "."
        elif k == "key_comma":
            ret += ","
        elif k == "key_minus":
            ret += "-"
        else:
            k = k.replace("spec_key_", "")
            k = k.replace("key_", "")
            k = k.replace("SPEC_KEY_", "")
            k = k.replace("KEY_", "")
            if len(k) == 1:
                ret += k
            else:
                print("Unknown key: {}".format(k))
    return ret

def convert_text_to_chunk(text):
    ret = []
    for c in text:
        if c in x11_char_to_keycode and x11_char_to_keycode[c] != 0:
            ret.append((x11_char_to_keycode[c], 0))
            ret.append((x11_char_to_keycode[c], 1))
            continue
        is_upper = c.isupper()
        if is_upper:
            ret.append((x11_char_to_keycode["leftshift"], 0))
        c = c.lower()
        if c == 'ö':
            ret.append((x11_char_to_keycode["rightalt"], 0))
            ret.append((x11_char_to_keycode["o"], 0))
            ret.append((x11_char_to_keycode["o"], 1))
            ret.append((x11_char_to_keycode["rightalt"], 1))
        elif c == 'å':
            ret.append((x11_char_to_keycode["rightalt"], 0))
            ret.append((x11_char_to_keycode["a"], 0))
            ret.append((x11_char_to_keycode["a"], 1))
            ret.append((x11_char_to_keycode["rightalt"], 1))
        elif c == 'ä':
            ret.append((x11_char_to_keycode["rightalt"], 0))
            ret.append((x11_char_to_keycode["r"], 0))
            ret.append((x11_char_to_keycode["r"], 1))
            ret.append((x11_char_to_keycode["rightalt"], 1))
        elif c == '?':
            ret.append((x11_char_to_keycode["leftshift"], 0))
            ret.append((x11_char_to_keycode["/"], 0))
            ret.append((x11_char_to_keycode["/"], 1))
            ret.append((x11_char_to_keycode["leftshift"], 1))
        elif c == '!':
            ret.append((x11_char_to_keycode["leftshift"], 0))
            ret.append((x11_char_to_keycode["1"], 0))
            ret.append((x11_char_to_keycode["1"], 1))
            ret.append((x11_char_to_keycode["leftshift"], 1))
        else:
            ret.append((x11_char_to_keycode[c], 0))
            ret.append((x11_char_to_keycode[c], 1))
        if is_upper:
            ret.append((x11_char_to_keycode["leftshift"], 1))
    return ret

def send_udp_string(server, port, string):
    # Convert the string to bytes
    bytes = string.encode('utf-8')
    # Send the specified bytes to the specified server over UDP using socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes, (IP_ADDR[server], port))
