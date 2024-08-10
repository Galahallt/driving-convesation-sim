from pathlib import Path
from openai import OpenAI
import winsound

from playsound import playsound

import speech_recognition as sr
import openai

import keyboard
import os
from os import path
import datetime

done = False
context = "Limit your response to two sentences. Less is better. You are trying to keep a driver awake. "
speech_file_path = str(Path(__file__).parent / "audioclips" / "speech.mp3")
mund_file_path = path.relpath(f"./logs/conversation_logs_{str(datetime.datetime.now()).replace(" ", "_").replace(":", ";").replace(".", ",")}_mundane.csv")
game_file_path = path.relpath(f"./logs/conversation_logs_{str(datetime.datetime.now()).replace(" ", "_").replace(":", ";").replace(".", ",")}_game-aided.csv")
style = 2
file = ''

def execute():
    global done
    print('end loop')
    done = True

def get_response(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response.choices[0].message.content
    print(ChatGPT_reply)
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

def get_audio(response):
    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=response,
    ) as response:
        response.stream_to_file(speech_file_path)
    playsound(speech_file_path)
    os.remove(speech_file_path)


def log(name, msg):
    global file

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file.write(f"{timestamp},{name},{msg.replace(',', ';')}\n")

#Initializing pyttsx3
def main():
    global keyword, name, file
    keyboard.add_hotkey("shift+a", execute)
    listening = True
    
    openai.api_key = r"sk-proj-EyMOcap0NWbY2Ln65TzET3BlbkFJeVNcSlhVUxqpTHoH29jV"

    global style, context, game_file_path, mund_file_path
    
    if style == 1:
        file = open(game_file_path, "w")
    elif style == 2:
        file = open(mund_file_path, "w")


    init_msg = ""
    end_msg = ""
    
    if style == 1:
        init_msg = "let's do some trivia to get you awake"
        end_msg = "Thank you for playing, I'll alert you again if you get sleepy"
    elif style == 2:
        init_msg = "let's talk"
        end_msg = "I enjoyed our conversation, I'll talk again when you get sleepy"

    if style == 1:
        messages = [
                        {
                            "role": "system", 
                            "content": f"You are a game show host for trivia questions. {context}"
                        }
                    ]
    elif style == 2:
        messages = [
                        {
                            "role": "system", 
                            "content": f"Act like a close friend and ask about my day, personality, hobbies, and more. {context}"
                        }
                    ]
    
    input("Press Enter to to start...")

    get_audio(f'You\'re looking sleepy, {init_msg}. When you hear this, ')
    winsound.Beep(400, 600)
    get_audio("it means I'm listening.")
    log("Bot",f"You\'re looking sleepy.. {init_msg}")


    if style == 1:
        response_from_openai, messages = get_response('I\'m ready, ask me a question.', messages)
    elif style == 2:
        response_from_openai, messages = get_response('Ask me anything that you would like to know about me.', messages)

    get_audio(response_from_openai)

    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 1000

    global done
    while listening:

        if done:
            get_audio(end_msg)
            break

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 1000
            try:
                if done:
                    get_audio(end_msg)
                    break

                print("Listening...")
                winsound.Beep(400, 600)
                audio = recognizer.listen(source, timeout=2.0)

                if done:
                    get_audio(end_msg)
                    break

                response = recognizer.recognize_google(audio)
                print(response)
                log("User", response)
                    
                response_from_openai, messages = get_response(response, messages)
                if response_from_openai.find("HTTP") == -1:
                    log("Bot", response_from_openai)                 
                get_audio(response_from_openai)
            
            except sr.UnknownValueError:
                print('Sorry I did not hear you properly. Can you repeat that?')
                get_audio('Sorry I did not hear you properly. Can you repeat that?')
                log("Bot", "Sorry I did not hear you properly. Can you repeat that?")
    
    file.close()


if __name__ == "__main__":
    main()