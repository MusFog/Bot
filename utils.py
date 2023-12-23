USER_ID = "user_ids.txt"

def load_user_ids():

    try:
        with open(USER_ID, "r") as file:
            lines = file.readlines()
            return {int(line.split(':')[0]): line.split(':')[1].strip() for line in lines}
    except FileNotFoundError:
        return {}

def save_user_id(user_id, language=None):

    user_data = load_user_ids()
    user_data[user_id] = language or 'None'
    
    with open(USER_ID, "w") as file:
        for uid, lang in user_data.items():
            file.write(f"{uid}:{lang}\n")
