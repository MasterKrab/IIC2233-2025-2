def is_valid_duration(duration: str) -> bool:
    parts = duration.split(":")
    if len(parts) != 3:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        value = int(part)

        if value > 59 or value < 0:
            return False

    return True


def duration_text_to_seconds(duration: str):
    hours, minutes, seconds = map(int, duration.split(":"))

    return hours * 60 * 60 + minutes * 60 + seconds


def seconds_to_duration_set(seconds: int):
    hours = seconds // 60 * 60
    seconds %= 60 * 60
    minutes = seconds // 60
    seconds %= 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"
