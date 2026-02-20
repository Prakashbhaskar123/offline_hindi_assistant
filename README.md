# 🗣️ Offline,  Hindi Voice Assistant on Raspberry Pi
## BHARATH AI-SoC  Student Challenge

---
## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Objective](#-objective)
- [System Architecture](#-system-architecture)
  - [High-Level Pipeline](#-1️⃣-high-level-embedded-speech-pipeline)
  - [Privacy & Data Flow](#-2️⃣-data-flow-diagram)
  - [ARM CPU Optimization](#-3️⃣-arm-cpu-optimization-flow)
  - [Software Architecture](#-4️⃣-software-architecture-diagram)
- [Hardware Used](#-hardware-used)
- [Software Stack](#-software-stack)
- [Core Implementation Details](#-core-implementation-details)
  - [Speech-to-Text (ASR)](#-🔷-1️⃣-speech-to-text-(asr))
  - [Intent Recognition](#-🔷-2️⃣-intent-recognition)
  - [Text-to-Speech (TTS)](#-🔷-3️⃣-text-to-speech-(tts))
- [ARM CPU Optimization Techniques](#-arm-cpu-optimization-techniques)
- [Performance Results](#-performance-results)
- [Privacy-Preserving Design](#-privacy-preserving-design)
- [Repository Structure](#-repository-structure)
- [Setup & Execution](#-setup--execution)
- [Deliverables](#-deliverables-included)
- [Learning Outcomes](#-learning-outcomes)
- [Conclusion](#-conclusion)



## 📌 Problem Statement

Develop a low-latency, privacy-preserving voice assistant on an Arm-based SBC (Raspberry Pi 4) that processes Hindi voice commands entirely offline.

The assistant must:

* Operate fully on CPU
* Avoid cloud dependency
* Support local Hindi queries (time, date, greetings, etc.)
* Maintain low response latency

---

## 🎯 Objective

To design and implement an embedded speech pipeline on Raspberry Pi that:

* Captures Hindi voice input
* Converts speech to text using offline ASR
* Identifies user intent using Python logic
* Generates spoken responses using offline TTS
* Runs completely on ARM CPU without accelerators

---

# 🧱 System Architecture

## 🔷 1️⃣ High-Level Embedded Speech Pipeline

```
+----------------------+
|      User (Hindi)    |
+----------+-----------+
           |
           v
+----------------------+
|    USB Microphone    |
+----------+-----------+
           |
           v
+----------------------+
|  Audio Capture       |
|  (PyAudio - 16kHz)   |
+----------+-----------+
           |
           v
+-------------------------------+
|  Offline ASR Engine           |
|  (Wav2Vec2 - Quantized INT8)  |
+----------+--------------------+
           |
           v
+-------------------------------+
|  Intent Recognition Engine    |
|  (Rule-Based Python Logic)    |
+----------+--------------------+
           |
           v
+-------------------------------+
|  Command Processing Layer     |
+----------+--------------------+
           |
           v
+-------------------------------+
|  Offline TTS Engine           |
|  (eSpeak-NG Hindi)            |
+----------+--------------------+
           |
           v
+----------------------+
|      Speaker Output  |
+----------------------+
```

✔ Entire pipeline runs on Raspberry Pi CPU
✔ No internet
✔ No cloud

---

## 🔷 2️⃣ Data Flow Diagram

```
        Voice Input
             |
             v
    +-------------------+
    |   Local ASR       |
    |  (On Device)      |
    +-------------------+
             |
             v
    +-------------------+
    | Intent Detection  |
    +-------------------+
             |
             v
    +-------------------+
    |  Local TTS        |
    +-------------------+
             |
             v
        Audio Output
```

🚫 No external servers
🚫 No API calls
🚫 No cloud processing

---

## 🔷 3️⃣ ARM CPU Optimization Flow

```
Model Loading
      |
      v
Dynamic Quantization (INT8)
      |
      v
CPU Inference Only
      |
      v
Low-Latency Response
```

✔ Optimized for ARM Cortex-A72
✔ No accelerators
✔ CPU-only execution

---

## 🔷 4️⃣ Software Architecture Diagram

```
Assistant.py
     |
     +-- record_audio()
     |
     +-- ASR Inference (Wav2Vec2)
     |
     +-- process_command()
             |
             +-- intent_engine.detect_intent()
     |
     +-- speak()  --> eSpeak-NG
```

---


### 🔷 End-to-End Embedded Pipeline

```
User (Hindi Speech)
        ↓
USB Microphone
        ↓
Audio Capture (PyAudio, 16kHz)
        ↓
Wav2Vec2 ASR Model (Offline, Quantized)
        ↓
Intent Recognition Engine (Python)
        ↓
Command Processing
        ↓
eSpeak-NG (Offline TTS)
        ↓
Speaker Output
```

✔ Entire pipeline runs locally on Raspberry Pi CPU
✔ No internet access required

---

## 🛠 Hardware Used

* Raspberry Pi 4 (ARM Cortex-A72)
* USB Microphone
* Speaker (3.5 mm Jack)
* 32GB SD Card

The system is designed to run entirely on CPU without external accelerators.

---

## 💻 Software Stack

* Python 3
* PyAudio (Audio I/O)
* HuggingFace Transformers
* Fine-tuned Wav2Vec2 (Hindi ASR)
* eSpeak-NG (Hindi TTS)
* Custom Intent Recognition Engine

---

## 🧠 Core Implementation Details

### 1️⃣ Speech-to-Text (ASR)

* Hindi Wav2Vec2 model
* Loaded locally using `local_files_only=True`
* Dynamic INT8 Quantization applied
* Optimized for ARM CPU inference

```python
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

---

### 2️⃣ Intent Recognition

Lightweight keyword-based rule engine:

```
TIME → ["समय", "टाइम"]
DATE → ["तारीख", "दिनांक"]
GREETING → ["नमस्ते", "हेलो"]
...
```

* No heavy NLP models
* Fast CPU execution
* Low memory overhead

---

### 3️⃣ Text-to-Speech (TTS)

* eSpeak-NG (Hindi phoneme support)
* Fully offline
* Subprocess-based execution

---

## ⚡ ARM CPU Optimization Techniques

To ensure efficient execution on ARM CPU:

* ✅ Dynamic Quantization (INT8)
* ✅ Silence detection before inference
* ✅ Controlled audio frame buffering
* ✅ Lightweight intent recognition
* ✅ CPU-only execution (no accelerators)

This aligns with ARM Challenge emphasis on CPU optimization.

---

## 📊 Performance Results

Tested with 15 standard Hindi commands:

| Metric            | Result     |
| ----------------- | ---------- |
| Average Latency   | ~3 seconds |
| Word Error Rate   | ~15%       |
| CPU Peak Usage    | ~85%       |
| RAM Usage         | ~1.2 GB    |
| Offline Operation | 100%       |

The system meets the requirement of robust offline execution and supports more than 10 Hindi commands.

---

## 🔐 Privacy-Preserving Design

The assistant ensures data sovereignty by:

* No internet usage
* No API keys
* No cloud processing
* No data logging
* All inference done locally

```
Voice → Local ASR → Local Intent Logic → Local TTS
```

---

## 📂 Repository Structure

```
├── Assistant.py
├── intent_engine.py
├── ASR_model/
├── Documentation.docx
├── Report_on_ARM_Challenge.pdf
└── README.md
```

---

## ▶️ Setup & Execution

### Clone Repository

```
git clone <repo-link>
cd <repo-name>
```

### Install Dependencies

```
pip install torch transformers pyaudio numpy
sudo apt install espeak-ng
```

### Run Assistant

```
python Assistant.py
```

---

## 🎥 Deliverables Included

* ✅ Complete source code
* ✅ Documentation
* ✅ Optimization details
* ✅ Performance metrics
* ✅ ARM-based implementation
* ✅ Offline operation proof

---

## 📘 Learning Outcomes

* Embedded Speech AI implementation
* ARM CPU optimization for ML inference
* Hindi ASR challenges
* Integrating ASR + NLP + TTS on constrained hardware
* Edge AI deployment without cloud

---

## 🏁 Conclusion

This project successfully demonstrates a fully offline, privacy-preserving Hindi voice assistant running entirely on ARM-based Raspberry Pi CPU. Through model quantization and lightweight intent recognition, the system achieves efficient on-device inference without cloud dependency, fulfilling the requirements of ARM Challenge Problem Statement 1.

---
