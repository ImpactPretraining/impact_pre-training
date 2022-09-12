import pandas as pd
from tqdm import tqdm

from langdetect import detect, DetectorFactory  
from langid.langid import LanguageIdentifier, model

identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
import cld3


OUTPUT_PATH = ''
INPUT_PATH = ''

def isEnglish_strong(doc):
    try:
        langid_prediction = identifier.classify(doc)
        cld3_prediction = cld3.get_language(doc)

        if langid_prediction[0] == "en" and langid_prediction[1] > 0.8 and\
            cld3_prediction.language == "en" and cld3_prediction.is_reliable and\
            detect(doc) == "en":
            return True
        return False
    except:
        print('LANG ISSUE (strong):')
        print(doc + '\n----------\n')
    return False

df = pd.read_csv(INPUT_PATH)
docstrings = list(df['cleaned_doc'])
print('data: ', len(docstrings))

is_english = []
for elem in tqdm(docstrings):
    first_sentence = elem.split('. ')[0]
    if isEnglish_strong(first_sentence):
        is_english.append(True)
    else:
        is_english.append(False)

not_english = sum([1 for elem in is_english if not elem])
english = sum([1 for elem in is_english if elem])

print('not english:', not_english)
print('english    :', english)

df['is_english'] = is_english

df.to_csv(OUTPUT_PATH)
