import speech_recognition as sr
import pyttsx3
import openai

import keyboard

done = False
name = "carla"
keyword = "hello " + name
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
    #ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

#Initializing pyttsx3
def main():
    global keyword, name
    keyboard.add_hotkey("shift+a", execute) # add the hotkey
    listening = True
    engine = pyttsx3.init()

    #Set your openai api key and customizing the chatgpt role
    openai.api_key = r"sk-proj-EyMOcap0NWbY2Ln65TzET3BlbkFJeVNcSlhVUxqpTHoH29jV"

    style = 2

    init_msg = ""
    end_msg = ""
    
    if style == 1:
        init_msg = "let's do some trivia to get you awake"
        end_msg = "Thank you for playing, I'll alert you again if you get sleepy"
    elif style == 2:
        init_msg = "let's talk"
        end_msg = "I enjoyed our conversation, I'll talk again when you get sleepy"

    if style == 1:
        messages = [{
                    "role": "system", 
                    "content": f"You are a game show host for trivia questions. Your name is {name}. Limit your response to two sentences. Less is better."
                    },
                    # {
                    # "role": "assistant", 
                    # "content": "I'll give you one trivia question. What is the tallest mountain in the world?"
                    # },
                    # {
                    # "role": "user", 
                    # "content": "Mt. Everest.! Ask me another."
                    # },    
                    ]
    elif style == 2:
        messages =[{
                    "role": "system", 
                    "content": f"Act like a close friend. Your name is {name}. Limit your response to two sentences. Less is better."
                    }
                    ]
    #Customizing The output voice

    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')

    # listener = keyboard.Listener(on_press=on_press)
    # listener.start()
    # listener.join() 
    
    input("Press Enter to to start...")

    engine.setProperty('rate', 150)
    engine.setProperty('volume', volume)
    engine.setProperty('voice', 'english')
    engine.say(f"you're looking sleepy, {init_msg}")
    engine.runAndWait()

    if style == 1:
        response_from_openai, messages = get_response('I\'m ready, ask me a question.', messages)
    elif style == 2:
        response_from_openai, messages = get_response('Ask me anything that you would like to know about me.', messages)

    engine.setProperty('rate', 120)
    engine.setProperty('volume', volume)
    engine.setProperty('voice', 'greek')
    engine.say(response_from_openai)
    engine.runAndWait()

    # with sr.Microphone() as source:
    #     recognizer = sr.Recognizer()
    #     recognizer.adjust_for_ambient_noise(source)
    #     recognizer.dynamic_energy_threshold = 3000

    global done
    while listening:

        if done:
            engine.setProperty('rate', 150)
            engine.setProperty('volume', volume)
            engine.setProperty('voice', 'english')
            engine.say(end_msg)
            engine.runAndWait()
            break

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 3000
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=20.0)
                response = recognizer.recognize_google(audio)
                print(response)
            
                if keyword in response.lower():
                    
                    response_from_openai, messages = get_response(response, messages)
                    engine.setProperty('rate', 120)
                    engine.setProperty('volume', volume)
                    engine.setProperty('voice', 'greek')
                    engine.say(response_from_openai)
                    engine.runAndWait()        
                
                else:
                    print(f"Didn't recognize {keyword}.")
            
            except sr.UnknownValueError:
                print("Didn't recognize anything.")

if __name__ == "__main__":
    main()