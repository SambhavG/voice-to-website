import sys
import json
import wave
import time
import pyttsx3
import torch
import requests
import soundfile
import yaml
import pygame
import pygame.locals
import numpy as np
import pyaudio
import whisper
import os

BACK_COLOR = (0, 0, 0)
REC_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
REC_SIZE = 80
FONT_SIZE = 24
WIDTH = 320
HEIGHT = 240
KWIDTH = 20
KHEIGHT = 6
MAX_TEXT_LEN_DISPLAY = 32

INPUT_DEFAULT_DURATION_SECONDS = 5
INPUT_FORMAT = pyaudio.paInt16
INPUT_CHANNELS = 1
INPUT_RATE = 16000
INPUT_CHUNK = 1024
OLLAMA_REST_HEADERS = {"Content-Type": "application/json"}
INPUT_CONFIG_PATH = "assistant.yaml"

deleteEverythingComponent = """import React from 'react';

const Component = () => {
  return (
    <div>
      Hello World!
    </div>
  );
}

export default Component;"""


def removeBackticks(response):
    # Replace ``` with \n```
    response = response.replace("```", "\n```")
    response = response.split("\n")
    # Find the first line with ``` in it and remove everything before it, unless the first nonwhitespace character
    # after it is a <, in which case remove the backticks from the line and all lines before it
    firstIndex = -1
    for i in range(len(response)):
        if "```" in response[i]:
            firstIndex = i
            break
    if firstIndex != -1:
        response = response[firstIndex + 1 :]
    # Find the last line with ``` in it and remove everything after it
    lastIndex = -1
    for i in range(len(response) - 1, -1, -1):
        if "```" in response[i]:
            lastIndex = i
            break
    if lastIndex != -1:
        response = response[: lastIndex + 1]
        # Remove the backticks and everything after them from the last line
        response[lastIndex] = response[lastIndex].split("```")[0]
        # If the last line is empty, remove it
        if response[lastIndex] == "":
            response = response[:lastIndex]
    return "\n".join(response)


def parseResponse(response):
    # The response is a block of text
    response = removeBackticks(response)

    # Import any react hooks that are used and weren't imported
    possibleHooks = [
        "useState",
        "useEffect",
        "useContext",
        "useReducer",
        "useRef",
        "useMemo",
        "useCallback",
        "useImperativeHandle",
        "useLayoutEffect",
        "useDebugValue",
        "useTransition",
        "useDeferredValue",
        "useOpaqueIdentifier",
        "useMutableSource",
        "useOpaqueIdentifier",
        "useDeferredValue",
        "useTransition",
        "useMutableSource",
        "useOpaqueIdentifier",
    ]

    # First, make a list of all the hooks which appear in the response
    hooksUsed = []
    for hook in possibleHooks:
        if hook in response:
            hooksUsed.append(hook)
    response = response.split("\n")

    # Second, find the line with "from 'react';" and import all the hooks that are used
    for i in range(len(response)):
        if "from 'react';" in response[i]:
            # Found the line. Delete it
            response[i] = ""
            break
    if len(hooksUsed) > 0:
        newImportLine = "import { " + ", ".join(hooksUsed) + " } from 'react';"
        response.insert(0, newImportLine)
    if "import React from 'react';" not in response and "React" in "".join(response):
        response.insert(0, "import React from 'react';")
    response = "\n".join(response)

    # Determine if the response has a "export default" line
    if not "export default" in response:
        # Determine name of component. Find first appearance of "const" and use the word after it
        responseLines = response.split("\n")
        for i in range(len(responseLines)):
            if "const" in responseLines[i]:
                componentName = responseLines[i].split(" ")[1]

        response = response + "\n\nexport default " + componentName + ";"

    # If the line `import { useState } from "react";` appears twice, remove the second one
    response = response.split("\n")
    importCount = 0
    for i in range(len(response)):
        if "import { useState } from 'react';" in response[i]:
            importCount += 1
            if importCount == 2:
                response[i] = ""
    response = "\n".join(response)

    return response


class Assistant:
    def __init__(self):
        self.config = self.init_config()

        programIcon = pygame.image.load("assistant.png")

        self.clock = pygame.time.Clock()
        pygame.display.set_icon(programIcon)
        pygame.display.set_caption("Assistant")

        self.windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.audio = pyaudio.PyAudio()

        self.tts = pyttsx3.init("nsss")
        self.tts.setProperty("rate", self.tts.getProperty("rate") - 20)

        try:
            self.audio.open(
                format=INPUT_FORMAT,
                channels=INPUT_CHANNELS,
                rate=INPUT_RATE,
                input=True,
                frames_per_buffer=INPUT_CHUNK,
            ).close()
        except Exception:
            self.wait_exit()

        self.display_message(self.config.messages.loadingModel)
        self.model = whisper.load_model(self.config.whisperRecognition.modelPath)
        self.context = []

        self.text_to_speech(self.config.conversation.greeting)
        time.sleep(0.5)
        self.display_message(self.config.messages.pressSpace)

    def wait_exit(self):
        while True:
            self.display_message(self.config.messages.noAudioInput)
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.shutdown()

    def shutdown(self):
        self.audio.terminate()
        pygame.quit()
        sys.exit()

    def init_config(self):
        class Inst:
            pass

        with open("assistant.yaml", encoding="utf-8") as data:
            configYaml = yaml.safe_load(data)

        config = Inst()
        config.messages = Inst()
        config.messages.loadingModel = configYaml["messages"]["loadingModel"]
        config.messages.pressSpace = configYaml["messages"]["pressSpace"]
        config.messages.noAudioInput = configYaml["messages"]["noAudioInput"]

        config.conversation = Inst()
        config.conversation.greeting = configYaml["conversation"]["greeting"]

        config.ollama = Inst()
        config.ollama.url = configYaml["ollama"]["url"]
        config.ollama.model = configYaml["ollama"]["model"]

        config.whisperRecognition = Inst()
        config.whisperRecognition.modelPath = configYaml["whisperRecognition"][
            "modelPath"
        ]
        config.whisperRecognition.lang = configYaml["whisperRecognition"]["lang"]

        config.autowebsite = Inst()
        config.autowebsite.userPromptFilePath = configYaml["autowebsite"][
            "userPromptFilePath"
        ]
        config.autowebsite.userPromptFormatFilePath = configYaml["autowebsite"][
            "userPromptFormatFilePath"
        ]
        config.autowebsite.componentFilePath = configYaml["autowebsite"][
            "componentFilePath"
        ]
        config.autowebsite.componentPlaintextFilePath = configYaml["autowebsite"][
            "componentPlaintextFilePath"
        ]
        config.autowebsite.forceRefreshCodeDisplay = configYaml["autowebsite"][
            "forceRefreshCodeDisplay"
        ]
        config.autowebsite.syntaxCorrectionPrompt = configYaml["autowebsite"][
            "syntaxCorrectionPrompt"
        ]

        return config

    def display_rec_start(self):
        self.windowSurface.fill(BACK_COLOR)
        pygame.draw.circle(
            self.windowSurface, REC_COLOR, (WIDTH / 2, HEIGHT / 2), REC_SIZE
        )
        pygame.display.flip()

    def display_sound_energy(self, energy):
        COL_COUNT = 5
        RED_CENTER = 100
        FACTOR = 10
        MAX_AMPLITUDE = 100

        self.windowSurface.fill(BACK_COLOR)
        amplitude = int(MAX_AMPLITUDE * energy)
        hspace, vspace = 2 * KWIDTH, int(KHEIGHT / 2)

        def rect_coords(x, y):
            return (int(x - KWIDTH / 2), int(y - KHEIGHT / 2), KWIDTH, KHEIGHT)

        for i in range(-int(np.floor(COL_COUNT / 2)), int(np.ceil(COL_COUNT / 2))):
            x, y, count = WIDTH / 2 + (i * hspace), HEIGHT / 2, amplitude - 2 * abs(i)

            mid = int(np.ceil(count / 2))
            for i in range(0, mid):
                offset = i * (KHEIGHT + vspace)
                pygame.draw.rect(
                    self.windowSurface, RED_CENTER, rect_coords(x, y + offset)
                )
                # mirror:
                pygame.draw.rect(
                    self.windowSurface, RED_CENTER, rect_coords(x, y - offset)
                )
        pygame.display.flip()

    def display_message(self, text):
        self.windowSurface.fill(BACK_COLOR)

        label = self.font.render(
            (
                text
                if (len(text) < MAX_TEXT_LEN_DISPLAY)
                else (text[0:MAX_TEXT_LEN_DISPLAY] + "...")
            ),
            1,
            TEXT_COLOR,
        )

        size = label.get_rect()[2:4]
        self.windowSurface.blit(
            label, (WIDTH / 2 - size[0] / 2, HEIGHT / 2 - size[1] / 2)
        )

        pygame.display.flip()

    def waveform_from_mic(self, key=pygame.K_SPACE) -> np.ndarray:

        self.display_rec_start()

        stream = self.audio.open(
            format=INPUT_FORMAT,
            channels=INPUT_CHANNELS,
            rate=INPUT_RATE,
            input=True,
            frames_per_buffer=INPUT_CHUNK,
        )
        frames = []

        while True:
            pygame.event.pump()  # process event queue
            pressed = pygame.key.get_pressed()
            if pressed[key]:
                data = stream.read(INPUT_CHUNK)
                frames.append(data)
            else:
                break

        stream.stop_stream()
        stream.close()

        return np.frombuffer(b"".join(frames), np.int16).astype(np.float32) * (
            1 / 32768.0
        )

    def speech_to_text(self, waveform):
        transcript = self.model.transcribe(
            waveform,
            language=self.config.whisperRecognition.lang,
            fp16=torch.cuda.is_available(),
        )
        text = transcript["text"]

        # Write the text to the text prompt file, which is in yaml at autowebsite.user-prompt-file-path
        with open(self.config.autowebsite.userPromptFilePath, "w") as f:
            # Delete the previous content
            f.truncate(0)
            f.write('const userPrompt = "' + text + '"; export default userPrompt;')

        print("\nMe:\n", text.strip())
        return text

    def ask_ollama(self, full_prompt):
        jsonParam = {
            "model": self.config.ollama.model,
            "stream": True,
            "context": self.context,
            "prompt": full_prompt,
        }
        response = requests.post(
            self.config.ollama.url,
            json=jsonParam,
            headers=OLLAMA_REST_HEADERS,
            stream=True,
            timeout=10,
        )  # Set the timeout value as per your requirement

        response.raise_for_status()

        tokens = []
        for line in response.iter_lines():
            body = json.loads(line)
            token = body.get("response", "")
            tokens.append(token)
            # Last 50 characters of the response
            self.display_message("".join(tokens)[-50:])

            # if "error" in body:
            #     responseCallback("Error: " + body["error"])

            if body.get("done", False) and "context" in body:
                current_response = "".join(tokens)

        return current_response

    def make_component(self, prompt):

        # Get previous component from self.config.autowebsite.componentFilePath
        with open(self.config.autowebsite.componentFilePath, "r") as f:
            component = f.read()

        # Check if prompt contains the text "fix error" with a case-insensitive search
        if "fix error" in prompt.lower():
            fileToOpen = self.config.autowebsite.syntaxCorrectionPrompt
        else:
            fileToOpen = self.config.autowebsite.userPromptFormatFilePath

        if "delete all" in prompt.lower():
            current_response = deleteEverythingComponent
        else:
            with open(fileToOpen, "r") as f:
                promptTemplate = f.read()

            promptTemplate = promptTemplate.replace("***COMPONENT***", component)
            promptTemplate = promptTemplate.replace("***REQUEST***", prompt)

            self.contextSent = True
            current_response = self.ask_ollama(promptTemplate)

            current_response = parseResponse(current_response)

        print("\nAI:\n", current_response)

        # Write to the component file
        with open(self.config.autowebsite.componentFilePath, "w") as f:
            f.truncate(0)
            f.write(current_response)
        # ... and to the plaintext file
        with open(self.config.autowebsite.componentPlaintextFilePath, "w") as f:
            f.truncate(0)
            f.write(current_response)
        # ... and force refresh
        with open(self.config.autowebsite.forceRefreshCodeDisplay, "r+") as f:
            # The second line says "x = [some number];" - change the number to a random int to force a refresh
            # First read the entire file
            file = f.readlines()
            # Find the line with the format "let x = [some number];" and change the number to a random int
            for i in range(len(file)):
                if "let x = " in file[i]:
                    file[i] = "let x = " + str(int(time.time())) + ";\n"
                    break
            # Then write the entire file back
            f.truncate(0)
            f.seek(0)
            f.writelines(file)

        # self.context = body["context"]

    # def fix_component(self, component):
    #     with open(self.config.autowebsite.syntaxCorrectionPrompt, "r") as f:
    #         promptTemplate = f.read()

    #     full_prompt = promptTemplate.replace("***COMPONENT***", component)
    #     current_response = self.ask_ollama(full_prompt)

    #     # Remove backticks
    #     current_response = removeBackticks(current_response)

    #     return current_response

    def text_to_speech(self, text):
        print("\nAI:\n", text.strip())

        tempPath = "./temp.wav"
        self.tts.save_to_file(text, tempPath)
        self.tts.runAndWait()

        # Fix 64bit RIFF id for Apple Silicon
        data, samplerate = soundfile.read(tempPath)
        soundfile.write(tempPath, data, samplerate)

        wf = wave.open(tempPath, "rb")

        stream = self.audio.open(
            format=self.audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

        chunkSize = 1024
        chunk = wf.readframes(chunkSize)
        while chunk:
            stream.write(chunk)
            tmp = np.array(np.frombuffer(chunk, np.int16), np.float32) * (1 / 32768.0)
            energy_of_chunk = np.sqrt(np.mean(tmp**2))
            self.display_sound_energy(energy_of_chunk)
            chunk = wf.readframes(chunkSize)

        wf.close()


def main():

    pygame.init()

    assist = Assistant()

    push_to_talk_key = pygame.K_SPACE

    running = True
    while running:
        assist.clock.tick(60)
        pygame.event.pump()  # Process system events

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == push_to_talk_key:
                speech = assist.waveform_from_mic(push_to_talk_key)
                transcription = assist.speech_to_text(waveform=speech)
                # Print the transcription
                assist.make_component(transcription)
                time.sleep(1)
                assist.display_message(assist.config.messages.pressSpace)

            # if event.type == pygame.locals.QUIT:
            #     running = True  # Exit the loop and shutdown the program

    assist.shutdown()


if __name__ == "__main__":
    main()

# Supress secure code Apple warning.
f = open("/dev/null", "w")
os.dup2(f.fileno(), 2)
f.close()
