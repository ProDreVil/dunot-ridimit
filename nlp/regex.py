import re

def detect_regex(message):
    message = message.lower().strip()
    patterns = {
        "yes": r"^(yes|yeah|yep|yup|sure|correct|alright|okay|ok|of course|absolutely|certainly|that's right|that is right)( sir| please)?[.!]?$",
        "no": r"^(no|nope|nah|never|not really|i don't think so|not at all|of course not|absolutely not|i refuse)( sir| please)?[.!]?$",
        "solution": r"^(how|what|where|you should|can you|please)\b.*\b(do|fix|solve|handle|deal with|remove|repair|resolve|need to do|should i do|instructions|steps|proceed)\b.*$",
        "question": r"^(what|why|how|when|where|who|can|could|should|do|does|is|are|will|would)\b.*\??$",
        "request": r"^(please\s+)?(can you|could you|would you|will you|please|help|assist|tell|show|explain|give|provide)\b.*$",
        "explanation": r"^(what is|what's|what does|what do you mean|what was|what happened|what's wrong|what is wrong|can you explain|could you explain|tell me what|tell me about)\b.*$",
        "reason": r"^(why|how come|what caused|what causes)\b.*$",
        "danger": r"^(is it|is this|can it|could it|will it|would it)\b.*(dangerous|harmful|safe|danger|harm|damage|hurt).*$",
        "confirmation": r"^(are you sure|is that true|is that correct|really|seriously|are you certain|can you confirm)\b.*$",
        "problem": r"^(my|the)\s+(computer|pc|system|device)\b.*(slow|freez|crash|stuck|hang|popup|pop-up|error|broken|not working|not responding|weird|strange|acting up).*$|^(slow|freezing|frozen|crashing|stuck|broken|not working|not responding|lots of popups|weird messages)\b.*$"
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