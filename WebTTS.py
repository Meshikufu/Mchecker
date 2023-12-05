# web_app/app.py

from flask import Flask, render_template, request
from modules.GoogleTTSv2 import TTSv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates\index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['sentence']

    # Call TTSv2 and get the file path
    file_path = TTSv2(text)

    if file_path:
        # Pass the file path to the template
        return render_template('templates\result.html', sentence=text, audio_file_path=file_path)
    else:
        # Handle case where file_path is not found
        return render_template('templates\result.html', error_message='Failed to generate audio file.')

if __name__ == '__main__':
    app.run(debug=True, port=7742)