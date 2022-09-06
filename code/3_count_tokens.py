import pandas as pd
import re
from transformers import T5Tokenizer
from tqdm import tqdm

INPUT_PATH = ''
OUTPUT_PATH = ''

def create_instance(docstring, function):
    instance = ''
    if docstring != '':
        instance += '<technical_language>' + docstring + '</technical_language>'

    instance += '<code>' + function + '</code>'
    instance = re.sub('\t', ' ', instance)
    instance = re.sub('\n', ' ', instance)
    instance = re.sub('\r', ' ', instance)
    instance = re.sub('[ ]{2,}', ' ', instance)
    return instance


tokenizer_path = './tokenizer/BPE_Model.model'
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)

df = pd.read_csv(INPUT_PATH)
docstrings = df['cleaned_doc']
functions = df['formatted_function']

instance_length = []
for i in tqdm(range(len(df))):
    doc = docstrings[i]
    function = functions[i]
    instance = create_instance(doc, function)
    tokens_id = tokenizer.encode(instance)
    instance_length.append(len(tokens_id))

df['instance_size'] = instance_length

df.to_csv(OUTPUT_PATH)



