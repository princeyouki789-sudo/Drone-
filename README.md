# Aero Voice

### A Voice-Controlled Tello EDU Drone

<img width="1080" height="603" alt="Screenshot_20261114_222801_Instagram" src="https://github.com/user-attachments/assets/d8573673-8025-4397-bf7f-60cc2f565c7b" />

---

## Meet the Team

### Chelsea Marin

**Creative Director**

- Came up with the original idea for the project: giving our club-issued drone the ability to be controlled using voice commands.
- Helped shape the concept and the creative direction of Aero Voice from the start.

### Price Youki

**Head Coder**

- Led the coding for the project, working on turning spoken instructions into commands the drone can understand and execute.
- Studied the drone's library and the voice model's library to learn how to connect voice control to real flight behaviour.

### Tibo Mba

**Co-Coder**

- Contributed to the coding alongside the head coder, helping build, test, and fix the project as it came together.
- Helped work through the code breaks and errors that came up during development.

**Together:** We combined creative direction and programming to build one complete system — a drone that listens, understands, and flies — while learning how to teach ourselves entirely new coding libraries along the way.

---

## Project Description

Aero Voice is a voice-controlled drone project that transforms vocal instructions into real-time flight instructions that the Tello EDU drone can execute.

Instead of flying with a standard joystick or controller, the pilot speaks — and the drone responds. By bypassing standard joysticks, Aero Voice gives a glimpse into a future of natural, hands-free human-computer interaction, where talking to a device is enough to make it move.

We did not stop at voice control. After getting the drone flying on voice commands, we felt the project was not great enough yet, so we also added facial recognition to the drone's camera feed — giving the drone a way to not only hear its pilot, but see who is in front of it as well.

### Features

- **Voice-Controlled Flight:** The drone is controlled entirely by vocal instructions, with no joystick required.
- **Fine Flight Controls:** We implemented many voice commands to give the pilot finer, more precise control over the drone.
- **Real-Time Response:** Spoken instructions are translated into flight instructions the Tello EDU can execute in real time.
- **Facial Recognition:** The drone's camera feed can recognise faces, adding a second, visual way for the drone to respond to people.
- **Hands-Free Interaction:** Bypassing standard controllers makes flying feel more natural and points toward more accessible ways of interacting with technology.

### How It Works

Aero Voice connects three things that do not normally talk to each other — a person's voice, a voice recognition model, and a drone — through code we wrote ourselves:

1. **The Pilot Speaks:** The pilot gives a vocal instruction out loud, instead of pushing a joystick or pressing a button.
2. **The Voice Model Listens:** The spoken instruction is recognised and passed into our Python code.
3. **Python Translates the Command:** Our code converts the recognised instruction into a flight command the drone understands.
4. **The Tello EDU Flies:** The drone receives the command and executes it in real time — moving as instructed.
5. **The Camera Adds Vision:** At the same time, the drone's camera feed is used for facial recognition, so the system can detect faces while it flies.

**System Loop:**

> Spoken Command → Voice Recognition → Python Translates the Instruction → Tello EDU Receives the Command → Drone Flies → Ready for the Next Command

The program keeps listening, so each new vocal instruction can trigger the next movement.

### What's in This Repository

| File | What It Does |
| --- | --- |
| `Drone_combined_Final_Version.py` | The combined, final version of the project, bringing the pieces together into one complete program. |
| `Drone_voice_commmands.py` | The voice-command implementation — the code that handles the spoken instructions for controlling the drone. |
| `drone_human_dronelibray_test.py` | Our test code for detecting people / recognising faces in the drone's camera feed. |

### What Users Gain From It

On a broader scale, Aero Voice demonstrates how natural human communication can be used to interact with technology, without having to physically hold a controller.

Speaking is one of the most natural things people do. Turning that into flight control makes the experience feel more intuitive, and it offers a glimpse of how hands-free interaction could make technology easier to use in the future — including in situations where a traditional joystick or controller is not practical.

More than anything, Aero Voice shows what a small team with little coding experience can build by learning as they go.

---

## Our Experience

### Inspiration

Our creative director, Chelsea, came up with the great idea of having our club-issued drone have the ability to be controlled using voice commands.

Since our team is made up of people with little to no coding experience, we decided the project was the right amount of difficulty for us: challenging enough to teach us a lot, but achievable enough that we could actually get a drone flying on voice commands by the end of it.

### Challenges We Faced

There were not many major difficulties we had to face — and the ones we did face were mostly our own code breaks.

Most problems were errors on our part: code that did not work the way we expected, until we figured out what we had written wrong. Once we wrote the code right, everything just sort of worked.

The real challenge underneath those errors was that almost everything in this project was new to us. The drone, the voice model, and their libraries all had to be learned from scratch before we could even tell whether an error was in our code, or in how we were using a library.

### What We Learned

The biggest and most important thing we learned from this project is how to teach ourselves new coding libraries.

Studying the drone's library and the voice model's library was a huge experience boost in learning how development is done for different devices. It was very helpful — not just for this drone, but for any future project where we have to pick up a new device, a new library, and figure it out on our own.

That skill mattered even after the voice control worked. It is what allowed us to push the project further and add facial recognition to the drone's camera feed, instead of stopping at our first working version.

### Team Collaboration

We divided the project by the parts each of us did best.

Chelsea directed the idea and the creative side of the project, Price led the coding, and Tibo co-coded — building and testing alongside him. Together, we had to make sure the voice model, the code, and the drone were all communicating correctly, because none of those pieces mean much on their own.

Voice control only works when every part of that chain works together, so testing, breaking, fixing, and testing again was a team effort from start to finish.

---

## Final Presentation

[View Our Final Presentation](https://canva.link/4inbfmzo6ego0pf)

---

## Future Improvements

Although we successfully demonstrated voice-controlled flight and facial recognition, there are several things we could explore if we continue developing Aero Voice:

- Expanding the set of voice commands for even finer flight control.
- Improving how reliably spoken commands are recognised in different environments.
- Developing the facial recognition in the camera feed further.
- Exploring other natural, hands-free ways of interacting with the drone.

---

*Aero Voice is an experimental proof of concept exploring the connection between voice, computer vision, and accessible hands-free technology.*
