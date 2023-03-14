import asyncio
import os
import time
from pydub import AudioSegment
import edge_tts
import pygame
import openai # this is a modified version: the base path has been changed to a tencent proxy server
import speech_recognition as sr
import STT
import file_utils
import memory

openai.api_key = file_utils.load_from_json("settings.json")["openai_key"]
if not openai.api_key:
    print("please set your api key!")
    input()
    exit()
pygame.init()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
mic = sr.Microphone()

def get_audio_length(audio_file_path="reply.mp3"):
    audio_file = AudioSegment.from_file(audio_file_path)
    audio_length = len(audio_file)
    audio_length_sec = audio_length / 1000
    return audio_length_sec

async def text_to_speech(text='', output_file="reply.mp3", voice="zh-TW-HsiaoChenNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def play_sound(filename="reply.mp3"):
    # For some reason the sound.play doesn't work. So I have to use music instead.
    pygame.mixer.music.unload() # clear resources
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def generate_prompt(user_input: str):
    # preprocess
    user_input = user_input.strip()
    # semantic search
    vector = memory.gpt3_embedding(user_input)
    total_memory = []
    for file_name in os.listdir("memories"):
        try:
            total_memory += file_utils.load_from_json(f"memories/{file_name}")
        except Exception:
            print(f"{file_name} is empty or wrong format.")

    if total_memory:
        fetched_memories = memory.fetch_memories(vector, total_memory, 1)
    else:
        return {"role": "user", "content": user_input}

    declarative_memories = "\n".join([_["content"] for _ in fetched_memories])
    prompt = [
        # {"role": "user", "content": f"Remember:\n{declarative_memories}"},
        {"role": "assistant", "content": f"{declarative_memories}"},
        {"role": "user", "content": user_input}
    ]
    return prompt

def get_response(prompt: list, max_tokens=50):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content

conversation = []
async def main():
    play_sound("loading.mp3")
    print("loading...")
    await text_to_speech("hello")
    STT.transcribe()
    play_sound()
    print(f"Chloe: Hello.")

    while True:
        while True: # continue only if the input is not empty
            with mic as source:
                r = sr.Recognizer()
                r.dynamic_energy_threshold = False
                r.energy_threshold = 250
                r.pause_threshold = 1
                # r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source)
                print("Recording ended.")

            user_input = r.recognize_whisper(audio, language="English", model="small")[1:]
            if user_input:
                break

        print(f"user: {user_input}")
        conversation.append({"role": "user", "content": user_input})
        user_prompt = generate_prompt(user_input)  # the prompt is internal. Not visible to the user.

        # chloe_output = get_response(user_prompt).replace("\n", "")
        chloe_output = "testing"

        pygame.mixer.music.unload()
        await text_to_speech(chloe_output)
        play_sound()
        print(f"Chloe: {chloe_output}")
        conversation.append({"role": "assistant", "content": chloe_output})
        time.sleep(get_audio_length())

if __name__ == "__main__":
    # asyncio.run(main())
    generated = generate_prompt("Hi?")
    print(generated)
    # print(generated, get_response(generated))
