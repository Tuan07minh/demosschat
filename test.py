from flask import Flask, render_template, request
import requests
import json
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

url = "https://backend.chatfly.co/api/chat/get-streaming-response?enable_response_message_id=true"
headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0dWFubmd1emVuQGdtYWlsLmNvbSIsImV4cCI6MTcxMDY4MjIwNH0.7-fop-4oPU3s_iOSIWuJogDN4_C-1bvkeNiYj0XsqBw",
    "content-type": "application/json",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://app.chatfly.co/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def ask_question_and_get_response(question):
    data = json.dumps({
        "bot_id": "800dc23b-ea87-4c3c-b35a-ef8999bf4ff4",
        "message": question,
        "session_id": "54a00bdd-a133-8ef1-50f1-df56188eaa27"
    })

    response = requests.post(url=url, headers=headers, data=data)
    return response.text
def remove_id_flag(response):
    words = response.split()
    filtered_words = [word for word in words if '<<id-flag>>' not in word]
    cleaned_response = ' '.join(filtered_words)
    return cleaned_response

def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    os.system("mpg321 " + filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response = ask_question_and_get_response(message)
    text_to_speech(response)
    return response

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        response = ask_question_and_get_response(text)
        text_to_speech(response)
        return response
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)
if __name__ == '__main__':
    app.run(debug=True)
