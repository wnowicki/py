import json


def load(file="config.json"):
    with open(file, 'r') as content_file:
        return json.load(content_file)


if __name__ == "__main__":
    conf = load('config.json')
    print(conf)
