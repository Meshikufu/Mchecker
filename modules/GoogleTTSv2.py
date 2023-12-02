import os
import random
import hashlib
import sqlite3
from google.cloud import texttospeech
import pygame
from datetime import datetime

pygame.mixer.init()


# Function to create a unique ID based on text content
def create_unique_id(text):
    # Use hashlib to create a unique ID based on the text content
    hash_object = hashlib.md5(text.encode())
    unique_id = hash_object.hexdigest()
    return unique_id

# Function to create and initialize the SQLite database
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
    conn = sqlite3.connect('TTSdb/quota.db')
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
def save_to_database(unique_id, filename, voicetype, bytes_amount, character_number):
    # Create TTSdb folder if it doesn't exist
    os.makedirs("TTSdb", exist_ok=True)

    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('TTSdb/unique_sentences.db')
    cursor = conn.cursor()

    # Insert the unique ID, filename, voicetype, bytes, character number, and date into the database
    date_now = datetime.now().strftime("%Y-%m")
    cursor.execute('''
        INSERT INTO sentences (unique_id, filename, voicetype, bytes, character_number, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (unique_id, filename, voicetype, bytes_amount, character_number, date_now))

    conn.commit()
    conn.close()

    playAudio(filename)

def quota_db(date_voicetype, bytes_sum, char_len_sum):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('TTSdb/quota.db')
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

### Main function to run
def GenerateAudioFile(text):
    quotaLimit = False
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
    
    voicetype = "Basic"
    if voicetype == "Neuro2":
        voicetype = "en-US-Neural2-H"
    elif voicetype == "Basic": 
        voicetype = "en-US-Standard-H"
    
    date_voicetype = datetime.now().strftime("%Y-%m") + voicetype

    # Check if the voicetype is "en-US-Standard-H"
    if "en-US-Standard-H" in date_voicetype:
        # Get the character length sum from the quota_db function
        char_len_sum = get_char_len_sum_from_quota_db(date_voicetype)

        char_len_quota = 3500000

        # Check if the character length exceeds the quota
        if char_len_sum > char_len_quota:
            print("Quota exceeded for", date_voicetype)
            quotaLimit = True

            sound_folder = "sounds"
            sound_file = "bell.wav"
            sound_path = os.path.join(sound_folder, sound_file)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
    if quotaLimit == False:
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

        # Save the unique ID, filename, voicetype, bytes, character number, and date to the database
        quota_db(date_voicetype, len(response.audio_content), len(text))
        save_to_database(unique_id, filename, voicetype, len(response.audio_content), len(text))


    elif quotaLimit == True:
        import tempfile
        from gtts import gTTS
        speech = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(suffix='.mp3', dir="ttsvoice", delete=False) as fp:
            speech.write_to_fp(fp)
            filename = fp.name
            print(f"created: {filename}\n")
            fp.close()
            sound = pygame.mixer.Sound(filename)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
            os.remove(filename)
            print(f"Deleted file: {filename}\n")
            output_file_path = None

    return output_file_path


# Function to play audio files
def playAudio(filenameID):
    # Construct the absolute path for the audio file
    abs_path = os.path.abspath(os.path.join("TTSdb/AudioFiles", filenameID))
    # Load the audio file using pygame mixer
    sound = pygame.mixer.Sound(abs_path)
    sound.play()
    # Wait until the audio finishes playing
    pygame.time.wait(int(sound.get_length() * 1000))



def get_char_len_sum_from_quota_db(date_voicetype):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('TTSdb/quota.db')
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
    texts = ["Hello, how are you doing right now?", "This is a mmm testing.", "Another sentence for testing."]
    
    for text in texts:
        print(f"Generating audio for: {text}")
        GenerateAudioFile(text)
        print("Playing audio...")
        print()

#test_tts()
#if __name__ == "__main__":
#    # Initialize pygame mixer
#    pygame.mixer.init()
#
#    # Run the testing function
#    test_tts()
