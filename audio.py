import os
import sys
import time
import soundfile as sf
import re
import threading
import queue

# Add the current directory to sys.path so that 'zipvoice' can be imported correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from zipvoice.luxvoice import LuxTTS

class StreamJarvisTTS:
    """
    A class for Text-to-Speech using LuxTTS.
    """
    def __init__(self, 
                 model_name='YatharthS/LuxTTS', 
                 device='mps', # mps or cpu
                 prompt_audio=os.path.join(os.path.dirname(__file__), 'sample.mp3'), # sample voice of jarvis
                 rms=0.2, 
                 ref_duration=30,
                 t_shift=0.9,
                 speed=0.8,
                 return_smooth=False,
                 num_steps=4):
        
        self.device = device
        self.prompt_audio = prompt_audio
        self.rms = rms
        self.ref_duration = ref_duration
        self.t_shift = t_shift
        self.speed = speed
        self.return_smooth = return_smooth
        self.num_steps = num_steps
        
        print("Loading TTS model...")
        self.lux_tts = LuxTTS(model_name, device=self.device)
        
        print("Encoding prompt audio (this might take a moment on first run)...")
        self.encoded_prompt = self.lux_tts.encode_prompt(
            self.prompt_audio, 
            rms=self.rms, 
            duration=self.ref_duration
        )
        print("Prompt encoded! TTS initialized.")

    def _play_audio_worker(self):
        """Worker thread that continuously plays audio files from the queue."""
        while True:
            file_path = self.audio_queue.get()
            if file_path is None:  # Sentinel value to stop the thread
                break
            os.system(f"afplay {file_path}")
            try:
                os.remove(file_path)
            except OSError:
                pass
            self.audio_queue.task_done()

    def speak(self, text):
        """
        Splits text into chunks, generates audio for each chunk, and streams playback.
        """
        if not text.strip():
            return
            
        print("working out audio...")
        
        # Split text into sentences/chunks to stream generation and playback
        # This regex splits by punctuation (. ! ? \n) while keeping the punctuation with the sentence
        chunks = re.split(r'(?<=[.!?\n])\s+', text.strip())
        chunks = [c.strip() for c in chunks if c.strip()]
        
        if not chunks:
            return

        self.audio_queue = queue.Queue()
        playback_thread = threading.Thread(target=self._play_audio_worker)
        playback_thread.start()
        
        module_dir = os.path.dirname(os.path.abspath(__file__))
        
        for i, chunk in enumerate(chunks):
            # print(f"Generating chunk {i+1}/{len(chunks)}...")
            
            final_wav = self.lux_tts.generate_speech(
                chunk, 
                self.encoded_prompt, 
                num_steps=self.num_steps,
                t_shift=self.t_shift,
                speed=self.speed,
                return_smooth=self.return_smooth
            )
            final_wav = final_wav.numpy().squeeze()
            
            temp_file = os.path.join(module_dir, f"temp_speech_{int(time.time())}_{i}.wav")
            sf.write(temp_file, final_wav, 48000)
            
            # Put the generated audio file into the queue for immediate playback
            self.audio_queue.put(temp_file)
            
        # Tell the playback thread to stop after processing all items
        self.audio_queue.put(None)
        
        # Wait for all audio playback to finish before returning to prompt
        playback_thread.join()
