import os
import time
import soundfile as sf
from zipvoice.luxvoice import LuxTTS

class StreamJarvisTTS:
    """
    A class for Text-to-Speech using LuxTTS.
    """
    def __init__(self, 
                 model_name='YatharthS/LuxTTS', 
                 device='mps', # mps or cpu
                 prompt_audio='modules/sample.mp3', # sample voice of jarvis
                 rms=0.01, 
                 ref_duration=5,
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

    def speak(self, text):
        """
        Generates audio for the entire text, saves it to a file, plays it, and deletes it.
        """
        if not text.strip():
            return
            
        print("Generating audio...")
        
        # Generate speech for the full text at once
        final_wav = self.lux_tts.generate_speech(
            text, 
            self.encoded_prompt, 
            num_steps=self.num_steps,
            t_shift=self.t_shift,
            speed=self.speed,
            return_smooth=self.return_smooth
        )
        final_wav = final_wav.numpy().squeeze()
        
        # Save to a temporary file inside the module's directory
        module_dir = os.path.dirname(os.path.abspath(__file__))
        temp_file = os.path.join(module_dir, f"temp_speech_{int(time.time())}.wav")
        sf.write(temp_file, final_wav, 48000)
        
        # Play the file using macOS afplay (synchronous)
        os.system(f"afplay {temp_file}")
        
        # Delete the file after playing
        try:
            os.remove(temp_file)
        except OSError:
            pass
