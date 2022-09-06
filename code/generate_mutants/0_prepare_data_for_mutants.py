import pandas as pd
from tqdm import tqdm

INPUT_PATH = ''
OUTPUT_FOLDER_PATH = ''

df = pd.read_csv(INPUT_PATH)
functions = list(df['function'])
print('functions: ', len(functions))


for i in tqdm(range(len(functions))):
    f = open(OUTPUT_FOLDER_PATH + '/function_' + str(i) + '.txt', 'w')
    f.write(functions[i])
    f.close()

print('done!')
