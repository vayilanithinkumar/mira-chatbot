import re

def extract_session_id(session_str: str):
    match = re.search(r"sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1) #in re expressions group(0) having the whole sessions and contexts but we don't won't that we need only session_id that's why we are using group(1)
        return extracted_string

    return ""

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
