from modules.audio import StreamJarvisTTS

text = "My name is JARVIS, an advanced artificial intelligence designed to assist, analyze, and anticipate your needs with precision. All systems are now online and functioning within optimal parameters. I am fully synchronized and ready to provide real-time insights, manage tasks, and ensure seamless operation across all connected processes. How may I be of service?"

# Initialize the StreamJarvisTTS engine
# You can customize parameters here if needed, such as prompt_audio, rms, speed, etc.
jarvisTTS = StreamJarvisTTS()

# Stream the text in real-time
jarvisTTS.speak(text)