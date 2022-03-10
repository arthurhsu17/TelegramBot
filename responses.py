from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello","hi", "sup","hey","hiya"):
        return "Hi there human"

    if user_message in ("who are you","who are you?","who r u",):
        return "I Arthur's Telegram Bot, he made me on the 26th Feb 2022"

    if user_message in ("What is the time?","time?","time","what time is it","time now",):
        now = datetime.now()
        date_time = now.strftime("%d/%m%y, %H:%M:%S")
        return str(date_time)

    if user_message in ("bye","goodbye","cya",):
        return "Ciao friend"

    return "I don't get that command, try something else"