import os
import sys
import queue
import json
import pyaudiowpatch
from vosk import Model, KaldiRecognizer

# 1. Verify the model folder exists locally
MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: The '{MODEL_PATH}' folder was not found in this directory.")
    print("Please make sure you downloaded and renamed the Vosk folder correctly.")
    sys.exit(1)

print("📦 Loading local Vosk language model (this may take a few seconds)...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# 2. Thread-safe queue to hold audio data chunks
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    """This function is called by PyAudio whenever the mic records sound."""
    audio_queue.put(in_data)
    return (None, pyaudiowpatch.paContinue)

# 3. Initialize PyAudio and open the mic stream
p = pyaudiowpatch.PyAudio()

try:
    stream = p.open(
        format=pyaudiowpatch.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000,  # Smaller buffer = lower delay
        stream_callback=audio_callback
    )
except Exception as e:
    print(f"❌ Error opening microphone: {e}")
    print("Verify your microphone is plugged in and terminal has mic permissions.")
    p.terminate()
    sys.exit(1)

# 4. Start listening
stream.start_stream()
print("\n" + "="*40)
print("🤖 OFFLINE VOICE TEST READY!")
print("Speak into your microphone now...")
print("Press Ctrl+C in the terminal to stop.")
print("="*40 + "\n")

try:
    while True:
        # Pull audio chunk from the queue
        data = audio_queue.get()
        
        # Feed data to the recognizer
        if recognizer.AcceptWaveform(data):
            # When a phrase ends/pauses, print the final result
            result_json = json.loads(recognizer.Result())
            text = result_json.get("text", "")
            if text:
                print(f"🗣️ Final Sentence: {text}")
        else:
            # Optional: Print partial words as you say them for real-time feedback
            partial_json = json.loads(recognizer.PartialResult())
            partial_text = partial_json.get("partial", "")
            if partial_text:
                print(f"🎙️ Hearing: {partial_text}...", end="\r")

except KeyboardInterrupt:
    print("\n\n🛑 Stopping audio stream and closing test...")
    
finally:
    # 5. Clean cleanup of audio hardware
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("👋 Test closed safely.")
