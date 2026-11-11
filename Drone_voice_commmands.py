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
    wtn = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "one hundred": 100,
            "one hundred and ten": 110, "one hundred and twenty": 120, "one hundred and thirty": 130, "one hundred and forty": 140, 
            "one hundred and fifty": 150, "one hundred and sixty": 160, "one hundred and seventy": 170, "one hundred and eighty": 180,
            "one hundred and ninety": 190, "two hundred": 200, "two hundred and ten": 210, "two hundred and twenty": 220,
            "two hundred and thirty": 230, "two hundred and forty": 240, "two hundred and fifty": 250, "two hundred and sixty": 260,
            "two hundred and seventy": 270, "two hundred and eighty": 280, "two hundred and ninety": 290, "three hundred": 300, 
            "three hundred and ten": 310, "three hundred and twenty": 320,
            "three hundred and thirty": 330, "three hundred and forty": 340, "three hundred and fifty": 350, "three hundred and sixty": 360,
            "three hundred and seventy": 370, "three hundred and eighty": 380, "three hundred and ninety": 390, "four hundred": 400,
            "four hundred and ten": 410, "four hundred and twenty": 420, "four hundred and thirty": 430, "four hundred and forty": 440,
            "four hundred and fifty": 450, "four hundred and sixty": 460, "four hundred and seventy": 470, "four hundred and eighty": 480,
            "four hundred and ninety": 490, "five hundred": 500}

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
    elif "rotate clockwise" in text or "turn right" in text:
        drone.rotate_clockwise(90)
        print("Rotating clockwise 90 degrees")
    elif "rotate counterclockwise" in text or "turn left" in text:
        drone.rotate_counter_clockwise(90)
        print("Rotating counterclockwise 90 degrees")
    elif "flip forward" in text:
        drone.flip_forward()
        print("Flipping forward")
    elif "flip back" in text:
        drone.flip_back()
        print("Flipping back")
    elif "flip left" in text:
        drone.flip_left()
        print("Flipping left")
    elif "flip right" in text:
        drone.flip_right()
        print("Flipping right")
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




