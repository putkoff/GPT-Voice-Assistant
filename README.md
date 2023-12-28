# GPT-Voice-Assistant
This repository contains a Python-based voice assistant that can transcribe your speech to text in real-time using the SpeechRecognition library. The GUI is built using PySimpleGUI.

## Getting Started

### Prerequisites

To install the required dependencies, run the following command:

pip install -r requirements.txt
Certainly, I'd be happy to help! Here are your README, requirements.txt, and a suggested repository structure. 

**README.md**
```markdown
# Voice Assistant

This repository contains a Python-based voice assistant that can transcribe your speech to text in real-time using the SpeechRecognition library. The GUI is built using PySimpleGUI.

## Getting Started

### Prerequisites

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Running the script

To run the assistant, execute the following command:

```bash
python3 main.py
```

## Features

- Real-time speech transcription
- Ambient noise calibration
- Interactive GUI

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

**requirements.txt**
```
sudo apt install python3-pyaudio
pip install SpeechRecognition --break-system-packages
pip install abstract_utilities --break-system-packages
pip install abstract_gui --break-system-packages
```

Repository structure:

```
|--- main.py (your script here)
|--- functions.py (your functions module)
|--- envy_it.py (your envy_it module)
|--- README.md (description and instructions)
|--- requirements.txt (list of dependencies)
|--- LICENSE (license details, if any)
|--- .env (environmental variables, if any)
```


### function descriptions:
change_glob(x, y): This function changes the value of the global variable named 'x' to the value 'y' and returns 'y'.

get_globe(x): Returns the global variable named 'x'. If 'x' doesn't exist in the global namespace, it returns an empty string.

cmd_it(st): Executes the command 'st' in the shell and returns a subprocess.Popen object.

get_output(p): Communicates with the process 'p' (a subprocess.Popen object) and returns its output.

mic_switch(): Toggles the microphone capture on/off.

get_cmd_out(st): Executes the command 'st' in the shell and returns its output.

parse_mic_state(st: str): Parses the string 'st' to find the current microphone state (on/off). It assumes the state is mentioned inside the last pair of square brackets.

get_mic_state(): Executes the 'amixer' command in the shell to get the microphone state and returns it.

win_update(win=get_globe('window'), st:str='-OUTPUT-', data:str =reader_make(filepath='voice.txt') + '\n' + get_globe('voice')): Updates the 'st' element of the window 'win' with 'data'.

get_values(st): Returns the 'st' value from the global 'values' dictionary. If 'st' doesn't exist in the dictionary, it returns None.

save_voice(voice): Appends the voice transcript 'voice' to the 'voice.txt' file and updates the '-OUTPUT-' element of the GUI with the new transcript.

playback(): Processes the audio to text and saves it.

start_recording_threaded(): Starts the recording in a separate thread.

ambient_noise(): Adjusts the recognizer for ambient noise.

listen_audio(): Listens to audio until it gets an input or until recording is stopped.

recognizer(): Recognizes the speech in the audio and returns it.

start_recording(): Starts the recording, adjusts for ambient noise, listens to audio, and processes it.

stop_record(window=get_globe('window')): Stops the recording and updates the GUI accordingly.

gui(): Creates and handles the GUI.

main(): The entry point of the application, which initializes some global variables and starts the GUI.

The use case of this script is to create a voice assistant that listens to your speech, transcribes it into text in real time, and displays it in the GUI. You can start and stop the recording using buttons in the GUI. It also has an ambient noise calibration feature that helps to improve the accuracy of the speech recognition in noisy environments.
