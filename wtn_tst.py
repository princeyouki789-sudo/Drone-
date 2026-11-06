# Comprehensive dictionary for number parsing (0-9, teens, tens)
import os
import sys
import queue
import json
import re
import time
import pyaudio
from djitellopy import Tello
from vosk import Model, KaldiRecognizer

# Dictionary to map spoken number words to integers
ONES = {str(i): i for i in range(10)}
TEENS = {"eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
HUNDRED_MULTIPLIERS = {str(i): i * 100 for i in range(1, 10)}
THOUSAND = 1000

def parse_number_from_words(words):
  
    if not words: return None
    total, current_group = 0, []
    for word in words:
        word = word.lower()
        if word in ONES: current_group.append(ONES[word])
        elif word in TEENS: current_group.append(TEENS[word])
        elif word in TENS:
            if current_group and isinstance(current_group[-1], int) < 20: current_group[-1] += TENS[word]
            else: current_group.append(TENS[word])
        elif word in HUNDRED_MULTIPLIERS:
            if current_group: total += sum(current_group); current_group = []
            total += HUNDRED_MULTIPLIERS[word]
        elif word == "thousand":
            if current_group: total += sum(current_group) * THOUSAND; current_group = []
    if current_group: total += sum(current_group)
    return total if total > 0 else None


def extract_distance(command_text, default=30):
    """
    Scans the spoken sentence for digits (like '50') or words (like 'forty').
    Ensures the value fits inside the safe Tello SDK limits (20cm to 10000cm).
    """
    # 1. Check for raw numeric digits first (e.g., "50")
    digits = re.findall(r'\d+', command_text)
    if digits:
        val = int(digits[0])
        return max(1, min(val, 10000)) # Clamp between safety boundaries
        
    # 2. Check for spoken English words (e.g., "forty")
    words = command_text.split()
    number_value = parse_number_from_words(words)
    if number_value is not None:
        return max(1, min(number_value, 10000)) # Clamp between safety boundaries


def execute_flexible_movement(command):
    """Parses sentences dynamically to extract direction and distance."""
    # Handle absolute base states first
    if "take off" in command or "takeoff"  or "start" in command:
        print("🛫 Executing: Takeoff")

    

def other_commands(command): 
    distance = extract_distance(command, default=30)
    # Match direction keywords anywhere inside the custom sentence
    if "forward" in command:
        print(f"➡️ Action: Moving Forward by {distance} cm")
  
        
    elif "back" in command or "backward" in command:
        print(f"⬅️ Action: Moving Backward by {distance} cm")

        
    elif "up" in command or "climb" in command:
        print(f"⬆️ Action: Moving Up by {distance} cm")
  
        
    elif "down" in command or "descend" in command:
        print(f"⬇️ Action: Moving Down by {distance} cm")

        
    elif "left" in command:
        print(f"👈 Action: Moving Left by {distance} cm")

        
    elif "right" in command:
        print(f"👉 Action: Moving Right by {distance} cm")
  
        


# --- System Initialization ---


MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: '{MODEL_PATH}' folder missing.")
    sys.exit(1)

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, 
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
                execute_flexible_movement(raw_command)

except KeyboardInterrupt:
    print("\n🛑 Shutting down.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

