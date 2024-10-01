import json
import pandas as pd

def json_to_csv(json_file_path, save_csv_path):
    line_number = 0

    try:
        with open(json_file_path) as f:
            df = pd.DataFrame()
            for line in f:
                dict = json.loads(line.strip())
                new_df = pd.DataFrame([dict])
                df = pd.concat([df, new_df])
                line_number += 1
            df.to_csv(save_csv_path, index=False)
    except Exception as e:
        print(e,'on line number', line_number)
if __name__=='__main__':
    json_to_csv()
