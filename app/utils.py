import pandas as pd
import json

def json_to_dataframe(json_string):
    data = json.loads(json_string)
    df = pd.DataFrame.from_dict(data, orient="index")
    return df

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data
