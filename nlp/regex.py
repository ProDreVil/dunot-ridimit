import re

def detect_regex(message):
    message = message.lower().strip()
    patterns = {
        "yes": r"^(yes|yeah|yep|yup|sure|correct|alright|okay|ok)( sir| please)?[.!]?$",
        "no": r"^(no|nope|nah|never|not really|i don't think so)( sir| please)?[.!]?$",
        "solution": r"^(how|what)\b.*\b(do|fix|solve|handle|need to do)\b.*$",
        "question": r"^(what|why|how|when|where|who|can|could|should|do|does|is|are)\b.*\??$",
        "request": r"^(please\s+)?(help|assist|tell|show|explain|give|provide)\b.*$",
        "explanation": r"^(what is|what's|what does|what do you mean|what was)\b.*$",
        "reason": r"^(why|how come)\b.*$",
        "danger": r"^(is it|is this|can it|could it)\b.*(dangerous|harmful|safe|danger|harm).*$",
        "confirmation": r"^(are you sure|is that true|really|seriously)\b.*$"
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