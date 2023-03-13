import json

def save_dict_to_json(dict_obj, file_path):
    """Save a dictionary object as a .json file."""
    with open(file_path, 'w') as json_file:
        json.dump(dict_obj, json_file)

def load_dict_from_json(file_path):
    """Load a .json file as a dictionary object."""
    with open(file_path, 'r') as json_file:
        dict_obj = json.load(json_file)
        return dict_obj

if __name__ == "__main__":
    dic = load_dict_from_json("settings.json")
    print(dic)
