from playsound import playsound ### Has to be 1.2.2
import os

def playAudio(file_name, sound_folder="sounds"): 
    sound_path = os.path.join(sound_folder, file_name)
    abs_sound_path = os.path.abspath(sound_path)  # Get the absolute path
    abs_sound_path = abs_sound_path.replace("\\", "\\\\") # Ensure the path is correctly formatted for Windows MCI commands
    try:
        playsound(abs_sound_path)
    except Exception as e:
        print(f"An error occurred while trying to play sound: {e}")