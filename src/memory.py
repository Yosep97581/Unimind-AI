MAX_HISTORY = 6


def get_recent_history(messages):
    return messages[-MAX_HISTORY:]

