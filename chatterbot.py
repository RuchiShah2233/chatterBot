import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI

with st.sidebar:
    st.write("Enter your OpenAI API key here.")
    API_KEY = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

def transcribe_text_to_voice(audio_location):
    client = OpenAI(api_key=API_KEY)
    audio_file = open(audio_location, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def chat_completion_call(text):
    client = OpenAI(api_key=API_KEY)
    messages = [ {"role": "system", "content": "You are a helpful assistant."},
        {"role" : "system", "content": "You are an intelligent assistant."},
        {"role" : "system", "content": "My name is Chatterbot."},
        {"role" : "system", "content": "I was created by Ruchi Shah."},
        {"role": "user", "content": text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content

def text_to_speech_ai(speech_file_path, api_response):
    client = OpenAI(api_key=API_KEY)
    response = client.audio.speech.create(model="tts-1", voice="nova", input=api_response)
    response.stream_to_file(speech_file_path)

st.title("ChatterBot :robot_face:")

# Add a text input box for user input
"""
Type or just click on the voice recorder and let me know how can I help you?
"""
user_input = st.text_input("Type your message here:", "")

audio_bytes = audio_recorder()
if audio_bytes:
    # Save the Recorded File
    audio_location = "audio_file.wav"
    with open(audio_location, "wb") as f:
        f.write(audio_bytes)

    # Transcribe the saved file to text
    if user_input:
        text = user_input
    else:
        text = transcribe_text_to_voice(audio_location)

    st.write("You:", text)

    # Use API to get an AI response
    api_response = chat_completion_call(text)
    st.write("ChatterBot:", api_response)

    # Read out the text response using TTS
    speech_file_path = 'audio_response.mp3'
    text_to_speech_ai(speech_file_path, api_response)
    st.audio(speech_file_path)
