import soundfile as sf
import os
import re
import threading
from queue import Queue
from zipvoice.luxvoice import LuxTTS

# load model on MPS for macs
print("Loading model...")
lux_tts = LuxTTS('YatharthS/LuxTTS', device='mps')

## change this to your reference file path, can be wav/mp3
prompt_audio = 'caged-battery-charged_pGyQfLxg.mp3'

## encode audio(takes 10s to init because of librosa first time)
print("Encoding prompt audio (this might take a moment on first run)...")
encoded_prompt = lux_tts.encode_prompt(prompt_audio, rms=0.01)
print("Prompt encoded! Ready for input.")

def play_audio(queue):
    while True:
        file_path = queue.get()
        if file_path is None:
            break
        # Play the chunk audio synchronously
        os.system(f"afplay {file_path}")
        # Clean up the temporary file
        try:
            os.remove(file_path)
        except OSError:
            pass
        queue.task_done()

while True:
    try:
        text = input("\nEnter text to speak (or 'quit' to exit): ").strip()
        if not text:
            continue
        if text.lower() == 'quit':
            break

        # Split text into manageable chunks using punctuation
        raw_chunks = re.split(r'(?<=[.,!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        # Threshold: accumulate smaller pieces to avoid choppy, unnatural audio cuts
        min_chunk_length = 40
        
        for c in raw_chunks:
            c = c.strip()
            if not c:
                continue
                
            if current_chunk:
                current_chunk += " " + c
            else:
                current_chunk = c
                
            # Finish the chunk if it ends with a major punctuation or exceeds the length threshold
            if len(current_chunk) >= min_chunk_length or current_chunk[-1] in '.!?':
                chunks.append(current_chunk)
                current_chunk = ""
                
        if current_chunk:
            chunks.append(current_chunk)
        
        if not chunks:
            continue

        # Setup audio player thread to play chunks sequentially as they are generated
        audio_queue = Queue()
        player_thread = threading.Thread(target=play_audio, args=(audio_queue,))
        player_thread.start()

        for i, chunk in enumerate(chunks):
            # Pad chunk with a period if it lacks punctuation, helping the TTS model not to cut the ending abruptly
            if not re.search(r'[.,!?]$', chunk):
                chunk += "."
                
            print(f"Generating chunk {i+1}/{len(chunks)}: {chunk}")
            final_wav = lux_tts.generate_speech(chunk, encoded_prompt, num_steps=4)
            final_wav = final_wav.numpy().squeeze()
            
            chunk_file = f"temp_chunk_{i}.wav"
            sf.write(chunk_file, final_wav, 48000)
            
            # Send to player queue to play immediately
            audio_queue.put(chunk_file)

        # Signal the player thread to exit after the queue is empty
        audio_queue.put(None)
        # Wait for all chunks to finish playing
        player_thread.join()

    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        break