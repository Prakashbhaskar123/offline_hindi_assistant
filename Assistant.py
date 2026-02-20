import os
import sys
import time
import torch
import pyaudio
import numpy as np
import subprocess
import datetime
import intent_engine
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# --- SUPPRESS ALSA ERRORS ---

from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt): pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
try:
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except: pass


# --- CONFIGURATION ---
MODEL_ID = "theainerd/Wav2Vec2-large-xlsr-hindi"
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 900
SILENCE_LIMIT = 10


# --- TTS & LOGIC ---
def speak(text):
    print(f"Assistant: {text}")
    subprocess.call(['espeak-ng', '-v', 'hi', '-s', '150', text])

def get_time_in_hindi():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    period = "सुबह" if 5 <= hour < 12 else "दोपहर" if 12 <= hour < 17 else "शाम" if 17 <= hour < 21 else "रात"
    if hour > 12: hour -= 12
    elif hour == 0: hour = 12
    return f"अभी {period} के {hour} बजकर {minute} मिनट हुए हैं"

def get_date_in_hindi():
    now = datetime.datetime.now()
    return f"आज की तारीख है {now.day} {now.strftime('%B')} {now.year}"


def process_command(text):
    # Detect the intent using our external engine
    intent = intent_engine.detect_intent(text)
    
    # Map the detected intent to the exact strings you provided
    responses = {
        "IDENTITY": "मैं आपका हिंदी वॉइस असिस्टेंट हूँ, जिसे पायथन और वेव-टू-वेक मॉडल से बनाया गया है।",
        "TIME": get_time_in_hindi(),
        "DATE": get_date_in_hindi(),
        "STATUS": "मैं आपके निर्देशों का इंतज़ार कर रहा हूँ और आपकी मदद के लिए तैयार हूँ।",
        "GREETING": "नमस्ते! बताइए, मैं आपकी क्या मदद कर सकता हूँ?",
        "WELL_BEING": "मैं बिल्कुल ठीक हूँ, शुक्रिया! आप कैसे हैं?",
        "CREATOR": "मुझे मेरे डेवलपर ने ऑफलाइन हिंदी बातचीत के लिए बनाया है।",
        "WEATHER": "अभी मेरे पास मौसम की जानकारी के लिए इंटरनेट एक्सेस नहीं है, पर बाहर खिड़की से देख लीजिए!",
        "JOKE": "सॉफ्टवेयर इंजीनियर को चाय क्यों पसंद है? क्योंकि उसमें 'टी' (Tea) होती है और कोड में 'बग'!",
        "LOCATION": "मैं आपके कंप्यूटर के अंदर एक सुरक्षित फोल्डर में बैठा हूँ।",
        "COMPLIMENT": "तारीफ के लिए बहुत-बहुत धन्यवाद! सुनकर अच्छा लगा।",
        "BORED": "चिंता न करें, मैं यहाँ हूँ। चलिए कुछ और बातें करते हैं या कोई कमांड आज़माते हैं।",
        "CAPABILITIES": "मैं समय बता सकता हूँ, तारीख बता सकता हूँ, चुटकुले सुना सकता हूँ और आपसे बातें कर सकता हूँ।",
        "LANGUAGE": "मैं फिलहाल सिर्फ हिंदी समझता और बोलता हूँ।",
        "FOOD": "मुझे बिजली और डेटा की भूख लगती है, पर आपके लिए दाल-चावल बढ़िया रहेगा।",
        "ADVICE": "कड़ी मेहनत और निरंतरता ही सफलता की कुंजी है। कोडिंग करते रहें!",
        "FEELING_SAD": "उदास मत होइए, एक गहरी सांस लीजिए। सब ठीक हो जाएगा।",
        "LOVE": "एक मशीन होने के नाते, मुझे इंसानों से बात करना बहुत पसंद है।",
        "AGE": "जब आपने इस स्क्रिप्ट को रन किया, तब मेरा जन्म हुआ।",
        "INTELLIGENCE": "यह सब आपके द्वारा लिखे गए कोड का कमाल है।",
        "APPS": "मैं अभी ऐप्स खोलने के लिए कॉन्फ़िगर नहीं किया गया हूँ, पर भविष्य में यह कर पाऊँगा।",
        "GOOD_NIGHT": "शुभ रात्रि! अच्छे सपने देखिये।",
        "THANKS": "आपका स्वागत है! मुझे आपकी मदद करके खुशी हुई।",
        "HEALTH": "मेरा प्रोसेसर बिल्कुल ठंडा है और सिस्टम सुचारू रूप से चल रहा है।",
        "EXIT": "EXIT"
    }

    # If the intent is found, return the string. Otherwise, return the fallback.
    return responses.get(intent, f"माफ कीजिये, मुझे इसका उत्तर नहीं पता। मैंने सुना: {text}")
    
# --- MODEL & INFERENCE ---
def load_model():
    print("Loading Offline Model...")
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID, local_files_only=True)
    model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID, local_files_only=True)
    model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    model.eval()
    return processor, model

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("\n[LISTENING]")
    frames, silent_chunks, started = [], 0, False
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        if np.abs(audio_data).mean() > SILENCE_THRESHOLD:
            started = True
            silent_chunks = 0
        elif started:
            silent_chunks += 1
        if started: frames.append(audio_data.astype(np.float32))
        if (started and silent_chunks > SILENCE_LIMIT) or len(frames) > 95: break
    stream.stop_stream(); stream.close(); p.terminate()
    return np.concatenate(frames) if frames else None

if __name__ == "__main__":
    proc, mdl = load_model()
    speak("नमस्कार, सिस्टम तैयार है")
    while True:
        audio = record_audio()
        if audio is not None:
            audio_norm = audio / (np.max(np.abs(audio)) + 1e-7)
            inputs = proc(audio_norm, sampling_rate=RATE, return_tensors="pt").input_values
            with torch.inference_mode():
                logits = mdl(inputs).logits
            user_text = proc.batch_decode(torch.argmax(logits, dim=-1))[0]
            if user_text.strip():
                print(f"USER: {user_text}")
                res = process_command(user_text)
                if res == "EXIT":
                    speak("अलविदा"); break
                speak(res)
