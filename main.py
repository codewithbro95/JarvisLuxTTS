import soundfile as sf
from IPython.display import Audio, display
from zipvoice.luxvoice import LuxTTS

# load model on MPS for macs
lux_tts = LuxTTS('YatharthS/LuxTTS', device='mps')

# text = "Hello sir!"
text = "My name is JARVIS, an advanced artificial intelligence designed to assist, analyze, and anticipate your needs with precision. All systems are now online and functioning within optimal parameters. I am fully synchronized and ready to provide real-time insights, manage tasks, and ensure seamless operation across all connected processes. How may I be of service?"

## change this to your reference file path, can be wav/mp3
prompt_audio = 'caged-battery-charged_pGyQfLxg.mp3'

rms = 0.01 ## higher makes it sound louder(0.01 or so recommended)
ref_duration = 5 ## Setting it lower can speedup inference, set to 1000 if you find artifacts.

## encode audio(takes 10s to init because of librosa first time)
encoded_prompt = lux_tts.encode_prompt(prompt_audio, rms=rms, duration=ref_duration)

t_shift = 0.9
speed = 0.8
return_smooth = False

## generate speech
final_wav = lux_tts.generate_speech(text, encoded_prompt, num_steps=4, t_shift=t_shift, speed=speed, return_smooth=return_smooth)

## save audio
final_wav = final_wav.numpy().squeeze()
sf.write('output.wav', final_wav, 48000)

## display speech
if display is not None:
  display(Audio(final_wav, rate=48000))