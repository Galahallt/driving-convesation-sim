import speech_recognition as sr
import pyttsx3
import openai
from pynput import keyboard
import threading

# Flag to control the main loop
listening = True

def on_press(key):
    global listening
    if key == keyboard.Key.esc:
        listening = False  # stop the main loop
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys

def get_response(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message['content']
    print(ChatGPT_reply)
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

def main():
    global listening
    engine = pyttsx3.init()

    # Set your openai api key and customizing the chatgpt role
    openai.api_key = r"sk-proj-EyMOcap0NWbY2Ln65TzET3BlbkFJeVNcSlhVUxqpTHoH29jV"
    messages = [{"role": "system", "content": "Your name is Jarvis and give answers in 2 lines"}]

    # Customizing the output voice
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')

    listener = keyboard.Listener(on_press=on_press)
    listener_thread = threading.Thread(target=listener.start)
    listener_thread.start()

    recognizer = sr.Recognizer()

    while listening:
        print("Listening...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 3000

            try:
                audio = recognizer.listen(source, timeout=10.0)
                response = recognizer.recognize_google(audio)
                print(response)
            
                if "jarvis" in response.lower():
                    response_from_openai, messages = get_response(response, messages)
                    engine.setProperty('rate', 120)
                    engine.setProperty('volume', volume)
                    engine.setProperty('voice', voices[0].id)
                    engine.say(response_from_openai)
                    engine.runAndWait()
                else:
                    print("Didn't recognize 'jarvis'.")
            
            except sr.UnknownValueError:
                print("Didn't recognize anything.")
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except Exception as e:
                print(f"An error occurred: {e}")

    listener_thread.join()
    print("Listener stopped.")

if __name__ == "__main__":
    main()
