import os
import speech_recognition as sr
import streamlit as st
import googletrans as trans
import gtts

# Title and Language Selection
st.title("Speech Recognition App")
languages = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
             'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs',
             'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn',
             'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da',
             'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi',
             'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el',
             'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi',
             'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga',
             'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km',
             'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv',
             'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms',
             'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn',
             'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps',
             'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru',
             'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd',
             'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su',
             'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th',
             'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi',
             'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
targeted_lang = st.selectbox("Choose language to translate to", list(languages.keys()))

# Initialize recognizer
recognizer = sr.Recognizer()


def process_audio_file(audio_file):
    try:
        audio_data = sr.AudioFile(audio_file)
        with audio_data as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")

        # Translation
        translator = trans.Translator()
        translation = translator.translate(text, dest=languages[targeted_lang])
        st.success(f"Translation is: {translation.text}")

        # Convert to speech
        converted_audio = gtts.gTTS(translation.text, lang=languages[targeted_lang])
        audio_path = "translated_audio.mp3"
        converted_audio.save(audio_path)

        # Display audio
        st.audio(audio_path, format="audio/mp3")

        # Download button
        with open(audio_path, "rb") as file:
            st.download_button("Download", file, file_name="translated_audio.mp3")

        os.remove(audio_path)  # Clean up
    except Exception as e:
        st.error(f"Error: {e}")


# Audio file uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if st.button("Translate"):
    if uploaded_file is not None:
        process_audio_file(uploaded_file)
    else:
        st.warning("Please upload an audio file.")
