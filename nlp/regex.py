import re

def detect_regex(message):
    message = message.lower().strip()
    patterns = {
        "yes": r"^(yes|yeah|yep|yup|sure|correct|alright|okay|ok)( sir| please)?[.!]?$",
        "no": r"^(no|nope|nah|never|not really|i don't think so)( sir| please)?[.!]?$",
        "question": r"^(what|why|how|when|where|who|can|could|should|do|does|is|are)\b.*\??$",
        "request": r"^(please\s+)?(help|assist|tell|show|explain|give|provide)\b.*$"
    }
    for intent, pattern in patterns.items():
        if re.fullmatch(pattern, message):
            return intent
    return None

def extract_number(message):
    match = re.search(r"\b\d+(?:\.\d+)?\b", message)
    if match:
        return match.group()
    return None

def extract_money(message):
    match = re.search(
        r"(?:₱|\$|php|usd)\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*(?:pesos?|dollars?)",
        message,
        re.IGNORECASE
    )
    if match:
        return match.group()
    return None