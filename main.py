from audio import StreamJarvisTTS

# Initialize the StreamJarvisTTS engine
# You can customize parameters here if needed, such as prompt_audio, rms, speed, etc.
jarvis_tts = StreamJarvisTTS()

print("\nJARVIS TTS Engine initialized. All systems online.")
print("Type 'quit' or 'exit' to stop.")

while True:
    try:
        text = input("\nWhat should JARVIS say? > ").strip()
        
        if not text:
            continue
            
        if text.lower() in ['quit', 'exit']:
            print("Shutting down JARVIS audio TTS engine...")
            break
            
        # Generate and play the audio
        jarvis_tts.speak(text)
        
    except (KeyboardInterrupt, EOFError):
        print("\nShutting down JARVIS...")
        break