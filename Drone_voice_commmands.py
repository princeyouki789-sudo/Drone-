import pyaudio
import json
import sys
from vosk import Model, KaldiRecognizer
from djitellopy import Tello

model = Model(r"C:\Users\mbata\Drone-\model")
recognizer = KaldiRecognizer(model, 16000)

drone = Tello()
try:
    drone.connect()
    print(f"Battery: {drone.get_battery()}%")
except Exception as e:
    print(f"Connection Failed: {e}")
    sys.exit(1)

def distance(spoken_text):
# word to number Dictionary
    wtn = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100}
    words = spoken_text.split()
    for word in words:
        if word in wtn:
            return wtn[word]
    return None

def voice_commands(drone,text):
    text = text.lower()
    if "take off" in text:
        print("Taking off")
        drone.takeoff()

    elif "land" in text:
        print("Landing")
        drone.land()

    dist = distance(text) or 30
    if "forward" in text:
        print(f"Moving forward {dist} cm")
        drone.move_forward(dist)

    elif "back" in text or "backward" in text:
        print(f"Moving backward {dist} cm")
        drone.move_backward(dist)
    elif "up" in text or "climb" in text:
        print(f"Moving up {dist} cm")
        drone.move_up(dist)
    elif "down" in text or "descend" in text:
        print(f"Moving down {dist} cm")
        drone.move_down(dist)
    elif "left" in text:
        print(f"Moving left {dist} cm")
        drone.move_left(dist)
    elif "right" in text:
        print(f"Moving right {dist} cm")
        drone.move_right(dist)
    else:
        print("Command not recognized.")

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)

while True:
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            spoken_text = (result.get("text", ""))
            print(spoken_text)
            if spoken_text:
                voice_commands(drone, spoken_text)
    except KeyboardInterrupt:
        print("\nStopping...")
        drone.land()
        break




