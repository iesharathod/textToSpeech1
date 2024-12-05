import pyttsx3
import argparse
import traceback
import sys

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional arguments
parser.add_argument("-t", "--text", help="string input")
parser.add_argument("-l", "--language", help="english or hindi")
parser.add_argument("-a", "--accent", help="indian, australian, us & uk")
parser.add_argument("-g", "--gender", help="male or female")
parser.add_argument("-i", "--index", help="reader index, start from zero.")

# Read arguments from command line
args = parser.parse_args()

# Default values
text_to_read = "my name is isha rathod A graduate engineer who is enrolled in the development programs. Dedicated to software engineering. One year of expertise and specializations in python development. And now Contributing at world’s first quantum secure blockchain platform as a developer  "
gender = "male"
language = "english"
accent = "us"

# Update based on CLI arguments
if args.text:
    text_to_read = args.text

if args.language:
    language = args.language
    if language == "hindi":
        accent = "indian"

if args.accent:
    accent = args.accent

if args.gender:
    gender = args.gender

# Define the filter rule
def filter_rule(voice, gender, language, accent, default):
    if not voice.languages:  # Ensure languages list is not empty
        return False
    if default:
        return voice.gender in gender and voice.languages[0] == (language + '_' + accent)
    return voice.languages[0] == (language + '_' + accent) or voice.name in ["default", "Alex"]

# Filtering voices based on given criteria
def filter_voice(voices, gender, language, accent, default=True):
    if not voices:  # Check if voices list is empty
        return []
    filter_list = [voice for voice in voices if filter_rule(voice, gender, language, accent, default)]
    if filter_list:
        return filter_list
    if default:
        return filter_voice(voices, gender, language, accent, False)
    return []

# Update reader's language, accent, and gender
def update_language(reader, language, accent, gender):
    # Define mappings
    languages = {"english": "en", "hindi": "hi"}
    genders = {"male": ["VoiceGenderMale", "male"], "female": ["VoiceGenderFemale", "female"], "none": ["None"]}
    accents = {"indian": "IN", "us": "US", "australian": "AU", "uk": "GB"}

    voices = reader.getProperty('voices')

    # Debug: List available voices
    print("\nAvailable Voices:")
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}, Languages: {voice.languages}, Gender: {voice.gender}")

    # Filter voices
    filtered_voice_list = filter_voice(voices, genders[gender], languages[language], accents[accent])

    if filtered_voice_list:
        print("\nFiltered Readers:")
        for index, voice in enumerate(filtered_voice_list):
            print(f"Index: {index}, Name: {voice.name}, ID: {voice.id}, Languages: {voice.languages}, Gender: {voice.gender}")

        # Select voice by index
        index = 0
        if args.index and int(args.index) < len(filtered_voice_list):
            index = int(args.index)

        print(f"\n{filtered_voice_list[index].name} is reading for you.")
        reader.setProperty('voice', filtered_voice_list[index].id)
    else:
        print("No matching reader available. Using default voice.")
        reader.setProperty('voice', reader.getProperty('voice'))

try:
    # Initialize the text-to-speech engine
    reader = pyttsx3.init()

    # Update the reader with selected language, accent, and gender
    update_language(reader, language, accent, gender)

    # Read the text
    reader.say(text_to_read)

    # Run and wait for the TTS engine to complete
    reader.runAndWait()

    # Stop the TTS engine
    reader.stop()

except OSError as error:
    traceback.print_exception(*sys.exc_info())
    print("There is a chance that some required system library is missing. Install the library and try again.")

except Exception as error:
    traceback.print_exception(*sys.exc_info())
    print("Something went wrong. Please report the issue at https://github.com/vishalnagda1/text-to-speech/issues.")
