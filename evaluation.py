import pandas as pd
import os
from CAAP import *

if __name__ == "__main__":
    data = []
    for file in os.scandir('evaluation set'):
        if file.is_file() and file.name.endswith(".pdf"):
            information = {"name" : file.name, "keywords" : None, "novice_definitions" : None, "proficient_definitions" : None, "expert_definitions" : None}
            print(file.name)
            path = file.path
            text = process_pdf(path)
            words = get_keywords(text)
            str_words = ""
            for word in words:
                str_words += word + ", "
            str_words = str_words[:-2]
            information["keywords"] = str_words
            for level in range(3):
                definitions = get_definitions(words, level, text)
                str_definitions = ""
                for word, definition, in definitions.items():
                    str_definitions += word + ": " + definition + ", "
                    str_definitions = str_definitions[:-2]
                if level == 0:
                    information["novice_definitions"] = str_definitions
                if level == 1:
                    information["proficient_definitions"] = str_definitions
                if level == 2:
                    information["expert_definitions"] = str_definitions
            data.append(information)
df = pd.DataFrame(data)
df.to_excel('evaluation.xlsx')
# 16385