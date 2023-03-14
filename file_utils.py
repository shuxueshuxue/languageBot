import json

def save_to_json(dict_obj, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(dict_obj, json_file)

def load_from_json(file_path):
    with open(file_path, 'r') as json_file:
        try:
            dict_obj = json.load(json_file)
            return dict_obj
        except Exception:
            return None

if __name__ == "__main__":
    save_to_json([1, 2, 3], "memories/facts.json")
    lst = load_from_json("memories/facts.json")
    print(lst)
