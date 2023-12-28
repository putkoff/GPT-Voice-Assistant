#!/usr/bin/env python3
import os
import subprocess
import threading
import speech_recognition as sr
from abstract_utilities.read_write_utils import write_to_file, create_and_read_file,read_from_file
from abstract_gui import AbstractWindowManager,sg
windows_mgr = AbstractWindowManager()

"""
This module provides functionalities to capture and manipulate audio input 
from a microphone and save them into a text file. It uses an abstract GUI 
to display the state of audio recording and playback.

The main functions in this script are as follows:
- change_glob: A utility function to update and retrieve global variables dynamically.
- get_globe: A utility function to retrieve the value of a global variable if it exists.
- cmd_it: Executes a shell command using subprocess and returns a Popen object for communication.
- get_output: Retrieves the output of a subprocess Popen object.
- mic_switch: Toggles the microphone state between on and off using the 'amixer set Capture toggle' command.
- parse_mic_state: Parses the microphone state from the output of 'amixer' command.
- get_mic_state: Retrieves the current microphone state.
- win_update: Updates the GUI window with new values for a given key.
- get_cmd_out: Executes a shell command and returns its output.
- get_values: Retrieves a value from the GUI window's stored values using the given key.
- save_voice: Saves the voice recording to a file 'voice.txt' and updates the GUI window accordingly.
- playback: Starts the speech recognition process and updates the GUI window with the recognized text.
- start_recording_threaded: Starts the recording process in a separate thread to avoid blocking the GUI.
- ambient_noise: Adjusts for ambient noise before starting the actual audio recording.
- listen_audio: Listens for audio input and stores it in the global variable 'audio'.
- recognzer: Uses the Google Web Speech API to recognize the audio and store the result in 'voice_value'.
- start_recording: Starts the audio recording process and handles exceptions for KeyboardInterrupt.
- get_gui_layout: Defines the layout for the PySimpleGUI GUI window.
- voice_record_function: Handles different events triggered by the GUI window and performs corresponding actions.
- gui: Initializes the GUI window, sets global variables, and starts the main GUI event loop.
- main: Sets up global variables, initializes the SpeechRecognizer and Microphone objects, and starts the GUI.

To use this script, run it as a Python program. It will open a GUI window with a 'record' button. Clicking on the 'record' button will start the audio recording, and the GUI screen will turn green to indicate recording. Once you stop speaking, the recorded audio will be processed using the Google Web Speech API, and the recognized text will be displayed in the GUI window.

Note: To use this script, make sure to have the required libraries installed, such as PySimpleGUI and SpeechRecognition.

Author: putkoff
Date: 8/1/23
"""
def cmd_it(st):
    return subprocess.Popen(st, stdout=subprocess.PIPE, shell=True)
def get_output(p):
    return p.communicate()
def get_cmd_out(st):
    return get_output(cmd_it(st))
class VoiceRecorder:
    def __init__(self):
        self.Recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.edit_timer  = 0
        self.voice = ''
        self.voice_value = ''
        self.output_display_text_path = 'output_display_text.txt'
        self.un_processed_text_path = 'un_processed_text.txt'
        self.edited_text_path = 'edited_text.txt'
        self.silence_kill = False
        self.recording = False
        self.edited=False
        self.recording_lock = threading.Lock()
        write_to_file(file_path = self.output_display_text_path,contents='')
        write_to_file(file_path = self.un_processed_text_path,contents='')
        self.window_name = windows_mgr.add_window(title='speech_to_text_window', layout=self.get_layout(), event_handlers=self.voice_record_function, exit_events=['Quit',"-SUBMIT-"],timeout=1000)
        windows_mgr.while_window()
    def start_recording_threaded(self):
        if not self.recording:
            self.recording = True
            threading.Thread(target=self.start_recording).start()
        else:
            print("Recording is already in progress.")
    def mic_switch(self):
        return str(get_cmd_out("amixer set Capture toggle")[0])
    def parse_mic_state(self,st:str):
        return str(st).split('[')[-1].split(']')[0]
    def get_mic_state(self):
        return self.parse_mic_state(get_cmd_out("amixer"))
    def get_layout(self):
        return [[sg.Multiline('', key='-OUTPUT-', size=(50, 20),enable_events=True)],[[sg.Button(button_text='record', key='-RECORD_BUTTON-',visible=True,enable_events=True,button_color='green'), sg.Button('STOP',key='-STOP_RECORDING-',visible=False, enable_events=True),sg.Button("-SUBMIT-")],sg.Text('when the screen turns green, speak',key='-SCREEN_TEXT-')]]
    def ambient_noise(self):
        self.Recognizer.adjust_for_ambient_noise(self.source)
        self.window['-SCREEN_TEXT-'].update(value="Callibrating...\nSet minimum energy threshold to {}".format(self.Recognizer.energy_threshold))
    def update_output_display(self):
        contents = read_from_file(self.output_display_text_path) + '\n' +read_from_file(self.un_processed_text_path)
        self.window['-OUTPUT-'].update(value=contents)
        return contents
    def save_voice(self):
        contents=self.update_output_display()

        write_to_file(file_path=self.output_display_text_path, contents=contents)
        write_to_file(file_path=self.un_processed_text_path, contents='')
    def start_recording(self):
        with self.recording_lock:
            if self.recording:
                try:
                    with self.microphone as source:
                        self.source=source
                        self.ambient_noise()
                        while self.recording:  # Loop will continue while recording flag is True
                            self.window.Element('-OUTPUT-').Update(background_color='green')
                            self.listen_audio()
                            try:
                                self.playback()
                            except LookupError:
                                print("Oops! Didn't catch that")
                            if not self.recording:
                                break
                        return 
                except KeyboardInterrupt:
                    pass
                finally:
                    self.recording = False  # Reset recording flag at the end
            else:
                print("Recording was stopped before it could start.")

    def listen_audio(self):
        self.window['-SCREEN_TEXT-'].update(value="Say something!")
        self.audio=None  # Initialize audio as None
        while not self.audio:  # Loop until audio is received or recording is stopped
            try:
                self.audio = self.Recognizer.listen(self.source, timeout=5)  # Increase timeout if needed
            except sr.WaitTimeoutError:
                if not self.recording:  # If recording has been stopped, break the loop
                    self.silence_kill=True
                    break
    def playback(self):
        # instead of updating the GUI directly, put a custom event in the event queue
        self.window["-SCREEN_TEXT-"].update(value="processing audio to text")
        self.voice_value=self.recognizer()
        if self.voice_value:
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                self.voice=u"{}".format(self.voice_value).encode("utf-8")
            else:  # this version of Python uses unicode for strings (Python 3+)
                self.voice="{}".format(self.voice_value)
            write_to_file(file_path=self.un_processed_text_path, contents=read_from_file(self.un_processed_text_path)+self.voice)
            self.save_voice()
    def recognizer(self):
        
        try:
            self.voice_value=self.voice_value=self.Recognizer.recognize_google(self.audio)
        except:
            self.window['-SCREEN_TEXT-'].update(value="looks like we didnt catch that, could you please repeat it?")
            self.voice_value=None
        return self.voice_value
    def start_recording_threaded(self):
        threading.Thread(target=self.start_recording).start()
    def edit_voice(self):
        write_to_file(file_path=self.output_display_text_path, contents=self.values['-OUTPUT-'])
    def record_button(self):
        self.recording = True
        self.window.Element('-RECORD_BUTTON-').Update(text='RECORDING',button_color='red')
        self.mic_switch()
        self.update_output_display()
        self.start_recording_threaded()
    def stop_record(self):
        self.recording=False
        self.window.Element('-OUTPUT-').Update(background_color='white')  # Change color back
        self.mic_switch()
        self.update_output_display()
        self.window.Element('-RECORD_BUTTON-').Update(text='record',button_color='green')
    def record_hit(self,bool_it):
        if (self.get_mic_state() == 'off' and bool_it) or (self.get_mic_state() == 'on' and not bool_it):
            self.mic_switch()
    def mic_switch(self):
        return str(get_cmd_out("amixer set Capture toggle")[0])
    def voice_record_function(self,event,values,window):
        print(window['-RECORD_BUTTON-'].ButtonText)
        self.event,self.values,self.window = event,values,window
        if event == '-UPDATE_SCREEN_TEXT-':
            # now you can safely update the GUI
            window['-SCREEN_TEXT-'].update(value=values[event])
        if event == '-RECORD_BUTTON-':
            if self.recording:
                self.stop_record()
            else:
                self.record_button()
        if event == '-STOP_RECORDING-':
            self.stop_record()
        if event == '-CLEAR_TEXT-':
            self.clear_voice()
        if event == '-OUTPUT-':
            self.edit_voice()
        if self.silence_kill == True:
            self.silence_kill=False
            self.stop_record()
            self.recording = True
            self.record_button()
        if event == "-SUBMIT-":
            self.voice = values['-OUTPUT-']
            return   

VoiceRecorder()
