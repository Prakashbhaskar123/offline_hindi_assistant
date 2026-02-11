# intent_engine.py

INTENTS = {
    "TIME": ["समय", "टाइम", "बजे", "घड़ी"],
    "DATE": ["तारीख", "दिनांक", "आज क्या ", "दिन"],
    "GREETING": ["नमस्ते", "हेलो", "सुनो", "सुप्रभात", "राम राम", "हाय"],
    "IDENTITY": ["कौन", "नाम", "पहचान"],
    "STATUS": ["क्या कर ", "काम"],
    "WELL_BEING": ["कैसे ", "क्या हाल "],
    "CREATOR": [" बनाया", "बनाने वाला", "मालिक"],
    "WEATHER": ["मौसम", "बारिश", "धूप"],
    "JOKE": ["चुटकुला", "हंसाओ", "मजाक"],
    "LOCATION": ["कहाँ ", "जगह"],
    "COMPLIMENT": ["अच्छे ", "बढ़िया", "शानदार"],
    "BORED": ["बोर", "अकेला"],
    "CAPABILITIES": ["क्या कर सकते ", "मदद", "फीचर"],
    "LANGUAGE": ["भाषा", "हिंदी", "अंग्रेजी"],
    "FOOD": ["खाना", "भूख", "प्यास"],
    "ADVICE": ["ज्ञान", "सफलता", "टिप"],
    "FEELING_SAD": ["उदास", "दुखी"],
    "LOVE": ["प्यार", "पसंद"],
    "AGE": ["उम्र", "कितने साल"],
    "INTELLIGENCE": ["बुद्धिमान", "तेज", "होशियार"],
    "APPS": ["खोल", "ओपन"],
    "GOOD_NIGHT": ["शुभ रात्रि", "सोने", "नींद"],
    "THANKS": ["धन्यवाद", "शुक्रिया", "थैंक"],
    "HEALTH": ["तबीयत", "सेहत"],
    "EXIT": ["रुको", "बंद", "खत्म", "अलविदा", "बाय"]
}

def detect_intent(text: str) -> str:
    text = text.strip().lower()
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "UNKNOWN"
