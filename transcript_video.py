import moviepy.editor as mp
import speech_recognition as sr

# Ścieżka do pliku wideo
video_path = "/Users/erykszczesniak/Downloads/TAWeb in Autodeploy.mp4"

# Ładowanie pliku wideo
video = mp.VideoFileClip(video_path)

# Ekstrakcja audio z wideo
audio_path = "/Users/erykszczesniak/Downloads/TAWeb_in_Autodeploy_audio.wav"
video.audio.write_audiofile(audio_path)

# Inicjalizacja rozpoznawania mowy
recognizer = sr.Recognizer()

# Transkrypcja audio
with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)
    try:
        # Rozpoznawanie mowy z użyciem Google Web Speech API
        text = recognizer.recognize_google(audio_data, language="pl-PL")
        print("Transkrypcja:")
        print(text)
    except sr.UnknownValueError:
        print("Google Web Speech API nie mogło zrozumieć audio")
    except sr.RequestError as e:
        print(f"Nie można zażądać wyników od Google Web Speech API; {e}")

# Zapisywanie transkrypcji do pliku tekstowego
transcript_path = "/Users/erykszczesniak/Downloads/TAWeb_in_Autodeploy_transcript.txt"
with open(transcript_path, "w") as transcript_file:
    transcript_file.write(text)
