import os
import sys
import queue
import json
import re
import time
import pyaudiowpatch
from djitellopy import Tello
from vosk import Model, KaldiRecognizer

# Dictionary to map spoken number words to integers
WORD_TO_NUM = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, 
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100
}

def extract_distance(command_text, default=30):
    """
    Scans the spoken sentence for digits (like '50') or words (like 'forty').
    Ensures the value fits inside the safe Tello SDK limits (20cm to 500cm).
    """
    # 1. Check for raw numeric digits first (e.g., "50")
    digits = re.findall(r'\d+', command_text)
    if digits:
        val = int(digits[0])
        return max(20, min(val, 500)) # Clamp between safety boundaries
        
    # 2. Check for spoken English words (e.g., "forty")
    words = command_text.split()
    for word in words:
        if word in WORD_TO_NUM:
            return WORD_TO_NUM[word]
            
    return default

def execute_flexible_movement(drone, command):
    """Parses sentences dynamically to extract direction and distance."""
    # Handle absolute base states first
    if "take off" in command or "takeoff"  or "start" in command:
        print("🛫 Executing: Takeoff")
        drone.takeoff()
    elif "land" in command or "stop" in command:
        print("🛬 Executing: Landing Sequence")
        drone.land()
    

def other_commands(command): 
    distance = extract_distance(command, default=30)
    # Match direction keywords anywhere inside the custom sentence
    if "forward" in command:
        print(f"➡️ Action: Moving Forward by {distance} cm")
        drone.move_forward(distance)
        
    elif "back" in command or "backward" in command:
        print(f"⬅️ Action: Moving Backward by {distance} cm")
        drone.move_backward(distance)
        
    elif "up" in command or "climb" in command:
        print(f"⬆️ Action: Moving Up by {distance} cm")
        drone.move_up(distance)
        
    elif "down" in command or "descend" in command:
        print(f"⬇️ Action: Moving Down by {distance} cm")
        drone.move_down(distance)
        
    elif "left" in command:
        print(f"👈 Action: Moving Left by {distance} cm")
        drone.move_left(distance)
        
    elif "right" in command:
        print(f"👉 Action: Moving Right by {distance} cm")
        drone.move_right(distance)
        
    elif "circle" in command:
        print(f"🔄 Action: Custom Routine - Circle layout")
        drone.send_rc_control(50, 0, 0, 40)
        time.sleep(5)
        drone.send_rc_control(0, 0, 0, 0)
    else:
        print("🤔 Sentence detected but no matching drone macro found.")

# --- System Initialization ---
print("🛸 Connecting to Tello EDU...")
drone = Tello()
try:
    drone.connect()
    print(f"🔋 Battery: {drone.get_battery()}%")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit(1)

MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: '{MODEL_PATH}' folder missing.")
    sys.exit(1)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudiowpatch.paContinue)

p = pyaudiowpatch.PyAudio()
stream = p.open(format=pyaudiowpatch.paInt16, channels=1, rate=16000, input=True, 
               frames_per_buffer=4000, stream_callback=audio_callback)
stream.start_stream()

print("\n" + "="*60)
print("🤖 FLEXIBLE VOICE PARSER ACTIVE!")
print("Try saying phrases like:")
print(" - 'Hey drone please move forward 50 centimeters'")
print(" - 'Can you climb up forty cm right now'")
print(" - 'execute land command'")
print("="*60 + "\n")

try:
    while True:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            raw_command = result.get("text", "").lower()
            
            if raw_command:
                print(f"\n🗣️ Heard Sentence: '{raw_command}'")
                execute_flexible_movement(drone, raw_command)

except KeyboardInterrupt:
    print("\n🛑 Shutting down.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    try:
        drone.land()
    except:
        pass
