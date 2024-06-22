using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using WindowsInput;
using WindowsInput.Native;
using System.Drawing.Imaging;

namespace win11_keysender
{
    public partial class Form1 : Form
    {
        private UdpClient udpClient;
        private string voiceboxclient_ip = "";
        private string sentText = "";

        private bool running = false;

        // Variable to keep what mode we are in
        private bool talon_mode = true;

        private Dictionary<string, int> charToKeyCombo = new Dictionary<string, int>()
        {
            /* These are needed as is for Windows native dictation */
            { "esc", 0x09},
            { "1", 0x0A},
            { "2", 0x0B},
            { "3", 0x0C},
            { "4", 0x0D},
            { "5", 0x0E},
            { "6", 0x0F},
            { "7", 0x10},
            { "8", 0x11},
            { "9", 0x12},
            { "0", 0x13},
            { "minus", 0x14},
            { "equal", 0x15},
            { "backspace", 0x16},
            { "leftbrace", 0x22},
            { "rightbrace", 0x23},
            { "enter", 0x24},
            { "leftctrl", 0x25},
            { "leftshift", 0x32},
            { "backslash", 0x33},
            { ",", 0x3B},
            { ".", 0x3C},
            { "/", 0x3D},
            { "leftalt", 0x40},
            { " ", 0x41},
            { "'", 0x30},

            /* Handle åäö separately */
            { "escape", 0x09},
            { "d1", 0x0A},
            { "d2", 0x0B},
            { "d3", 0x0C},
            { "d4", 0x0D},
            { "d5", 0x0E},
            { "d6", 0x0F},
            { "d7", 0x10},
            { "d8", 0x11},
            { "d9", 0x12},
            { "d0", 0x13},
            { "oemminus", 0x14},
            { "oemplus", 0x15},
            { "back", 0x16},
            { "tab", 0x17},
            { "q", 0x18},
            { "w", 0x19},
            { "e", 0x1A},
            { "r", 0x1B},
            { "t", 0x1C},
            { "y", 0x1D},
            { "u", 0x1E},
            { "i", 0x1F},
            { "o", 0x20},
            { "p", 0x21},
            { "oemopenbrackets", 0x22},
            { "oem6", 0x23},
            { "return", 0x24},
            { "controlkey", 0x25},
            { "a", 0x26},
            { "s", 0x27},
            { "d", 0x28},
            { "f", 0x29},
            { "g", 0x2A},
            { "h", 0x2B},
            { "j", 0x2C},
            { "k", 0x2D},
            { "l", 0x2E},
            { "semicolon", 0x2F},
            { "oem7", 0x30},
            { "grave", 0x31},
            { "shiftkey", 0x32},
            { "oemquestion_alt", 0x33},
            { "z", 0x34},
            { "x", 0x35},
            { "c", 0x36},
            { "v", 0x37},
            { "b", 0x38},
            { "n", 0x39},
            { "m", 0x3A},
            { "oemcomma", 0x3B},
            { "oemperiod", 0x3C},
            { "oemquestion", 0x3D},
            { "rightshift", 0x3E},
            { "kpasterisk", 0x3F},
            { "menu", 0x40},
            { "space", 0x41},
            { "capslock", 0x42},
            { "f1", 0x43},
            { "f2", 0x44},
            { "f3", 0x45},
            { "f4", 0x46},
            { "f5", 0x47},
            { "f6", 0x48},
            { "f7", 0x49},
            { "f8", 0x4A},
            { "f9", 0x4B},
            { "f10", 0x4C},
            { "numlock", 0x4D},
            { "scrolllock", 0x4E},
            { "kp7", 0x4F},
            { "kp8", 0x50},
            { "kp9", 0x51},
            { "kpminus", 0x52},
            { "kp4", 0x53},
            { "kp5", 0x54},
            { "kp6", 0x55},
            { "kpplus", 0x56},
            { "kp1", 0x57},
            { "kp2", 0x58},
            { "kp3", 0x59},
            { "kp0", 0x5A},
            { "kpdot", 0x5B},
            { "zenkakuhankaku", 0x5D},
            { "102nd", 0x5E},
            { "f11", 0x5F},
            { "f12", 0x60},
            { "ro", 0x61},
            { "katakana", 0x62},
            { "hiragana", 0x63},
            { "henkan", 0x64},
            { "katakanahiragana", 0x65},
            { "muhenkan", 0x66},
            { "kpjpcomma", 0x67},
            { "kpenter", 0x68},
            { "rightctrl", 0x69},
            { "kpslash", 0x6A},
            { "sysrq", 0x6B},
            { "rightalt", 0x6C},
            { "linefeed", 0x6D},
            { "home", 0x6E},
            { "up", 0x6F},
            { "pageup", 0x70},
            { "left", 0x71},
            { "right", 0x72},
            { "end", 0x73},
            { "down", 0x74},
            { "pagedown", 0x75},
            { "insert", 0x76},
            { "delete", 0x77},
            { "macro", 0x78},
            { "mute", 0x79},
            { "volumedown", 0x7A},
            { "volumeup", 0x7B},
            { "power", 0x7C},
            { "kpequal", 0x7D},
            { "kpplusminus", 0x7E},
            { "pause", 0x7F},
            { "scale", 0x80},
            { "kpcomma", 0x81},
            { "hanguel", 0x82},
            { "hanja", 0x83},
            { "yen", 0x84},
            { "leftmeta", 0x85},
            { "rightmeta", 0x86},
            { "compose", 0x87},
            { "\n", 0x24},
            // Special keys
            { "å", 0x00},
            { "ä", 0x00},
            { "ö", 0x00},
            { "?", 0x00},
            { "!", 0x00},
        };

        public Form1()
        {
            InitializeComponent();
            udpClient = new UdpClient(5000);
            udpClient.BeginReceive(new AsyncCallback(ReceiveCallback), null);
            //unittest_test_handle_text_change();
            textBox1.PreviewKeyDown += new PreviewKeyDownEventHandler(textBox1_PreviewKeyDown);
            textBox1.KeyUp += new KeyEventHandler(textBox1_KeyUp);
        }

        // TODO
        // This method is catching all the keystrokes, as such it is a good candidate to receive all the keystrokes also sent by Talon
        // The next step is to introduce a second mode in this module which will handle talon commands,
        // it also needs some refactoring and better naming.
        private void textBox1_PreviewKeyDown(object sender, PreviewKeyDownEventArgs e)
        {
            if (!talon_mode) { return; }
            // Print the key that was pressed
            Debug.Print("Key pressed: " + e.KeyCode.ToString());
            var keystr = e.KeyCode.ToString();
            // Convert to lower
            keystr = keystr.ToLower();
            // Get the code from lookup table
            if (charToKeyCombo.ContainsKey(keystr))
            {
                int keyCode = charToKeyCombo[keystr];
                Debug.Print(" *FOUND * Key code: " + keyCode);
                // Send the key
                send_key(keyCode, true);
            }
            else
            {
                Debug.Print("Key --not-- found in dict: " + keystr);
            }
            // Print the keycoade as hex
            //Debug.Print("Key pressed as hex: " + ((int)e.KeyCode).ToString("X"));
        }

        private void textBox1_KeyUp(object sender, KeyEventArgs e)
        {
            if (!talon_mode) { return; }
            var keystr = e.KeyCode.ToString();
            // Convert to lower
            keystr = keystr.ToLower();
            // Get the code from lookup table
            if (charToKeyCombo.ContainsKey(keystr))
            {
                int keyCode = charToKeyCombo[keystr];
                Debug.Print(" *FOUND * Key code: " + keyCode);
                // Send the key
                send_key(keyCode, false);
            }
            else
            {
                Debug.Print("Key --not-- found in dict: " + keystr);
            }
            // Print the keycoade as hex
            //Debug.Print("Key pressed as hex: " + ((int)e.KeyCode).ToString("X"));
            // Print the key that was released
            //Debug.Print("Key released: " + e.KeyCode.ToString());
        }

        private void stop() {
            // Send the escape key (stop the dictation)
            var simulator = new InputSimulator();
            simulator.Keyboard.KeyPress(VirtualKeyCode.ESCAPE);
            simulator.Keyboard.KeyPress(VirtualKeyCode.F10);
            voiceboxclient_ip = "";

            this.Invoke((MethodInvoker)delegate
            {
                textBox1.Text = "";
                sentText = "";
            });

            running = false;
            talon_mode = false;
        }

        private void ReceiveCallback(IAsyncResult ar)
        {
            IPEndPoint ip = new IPEndPoint(IPAddress.Any, 0);
            byte[] bytes = udpClient.EndReceive(ar, ref ip);
            string inputText = Encoding.ASCII.GetString(bytes);

            if (inputText.StartsWith("start@"))
            {
                talon_mode = false;
                if (running) { 
                    stop();
                    Thread.Sleep(500);
                }
                running = true;
                string[] parts = inputText.Split('@');
                if (parts.Length == 2)
                {
                    voiceboxclient_ip = parts[1];
                    var simulator = new InputSimulator();
                    simulator.Keyboard.ModifiedKeyStroke(VirtualKeyCode.LWIN, VirtualKeyCode.VK_H);
                }
            }

            if (inputText.StartsWith("start_talon_command@"))
            {
                if (running) { 
                    stop();
                }

                running = true;
                talon_mode = true;
                string[] parts = inputText.Split('@');

                if (parts.Length == 2)
                {
                    voiceboxclient_ip = parts[1];
                    var simulator = new InputSimulator();
                    simulator.Keyboard.KeyPress(VirtualKeyCode.F9);
                }
            }

            if (inputText.StartsWith("start_talon_dictation@"))
            {
                if (running) { 
                    stop();
                }

                talon_mode = true;
                running = true;
                string[] parts = inputText.Split('@');

                if (parts.Length == 2)
                {
                    voiceboxclient_ip = parts[1];
                    var simulator = new InputSimulator();
                    simulator.Keyboard.KeyPress(VirtualKeyCode.F11);
                }
            }

            else if (inputText == "stop")
            {
                stop();
            }

            else if (inputText == "toggle-lang")
            {
                var simulator = new InputSimulator();
                simulator.Keyboard.ModifiedKeyStroke(VirtualKeyCode.LWIN, VirtualKeyCode.SPACE);
                Thread.Sleep(500);
                simulator.Keyboard.ModifiedKeyStroke(VirtualKeyCode.LMENU, VirtualKeyCode.TAB);
                Thread.Sleep(500);
                simulator.Keyboard.ModifiedKeyStroke(new[] {  VirtualKeyCode.CONTROL, VirtualKeyCode.SHIFT }, VirtualKeyCode.F5);
            }

            else if (inputText == "get-current-lang")
            {
                // Take a screenshot of a specific area
                int startX = 1700;
                int startY = 1035;
                int width = 55;
                int height = 45;
                Bitmap bmpScreenCapture = new Bitmap(width, height);
                Graphics g = Graphics.FromImage(bmpScreenCapture);
                g.CopyFromScreen(startX, startY, 0, 0, new Size(width, height), CopyPixelOperation.SourceCopy);

                // Convert to grayscale
                for (int y = 0; y < bmpScreenCapture.Height; y++)
                {
                    for (int x = 0; x < bmpScreenCapture.Width; x++)
                    {
                        Color c = bmpScreenCapture.GetPixel(x, y);
                        int gray = (int)(0.3 * c.R + 0.59 * c.G + 0.11 * c.B);
                        bmpScreenCapture.SetPixel(x, y, Color.FromArgb(gray, gray, gray));
                    }
                }

                MemoryStream ms = new MemoryStream();
                bmpScreenCapture.Save(ms, ImageFormat.Jpeg);
                byte[] bmpBytes = ms.ToArray();

                // Send back a response.
                udpClient.Send(bmpBytes, bmpBytes.Length, ip);
            }
            udpClient.BeginReceive(new AsyncCallback(ReceiveCallback), null);
        }

        private void send_key(int key, bool press) {
            string message = string.Format("{0},{1}", key.ToString("X"), press ? "0" : "1");
            //Debug.Print("Sending message: " + message);
            // Get the char that corresponds to the key from charToKeyCombo
            string keyChar = charToKeyCombo.FirstOrDefault(x => x.Value == key).Key;
            //Debug.Print("(Which corresponds to: " + keyChar + ")");
            if (voiceboxclient_ip != "")
            {
                // Send this message to the ip specified in voiceboxclient_ip at port 5000 overt UDP
                byte[] bytes = Encoding.ASCII.GetBytes(message);
                // Send the message
                udpClient.Send(bytes, bytes.Length, voiceboxclient_ip, 5000);
            }
        }

        private void processKey(string key)
        {
            if (charToKeyCombo.ContainsKey(key))
            {
                if (charToKeyCombo[key] != 0x00)
                {
                    // Get the key code
                    int keyCode = charToKeyCombo[key];
                    send_key(keyCode, true);
                    send_key(keyCode, false);
                    return;
                }
            }
            char c = key[0];
            if (!charToKeyCombo.ContainsKey(char.ToLower(c).ToString()))
            {
                Debug.Print("Key not found in dict: " + c);
                Debug.Print("(Key as hex: " + ((int)c).ToString("X") + ")");
                return;
            }

            // Check if c is upper case
            bool upper = char.IsUpper(c);
            if (upper) { send_key(charToKeyCombo["leftshift"], true); }

            // Convert c to lower case
            c = char.ToLower(c);
            // Handle the special keys
            if (c == 'ö')
            {
                send_key(charToKeyCombo["rightalt"], true);
                send_key(charToKeyCombo["o"], true);
                send_key(charToKeyCombo["o"], false);
                send_key(charToKeyCombo["rightalt"], false);
            }
            else if (c == 'å')
            {
                send_key(charToKeyCombo["rightalt"], true);
                send_key(charToKeyCombo["a"], true);
                send_key(charToKeyCombo["a"], false);
                send_key(charToKeyCombo["rightalt"], false);
            }
            else if (c == 'ä')
            {
                send_key(charToKeyCombo["rightalt"], true);
                send_key(charToKeyCombo["r"], true);
                send_key(charToKeyCombo["r"], false);
                send_key(charToKeyCombo["rightalt"], false);
            }
            else if (c == '?')
            {
                send_key(charToKeyCombo["leftshift"], true);
                send_key(charToKeyCombo["/"], true);
                send_key(charToKeyCombo["/"], false);
                send_key(charToKeyCombo["leftshift"], false);
            }
            else if (c == '!')
            {
                send_key(charToKeyCombo["leftshift"], true);
                send_key(charToKeyCombo["1"], true);
                send_key(charToKeyCombo["1"], false);
                send_key(charToKeyCombo["leftshift"], false);
            }
            else {
                // Get the key code
                int keyCode = charToKeyCombo[c.ToString()];
                send_key(keyCode, true);
                send_key(keyCode, false);
            }
            if (upper) { send_key(charToKeyCombo["leftshift"], false); }
        }

        private void handle_text_change(string inputText) {
            for (int i = 0; i < inputText.Length; i++)
            {
                char c = inputText[i];
                if (sentText.Length > i)
                {
                    // If the character is the same as the one we sent, skip it
                    if (c == sentText[i])
                    {
                        continue;
                    }
                    // If the character is different, send the backspace key
                    else
                    {
                        // Send backspace to delete everything after the current character from sentText
                        for (int j = sentText.Length; j > i; j--)
                        {
                            processKey("backspace");
                        }
                        sentText = sentText.Substring(0, i);
                        processKey(c.ToString());
                    }
                }
                else {
                    processKey(c.ToString());
                    sentText += c;
                }
            }
        }

        private void unittest_test_handle_text_change()
        {
            Debug.Print("Starting test!");

            Debug.Print("*******************");
            sentText = "";
            handle_text_change("Jag vet komma du är min bästa vän.");
            handle_text_change("Jag vet, du är min bästa vän?");
            Debug.Print("*******************");
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            // If in talon mode, do nothing
            if (talon_mode) { return; }
            string inputText = textBox1.Text;
            handle_text_change(inputText);
        }
    }
}