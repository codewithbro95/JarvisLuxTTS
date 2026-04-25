# Jarvis Voice Module

The dedicated Text-to-Speech (TTS) voice module for the overall [JARVIS](https://github.com/codewithbro95/JARVIS) project. 

This repository is a customized adaptation of the highly efficient [LuxTTS by YatharthS](https://github.com/ysharma3501/LuxTTS). It serves as a lightweight, plug-and-play module built to provide high-quality tts for the larger JARVIS ecosystem.

## ✨ Features
- **Plug-and-Play Module:** A self-contained, object-oriented module designed to be easily imported and used anywhere in the main JARVIS codebase.
- **Auto-Cleanup:** Audio files are generated, played synchronously, and automatically deleted to keep the system clean without leaving temp files behind (still need to figure out a way to stream the audio as it is generated)
- **High-Quality Voice:** Retains LuxTTS's state-of-the-art voice cloning capabilities with crisp 48khz speech generation.
- **Speed:** Reaches lightning-fast speeds (150x real-time) on GPUs and is heavily optimized for Apple Silicon (MPS).

## 🚀 Usage

### 1. Installation
Clone this repository and install the required dependencies:
```bash
git clone https://github.com/codewithbro95/JarvisLuxTTS.git
cd JarvisLuxTTS
pip install -r requirements.txt
```

### 2. Testing the Module
This repository includes a `main.py` script to easily test the voice module on the fly:
```bash
python main.py
```
This will run a sample interactive loop where you can type prompts and hear JARVIS speak to verify the module is working correctly.

### 3. Module Integration
To use this within the larger JARVIS architecture, simply import the TTS engine:
```python
from modules.audio import StreamJarvisTTS

jarvisTTS = StreamJarvisTTS()
jarvisTTS.speak("All systems are online. How may I be of service?")
```

## 📜 Acknowledgments
- Adapted from the original [LuxTTS](https://github.com/ysharma3501/LuxTTS) repository by YatharthS.
- Core architecture derived from [ZipVoice](https://github.com/k2-fsa/ZipVoice) and [Vocos](https://github.com/gemelo-ai/vocos.git).


