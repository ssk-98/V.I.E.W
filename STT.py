import random
import time
import subprocess
from subprocess import call
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        recognizer.pause_threshold = 0.8
        audio = recognizer.listen(source)
        #except:
        #    response["success"] = True
        #    return response
        

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def stt(NUM_ATTEMPTS, PROMPT_LIMIT, OPTIONS = None):

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # format the instructions string
    if OPTIONS is not None:
        instructions = (
            "Available options:\n"
            "{words}\n"
            "You have {n} attempts.\n"
        ).format(words=', '.join(OPTIONS), n=NUM_ATTEMPTS)

        # show instructions
        print(instructions)

    # wait before starting recording session
    time.sleep(5)

    for i in range(NUM_ATTEMPTS):
        # get the attempt from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their attempt again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Attempt {}. Speak now:'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. Please try again.\n")

        # if there was an error, stop 
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        transcription = guess["transcription"].lower()
        print("You said: {}".format(transcription))

        if OPTIONS is not None:
            # determine if guess is correct and if any attempts remain
            guess_is_correct = transcription in OPTIONS
            user_has_more_attempts = i < NUM_ATTEMPTS - 1

            if guess_is_correct:
                return transcription
            elif user_has_more_attempts:
                print("Not a valid option. Please try again.\n")
        else:
            return transcription

def stt_min(timeout):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
        response = {
            "success": True,
            "error": None,
            "transcription": None
            }
        with microphone as source:
            recognizer.pause_threshold = 0.8
            audio = recognizer.record(source,duration=timeout)
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"
        if response["transcription"] != None:
            break
        if not response["success"]:
            break
        tts("Retry")
    transcription = response["transcription"].lower()
    return transcription

def tts(text):
    call(["espeak", "-s130 -ven+18 -z", text], stderr = subprocess.DEVNULL)
    print(text)
        

if __name__ == "__main__":

    # set the list of words, maxnumber of attempts, and prompt limit
    OPTIONS = ["face recognition", "character recognition", "distance measure", "object recognition"]
    NUM_ATTEMPTS = 3
    PROMPT_LIMIT = 5

    transcription = stt(NUM_ATTEMPTS, PROMPT_LIMIT, OPTIONS)
    print(transcription)
