def extract_state(text: str) -> str:
    return text.split(" ")[::-1][1].strip().upper()
