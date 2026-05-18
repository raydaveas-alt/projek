# save
import json

def save_game(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# load
def load_game(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# ini belum jadi sih 🗿