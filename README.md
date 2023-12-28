# README for GPT-Voice-Assistant by Putkoff

## Overview
GPT-Voice-Assistant is a Python-based tool that facilitates speech-to-text functionality, converting spoken words into written text using a microphone. This tool is designed to be easy to use and integrates various Python libraries to handle voice recognition and GUI management.

## Features
- **Speech-to-Text Conversion:** Converts spoken language into text using Google's speech recognition service.
- **GUI Interface:** Provides a user-friendly graphical interface for interaction.
- **Real-time Voice Transcription:** Transcribes voice in real-time as you speak.
- **Editable Transcribed Text:** Allows users to edit the transcribed text within the application.

![image](https://github.com/putkoff/GPT-Voice-Assistant/blob/main/documentation/speech_to_text.png)

## Installation Requirements
Before running the GPT-Voice-Assistant, ensure that the following dependencies are installed on your system:

### System Requirements
- Linux Operating System (Recommended: Ubuntu or Debian-based distributions)

### Python Dependencies
1. PyAudio: For microphone access
    ```bash
    sudo apt install python3-pyaudio
    ```

2. SpeechRecognition: For converting spoken words into text
    ```bash
    pip install SpeechRecognition --break-system-packages
    ```

3. Abstract Utilities: For file read/write operations
    ```bash
    pip install abstract_utilities --break-system-packages
    ```

4. Abstract GUI: For the graphical user interface
    ```bash
    pip install abstract_gui --break-system-packages
    ```

## Usage
After installing the necessary dependencies, run the `GPT-Voice-Assistant.py` script. A window will appear with the following components:

- A **record button** to start voice recording.
- A **stop button** to end the recording session.
- A **text area** where the transcribed text will be displayed.
- An **edit option** to modify the transcribed text.

## How to Use
1. **Start the Application:** Run the script to open the GUI.
2. **Start Recording:** Click the 'record' button to begin recording your speech.
3. **Stop Recording:** Click the 'stop' button to end the recording session.
4. **Edit Text:** The transcribed text can be edited directly in the text area.
5. **Save Changes:** Edited text will be saved automatically.

## Troubleshooting
- Ensure that your microphone is properly configured and working.
- Check if all dependencies are correctly installed.
- Make sure you have an active internet connection, as Google's speech recognition service is used.

## Contributions
Contributions to the GPT-Voice-Assistant are welcome. Please submit your contributions as pull requests on GitHub.

## License
The GPT-Voice-Assistant is released under the [MIT License](https://opensource.org/licenses/MIT).

## Contact
For any queries or suggestions, please contact the author, Putkoff, through the GitHub repository.

---
**Note:** This README is intended to provide a basic understanding of the GPT-Voice-Assistant tool. For more detailed information or specific use cases, refer to the tool's documentation or contact the author.
