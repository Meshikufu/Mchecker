import os
import random
import hashlib
import sqlite3
from google.cloud import texttospeech
import pygame
from datetime import datetime
import tempfile
from gtts import gTTS
from google.api_core.exceptions import ResourceExhausted


pygame.mixer.init()


def play_bell():
    sound_folder = "sounds"
    sound_file = "bell.wav"
    sound_path = os.path.join(sound_folder, sound_file)

    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Function to create a unique ID based on text content
def create_unique_id(text):
    # Use hashlib to create a unique ID based on the text content
    hash_object = hashlib.md5(text.encode())
    unique_id = hash_object.hexdigest()
    return unique_id

# Function to create and initialize the SQLite database
def create_database(path_tts_db):
    # Create the TTSdb folder if it doesn't exist
    os.makedirs(rf'{path_tts_db}', exist_ok=True)

    # Create the AudioFiles subfolder
    os.makedirs(rf'{path_tts_db}/AudioFiles', exist_ok=True)

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(rf'{path_tts_db}/unique_sentences.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            unique_id TEXT PRIMARY KEY,
            filename TEXT,
            voicetype TEXT,
            bytes INTEGER,
            character_number INTEGER,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(rf'{path_tts_db}/quota.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quota (
            date_voicetype TEXT PRIMARY KEY,
            bytes_sum INTEGER,
            char_len_sum INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Function to save a unique ID, filename, voicetype, bytes, character number, and date to the database
def save_to_database(unique_id, filename, voicetype, bytes_amount, character_number, path_tts_db):
    # Create TTSdb folder if it doesn't exist
    os.makedirs(rf'{path_tts_db}', exist_ok=True)

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(rf'{path_tts_db}/unique_sentences.db')
    cursor = conn.cursor()

    # Insert the unique ID, filename, voicetype, bytes, character number, and date into the database
    date_now = datetime.now().strftime("%Y-%m")
    cursor.execute('''
        INSERT INTO sentences (unique_id, filename, voicetype, bytes, character_number, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (unique_id, filename, voicetype, bytes_amount, character_number, date_now))

    conn.commit()
    conn.close()

    playAudio(filename, path_tts_db)

def quota_db(date_voicetype, bytes_sum, char_len_sum, path_tts_db):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(rf'{path_tts_db}/quota.db')
    cursor = conn.cursor()

    # Try to update the existing record
    cursor.execute('''
        UPDATE quota
        SET bytes_sum = bytes_sum + ?,
            char_len_sum = char_len_sum + ?
        WHERE date_voicetype = ?
    ''', (bytes_sum, char_len_sum, date_voicetype))

    # If no records were updated, insert a new record
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO quota (date_voicetype, bytes_sum, char_len_sum)
            VALUES (?, ?, ?)
        ''', (date_voicetype, bytes_sum, char_len_sum))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def check_if_sentence_exists(text, path_tts_db):
    # Check if the sentence already exists in the database
    unique_id = create_unique_id(text)

    # Create TTSdb folder if it doesn't exist
    os.makedirs(rf'{path_tts_db}', exist_ok=True)

    conn = sqlite3.connect(rf'{path_tts_db}/unique_sentences.db')
    cursor = conn.cursor()

    cursor.execute('SELECT filename FROM sentences WHERE unique_id = ?', (unique_id,))
    result = cursor.fetchone()

    conn.close()
    return result

# Function to play audio files
def playAudio(filenameID, path_tts_db):
    # Construct the absolute path for the audio file
    abs_path = os.path.abspath(os.path.join(rf'{path_tts_db}/AudioFiles', filenameID))
    # Load the audio file using pygame mixer
    sound = pygame.mixer.Sound(abs_path)
    sound.play()
    # Wait until the audio finishes playing
    pygame.time.wait(int(sound.get_length() * 1000))

### Main function to run
def TTSv2(text, path=None):
    TTS_type = None
    output_file_path = None

    if path is None:
        path_tts_db = 'modules/TTSdb'
    else:
        path_tts_db = path
        
    # Create TTSdb folder and database if they don't exist
    create_database(path_tts_db)

    # Check if the sentence already exists
    existing_filename = check_if_sentence_exists(text, path_tts_db)
    if existing_filename:
        print("Sentence already generated, playing existing audio.")
        print("")
        playAudio(existing_filename[0], path_tts_db)  # Play the existing audio
        #path_tts_db_audio = rf'{path_tts_db}/AudioFiles/{existing_filename[0]}'
        abs_path = os.path.abspath(os.path.join(rf'{path_tts_db}/AudioFiles', existing_filename[0]))
        return abs_path

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    test1 = 0
    if test1 == 0:
        # Get the character length sum from the quota_db function
        voicetype = "en-US-Standard-H"  # "Basic"
        date_voicetype = datetime.now().strftime("%Y-%m") + voicetype
        char_len_sum = get_char_len_sum_from_quota_db(date_voicetype, path_tts_db)
        char_len_quota = 3500000
        if char_len_sum <= char_len_quota:
            TTS_type = "Basic"
        elif char_len_sum > char_len_quota:
            print("Quota exceeded for", date_voicetype)
            #play_bell()
            voicetype = "en-US-Wavenet-H"
            date_voicetype = datetime.now().strftime("%Y-%m") + voicetype
            char_len_sum = get_char_len_sum_from_quota_db(date_voicetype, path_tts_db)
            char_len_quota = 750000
            if char_len_sum <= char_len_quota:
                TTS_type = "WaveNet"
            elif char_len_sum > char_len_quota:
                print("Quota exceeded for", date_voicetype)
                print("Initiating shitty text to speech")
                TTS_type = "gTTS"
    
    if test1 == 1:
        voicetype = "en-US-Wavenet-H"
        date_voicetype = datetime.now().strftime("%Y-%m") + voicetype
        TTS_type = "WaveNet"

    if TTS_type == "Basic" or "Neuro2" or "WaveNet":
        try:
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
            output_file_path = os.path.join(rf'{path_tts_db}/AudioFiles', filename)
            abs_path = os.path.abspath(os.path.join(rf'{path_tts_db}/AudioFiles', filename))

            # Ensure the directory exists before writing the audio file
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # The response's audio_content is binary.
            with open(output_file_path, "wb") as out:
                out.write(response.audio_content)
                print(f'Audio content written to file "{output_file_path}"')
                print(f"created with {TTS_type}: {filename}")
                print("")

            # Save to the database
            if TTS_type == "Basic":
                save_to_database(unique_id, filename, voicetype, len(response.audio_content), len(text), path_tts_db)
            quota_db(date_voicetype, len(response.audio_content), len(text), path_tts_db)
            if TTS_type != "Basic":

                playAudio(filename)
                print(f"Deleted file: {filename}\n")
                print(output_file_path)
                os.remove(output_file_path)
        except ResourceExhausted as e:
            print(f"Caught ResourceExhausted error: {e}")
            TTS_type = "gTTS"

    if TTS_type == "gTTS":
        speech = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(suffix='.mp3', dir="ttsvoice", delete=False) as fp:
            speech.write_to_fp(fp)
            filename = fp.name
            print(f"created with {TTS_type}: {filename}")
            fp.close()
            sound = pygame.mixer.Sound(filename)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
            os.remove(filename)
            print(f"Deleted file: {filename}\n")
            output_file_path = None

    return abs_path


def get_char_len_sum_from_quota_db(date_voicetype, path_tts_db):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(rf'{path_tts_db}/quota.db')
    cursor = conn.cursor()

    # Fetch the char_len_sum for the given date_voicetype
    cursor.execute('''
        SELECT char_len_sum
        FROM quota
        WHERE date_voicetype = ?
    ''', (date_voicetype,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


# Testing function
def test_tts():
    texts = ["Hello, how are you doing right now?", "This isa a testing.", "Another sentence for testing."]
    
    for text in texts:
        print(f"Generating audio for: {text}")
        TTSv2(text)
        print("Playing audio...")
        print()

#test_tts()