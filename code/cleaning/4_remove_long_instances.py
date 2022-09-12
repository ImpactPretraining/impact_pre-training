import pandas as pd
from tqdm import tqdm

INPUT_DATA = ''
OUTPUT_DATA = ''

df = pd.read_csv(INPUT_DATA)
print(len(df))
print(df.columns)

doc_summary = df['cleaned_doc']
functions = df['formatted_function']
instances = df['instance']
instances_length = df['instance_size']
function_ids = df['formatted_function_id']
print(len(doc_summary))
print(len(functions))
print(len(instances))
print(len(instances_length))
print(len(function_ids))

good_docs = []
good_functions = []
good_instances = []
good_function_ids = []

for i in tqdm(range(len(instances_length))):
    if int(instances_length[i]) < 513:
        good_docs.append(doc_summary[i])
        good_functions.append(functions[i])
        good_instances.append(instances[i])
        good_function_ids.append(function_ids[i])

df_good = pd.DataFrame({
    'formatted_function_id' : good_function_ids,
    'docstring' : good_docs,
    'function' : good_functions,
    'instance' : good_instances
})

print('good_data:', len(df_good))
df_good.to_csv(OUTPUT_DATA)
