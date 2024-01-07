import streamlit as st
from gtts import gTTS
import time
import os
import speech_recognition as sr
import playsound
from pydub import AudioSegment
from pydub.playback import play
import json

json_data = []
with open('data.json', 'r') as file:
    json_data = json.load(file)

def read_aloud(question, idx):
    tts = gTTS(question, lang='en')
    tts.save(f"question{idx}.mp3")
    # st.audio('question.mp3', format='audio/mp3')
    # playsound.playsound("question.mp3")
    audio = AudioSegment.from_file(f"question{idx}.mp3")
    play(audio)
    # os.remove(f"question{idx}.mp3")

def collect_response():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.warning("Speak your answer now...")
        audio_data = recognizer.listen(source, timeout=5)

    try:
        response = recognizer.recognize_google(audio_data)
        st.success(f"You said: {response}")
        return response
    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand your response.")
        return None
    except sr.WaitTimeoutError:
        print("No speech detected within 5 seconds.")
        return None

def main():
    st.title("AI Interviewer")

    responses = []

    for idx, qa_pair in enumerate(json_data):
        question = qa_pair["question"]
        st.header(f"Question {idx + 1}")
        st.write(question)

        read_aloud(question, idx)

        response = collect_response()
        responses.append(response)
        
    st.title("Responses")
    for idx, response in enumerate(responses):
        st.write(f"Question {idx + 1}: {response}")

if __name__ == "__main__":
    main()
