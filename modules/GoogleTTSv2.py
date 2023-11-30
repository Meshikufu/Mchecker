import os
import random
import hashlib
import sqlite3
from google.cloud import texttospeech
import pygame

pygame.mixer.init()

def create_unique_id(text):
    # Use hashlib to create a unique ID based on the text content
    hash_object = hashlib.md5(text.encode())
    unique_id = hash_object.hexdigest()
    return unique_id

def create_database():
    # Create the TTSdb folder if it doesn't exist
    os.makedirs("TTSdb", exist_ok=True)

    # Create the AudioFiles subfolder
    os.makedirs("TTSdb/AudioFiles", exist_ok=True)

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('TTSdb/unique_sentences.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            unique_id TEXT PRIMARY KEY,
            filename TEXT
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

def save_to_database(unique_id, filename):
    # Create TTSdb folder if it doesn't exist
    os.makedirs("TTSdb", exist_ok=True)

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('TTSdb/unique_sentences.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            unique_id TEXT PRIMARY KEY,
            filename TEXT
        )
    ''')

    # Insert the unique ID and filename into the database
    cursor.execute('INSERT INTO sentences (unique_id, filename) VALUES (?, ?)', (unique_id, filename))

    # Commit changes and close connection
    conn.commit()
    conn.close()


    # Play the audio after saving
    playAudio(filename)


def check_if_sentence_exists(text):
    # Check if the sentence already exists in the database
    unique_id = create_unique_id(text)

    # Create TTSdb folder if it doesn't exist
    os.makedirs("TTSdb", exist_ok=True)

    conn = sqlite3.connect('TTSdb/unique_sentences.db')
    cursor = conn.cursor()

    cursor.execute('SELECT filename FROM sentences WHERE unique_id = ?', (unique_id,))
    result = cursor.fetchone()

    conn.close()

    return result

def GenerateAudioFile(text):
    # Create TTSdb folder and database if they don't exist
    create_database()

    # Check if the sentence already exists
    existing_filename = check_if_sentence_exists(text)
    if existing_filename:
        print("Sentence already generated, playing existing audio.")
        print("")
        playAudio(existing_filename[0])  # Play the existing audio
        return existing_filename[0]

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voicetype = "std"
    if voicetype == "neuro2":
        voicetype = "en-US-Neural2-H"
    elif voicetype == "std": 
        voicetype = "en-US-Standard-H"

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voicetype,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=1,
        speaking_rate=0.83
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # Create a unique ID and filename
    unique_id = create_unique_id(text)
    filename = f"{unique_id}.mp3"
    output_file_path = os.path.join("TTSdb/AudioFiles", filename)

    # Ensure the directory exists before writing the audio file
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # The response's audio_content is binary.
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file_path}"')
        print(f"created: {filename}")
        print("")

    # Save the unique ID and filename to the database
    save_to_database(unique_id, filename)

    return output_file_path

# Function to play audio files
def playAudio(filenameID):
    # Construct the absolute path for the audio file
    abs_path = os.path.abspath(os.path.join("TTSdb/AudioFiles", filenameID))

    # Load the audio file using pygame mixer
    sound = pygame.mixer.Sound(abs_path)
    # Play the audio file
    sound.play()
    # Wait until the audio finishes playing
    pygame.time.wait(int(sound.get_length() * 1000))




# Testing function
def test_tts():
    texts = ["Hello, how are you doing right now?", "This is a test.", "Another sentence for testing."]
    
    for text in texts:
        print(f"Generating audio for: {text}")
        GenerateAudioFile(text)
        print("Playing audio...")
        print()

#if __name__ == "__main__":
#    # Initialize pygame mixer
#    pygame.mixer.init()
#
#    # Run the testing function
#    test_tts()
