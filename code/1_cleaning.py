import pandas as pd
import re
import regex
from tqdm import tqdm

##########################################################################################################
##########################################################################################################
PATH_DATA = ''
PATH_OUTPUT = ''
##########################################################################################################
##########################################################################################################

def get_doc_without_params(doc):
    all_lines = doc.split('\n')
    no_param_doc = ''
    for s in all_lines:
        if not s.strip().startswith('@'):
            no_param_doc += ' ' + s
        else:
            break
    no_param_sentences = no_param_doc.split('. ')
    sentences = []
    for s in no_param_sentences:
        if s.strip().startswith('/*'):
            s = s[2:].strip()
        if s.strip().startswith('/**'):
            s = s[3:].strip()
        if s.strip().lower().startswith('todo') or\
            s.strip().lower().startswith('* todo'):
            return '. '.join(sentences)
        if s.strip() != '':
            sentences.append(s)
    doc = '. '.join(sentences)
    if doc.strip() == '.':
        return ''   
    return doc

def remove_todos(doc):
    if ' todo:' in doc.lower():
        return doc[:doc.index(' todo:')]
    if ' todo :' in doc.lower():
        return doc[:doc.index(' todo :')]
    if ' todo -' in doc.lower():
         return doc[:doc.index(' todo -')]
    if ' todo ' in doc.lower():
        return doc[:doc.index(' todo ')]
    return doc

# false if string does not contains any letter (e.g., `------------`)
def hasChar(s):
  return bool(regex.search(r'[a-zA-Z]+', s))

# replace bunch of weird characters with proper ones
def replace_math_char(s):
    s = s.replace("`", "").replace("←", "<-").replace("१२", "").replace("⁻⁵", "").replace("•", "") \
            .replace("．", "").replace("￼", "").replace("°", "").replace("»«", "").replace("ｔ", "t") \
            .replace("е", "e").replace("≈", "").replace("⇒", "").replace("¯", "").replace("۸", "").replace("३", "") \
            .replace("‘", "'").replace("➜", "->").replace("≠", "!=").replace("？", "?").replace("¦¦", "") \
            .replace("�", "").replace("ह", "").replace("µ", "mu").replace("с", "c").replace("×", "x") \
            .replace("»", "").replace("²", "").replace('"', '"').replace("ö", "").replace("ô", "").replace("ó", "") \
            .replace("ツ", "").replace("⌘", "").replace("«", "").replace("„", "").replace("·", "").replace("İ", "") \
            .replace("。。。", "...").replace("λ", "lambda").replace("§", "").replace("ø", "").replace("�", "") \
            .replace("￼", "").replace("→", "->").replace("´", "'").replace("…", " ").replace("–", "-") \
            .replace("—", "-").replace("─", "-").replace("’", "'").replace("≤", "<=").replace("≥", ">=") \
            .replace("∞", "inf").replace("±", "+-").replace("“", "\"").replace("”", "\"").replace("└", " ") \
            .replace("├", " ").replace("（", "(").replace("）", ")")
    return s

# replace tags
def replace_tags(s):
    s = s.replace('<!-- begin-user-doc -->','').replace('<!-- end-user-doc -->','').replace('<!-- begin-UML-doc -->','')\
        .replace('<!-- end-UML-doc -->','').replace('<!-- -->','').replace('<!-- @see #setRangeProperties //bad link-->','')\
        .replace('<!-- PENDING -->','')
    return s

# clean sentences from patterns such as {@link NAME} -> replace with NAME only 
def replace_java_link(s):
    if "{@class" in s:
        s_split = s.split("{@class")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@cdk.cite" in s:
        s_split = s.split("{@cdk.cite")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@coe @" in s:
        s_split = s.split("{@coe @")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@code" in s:
        s_split = s.split("{@code")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@Code" in s:
        s_split = s.split("{@Code")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@href" in s:
        s_split = s.split("{@href")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@inheritDoc" in s:
        s_split = s.split("{@inheritDoc")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@ link" in s:
        s_split = s.split("{@ link")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@link" in s:
        s_split = s.split("{@link")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@Link" in s:
        s_split = s.split("{@Link")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@lin" in s:
        s_split = s.split("{@lin")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@llin" in s:
        s_split = s.split("{@lin")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@list" in s:
        s_split = s.split("{@list")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@literal" in s:
        s_split = s.split("{@literal")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@param" in s:
        s_split = s.split("{@param")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@sample" in s:
        s_split = s.split("{@sample")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@see" in s:
        s_split = s.split("{@see")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@scope" in s:
        s_split = s.split("{@scope")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@state" in s:
        s_split = s.split("{@state")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@throws" in s:
        s_split = s.split("{@throws")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@url" in s:
        s_split = s.split("{@url")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    if "{@value" in s:
        s_split = s.split("{@value")
        new_s = s_split[0]
        for i in range(1, len(s_split)):
            s_split[i] = s_split[i].replace('}', ' ', 1)
            new_s +=  s_split[i]
            s = new_s
    s = s.replace('{@inheritDoc}', '').replace('{@inhericDoc}', '').replace('{@inherit-doc}', '')\
        .replace('{@inheritDoc }', '').replace('{@inheritDocs}', '').replace('{@inheritdoc}', '')\
        .replace('{@inheritDpc}', '').replace('{@interitDoc}', '')

    s = s.replace('{@hide', '').replace('{@index', '').replace('{@abc', '')\
        .replace('{@unknownInlineTag','').replace('{@return', '').replace('{@suppress', '')

    s.strip()
    
    elem = s
    new_s = ''
    count = 0
    while '{@' in str(elem):
        if '"{@"' in str(elem):
            break
        count += 1
        start = elem.index('{@')
        try:
            end = elem.index('}')
        except:
            print(s)
            print(elem)
            end = elem.index('}')
        new_s += elem[:start] + elem[start + 2:end]
        elem = elem[end + 1:]
    if count > 0:
        new_s += elem
        s = new_s
    return(s)

# replace links
def replaceLinks(s1, s2):
	link_pattern = regex.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
	matches = [m.group() for m in link_pattern.finditer(s1 + " " + s2)]
	to_replace = set(matches)

	for idx, val in enumerate(to_replace):
		s1 = s1.replace(val, " <LINK_" + str(idx)+ "> ")
		s2 = s2.replace(val, " <LINK_" + str(idx)+ "> ")
	return s1, s2

# not English (Chinese/Russian)
def isNonLatin(s):
	return bool(regex.search(r'[^\x00-\x7F]+', s))

# build list of regex to discard markdown tags
invalid_tags = ["img", "s", "b", "dl", "dd", "i", "sub","sup", "kbd", "code", "CODE", "pre", "a", "hr", "br", "BR", "h1" ,"h2" ,"h3" ,"h4" ,"h5" ,"h6" ,"strong" ,"ul" ,"ol" ,"li" ,"p", "pre","blockquote" ,"em" ,"s" ,"strike", "body" ,"html"]
patterns = []
for tag in invalid_tags:
  patterns.append(regex.compile("<\s*\/?\s*"+tag+"\s*[^>]*\s*>"))

# remove comments from code
def removeComments(s):
  block_comment_pattern = regex.compile(r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/")
  inline_comment_pattern = regex.compile(r"(?<!:)\/\/.*")
  s = block_comment_pattern.sub(r' ', s)
  s = inline_comment_pattern.sub(r' ', s)
  return s

# remove meaningless tokens
def remove_meaningless_tokens(doc, s):
    new_s = ''
    tokens = s.split()
    count_t = 0
    for t in tokens:
        if len(set(t)) == 1 and len(t) > 3 and t[0] in ['<', '>', '~', '!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', '/']:
            count_t += 1
            continue
        new_s += t + ' '
    if count_t > 0:
        f = open('meh_doc.txt', 'a')
        for doc_elem in doc:
            f.write(doc_elem + '. ')
        f.write('\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n')
        f.close()
    return new_s.strip()

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

useless_docs = ['Internal API. Not Stable!.', 'Internal Method. Stay away.', 'Internal. Do not use.', 'Internal. You will not need to use this method.',\
    'Internal. You will not need this.', 'Internal method. Do not use.', 'Internal. You will not need this method.', 'Internal API - subject to change.',\
    'Internal parse method - made protected for unit testing.', 'Internal method. Do not call directly.', 'Internal implementation, normal users should not use it.',\
    'Internally called by JMeter, never call it directly.']

def is_useless_doc(s):
    if s.lower().strip().startswith('internal'):
        if s.split()[0].lower() != 'internal':
            return True
        if s in useless_docs:
            return True
        return False
    if s.lower().strip().startswith('<!--workaround-->'):
        return True
    if s.lower().strip().startswith('<?xml'):
        return True
    if s.lower().strip().startswith('<xsl'):
        return True
    if s.lower().strip().startswith('<tested xml'):
        return True
    if s.lower().strip().startswith('<!-- c'):
        return True
    if s.lower().strip().startswith('<xsd'):
        return True
    if s.lower().strip().startswith('<!-- begin-model-doc -->'):
        return True
    if '<!-- options -->' in s:
        return True
    if '<!-- description -->' in s:
        return True
    return False

def is_empty_strange_method(method):
    try:
        m_split = method.split('{')[1]
    except:
        return False, True
    if m_split.strip() == '}':
        return True, False
    return False, False

def is_method(method):
    if method.strip()[-1] == '}':
        return True
    return False

def is_test(method):
    if '@test' in method.lower():
        return True
    return False

def is_reminder(doc):
    if doc.strip().lower().startswith('remind'):
        return True
    return False

##########################################################################################################
##########################################################################################################


cleaned_doc_summary = []
cleaned_functions = []

# load data
print('loading data...')
df_all = pd.read_csv(PATH_DATA)
print('starting data: ', len(df_all))
df_all.drop_duplicates(inplace=True)

functions = list(df_all['method'])
docstrings = list(df_all['cleaned_docstrings'])
cleaned_doc = []

print('Java methods cleaning...')
indexes_to_remove = []

empty_method = 0
not_a_method = 0
test_method = 0
# remove comments from functions
for i in tqdm(range(len(functions))):
    f = functions[i]
    f = removeComments(f)
    flag1, flag2 = is_empty_strange_method(f)
    if flag1:
        indexes_to_remove.append(i)
        cleaned_functions.append('')
        empty_method += 1
        continue
    if flag2:
        indexes_to_remove.append(i)
        cleaned_functions.append('')
        not_a_method += 1
        continue
    if not is_method(f):
        indexes_to_remove.append(i)
        cleaned_functions.append('')
        not_a_method += 1
        continue
    if is_test(f):
        indexes_to_remove.append(i)
        cleaned_functions.append('')
        test_method += 1
        continue
    cleaned_functions.append(f)

print('empty methods      : ', empty_method)
print('not correct method : ', not_a_method)
print('test methods       : ', test_method)

##########################################################################################################
##########################################################################################################

indexes_to_check = list(set(range(len(docstrings))) - set (indexes_to_remove))

empty_doc_summary = 0
useless_doc = 0
not_latin_doc = 0

print('Javadoc comments cleaning...')
for i in tqdm(indexes_to_check):
    current_doc = str(docstrings[i])
    if current_doc == 'nan' or current_doc == '':
        indexes_to_remove.append(i)
        empty_doc_summary += 1
        continue
    if current_doc.strip().endswith('}'):
        indexes_to_remove.append(i)
        useless_doc += 1
        continue
    # remove params
    current_doc = get_doc_without_params(current_doc)
    # replace links
    current_doc, cleaned_functions[i] = replaceLinks(current_doc, cleaned_functions[i])
    # discard markdown from string
    for pattern in patterns:
        current_doc = pattern.sub(r' ', current_doc)
    # replace bunch of weird characters with proper ones
    current_doc = replace_math_char(current_doc)
    # replace Java links {@class class_name}
    current_doc = replace_java_link(current_doc)
    # replace some tags
    current_doc = replace_tags(current_doc)

    # remove empty docstrings after cleaning
    if current_doc.strip() == '':
        indexes_to_remove.append(i)
        empty_doc_summary += 1
        continue
    # meaningless sentences (e.g., "-------")
    if not hasChar(current_doc):
        useless_doc.append(current_doc)
        indexes_to_remove.append(i)
        continue
    if is_useless_doc(current_doc):
        indexes_to_remove.append(i)
        useless_doc += 1
        continue
    # remove not latin languages
    if isNonLatin(current_doc):
        not_latin_doc.append(current_doc)
        indexes_to_remove.append(i)
        continue
    if is_reminder(current_doc):
        indexes_to_remove.append(i)
        useless_doc += 1
        continue

    cleaned_doc.append(current_doc)

###############################################################
df = pd.DataFrame({
    'function' : cleaned_functions,
    'docstring' : docstrings
})
df.drop(index=indexes_to_remove, axis=0, inplace=True)

cleaned_functions = list(df['function'])
docstrings = list(df['docstring'])
###############################################################

# split doc summary in sentences
doc_summary_sentences = [doc.split('. ') for doc in cleaned_doc]

# clean sentences
for doc in tqdm(doc_summary_sentences):
    cleaned_sentences = []
    for s in doc:
        # ignore empty line
        if s.strip() == '' or s.strip() == '.':
            continue
        # remove meaningless tokens
        s = remove_meaningless_tokens(doc, s)
        s = " ".join(s.split())
        # check if empty sentence
        if s.strip() == '':
            continue
        cleaned_sentences.append(s.strip())
    cleaned_doc_summary.append(cleaned_sentences)

# remove empty and strange doc summary 
empty_doc_summary_instances = []
strange_doc_count = 0
for i in tqdm(range(len(cleaned_doc_summary))):
    if len(doc_summary_sentences[i]) == 0:
        empty_doc_summary_instances.append(i)
        continue
    if str(current_doc.strip()).startswith('$ANTLR'):
        empty_doc_summary_instances.append(i)
        strange_doc_count += 1
        continue
    
empty_doc_summary += len(empty_doc_summary_instances)
empty_doc_summary -= strange_doc_count

###############################################################
df = pd.DataFrame({
    'function' : cleaned_functions,
    'docstring' : docstrings,
    'cleaned_doc' : cleaned_doc_summary
})

df.drop(index=empty_doc_summary_instances, axis=0, inplace=True)

cleaned_functions = list(df['function'])
docstrings = list(df['docstring'])
cleaned_doc_summary = list(df['cleaned_doc'])


# put sentences together and create a single string for the doc summary
for i in tqdm(range(len(cleaned_doc_summary))):
    for j in range(len(cleaned_doc_summary[i])):
        cleaned_doc_summary[i][j] = cleaned_doc_summary[i][j].strip()

    cleaned_doc_summary[i] = '. '.join(cleaned_doc_summary[i]).strip()
    while cleaned_doc_summary[i].startswith('*') or\
        cleaned_doc_summary[i].startswith('/') or\
        cleaned_doc_summary[i].startswith('-'):
        cleaned_doc_summary[i] = cleaned_doc_summary[i][1:].strip()
    if cleaned_doc_summary[i].endswith(' .'):
        cleaned_doc_summary[i] = cleaned_doc_summary[i][-1].strip() + '.'
    if not cleaned_doc_summary[i].endswith('.'):
        cleaned_doc_summary[i] = cleaned_doc_summary[i].strip() + '.'

# remove short doc summary
short_doc_indexes = []
for i in tqdm(range(len(cleaned_doc_summary))):
    s = str(cleaned_doc_summary[i])
    while s.strip().endswith('.'):
        s = s.strip()[:-1]
    if len(s.split()) < 4:
        short_doc_indexes.append(i)

###############################################################
df = pd.DataFrame({
    'function' : cleaned_functions,
    'docstring' : docstrings,
    'cleaned_doc' : cleaned_doc_summary
})

print('data before removing useless instances:', len(df))
df.drop(index=short_doc_indexes, axis=0, inplace=True)
print('data after:', len(df))
df.drop_duplicates(inplace=True)
print('without duplicates:', len(df))

cleaned_functions = list(df['function'])
docstrings = list(df['docstring'])
cleaned_doc_summary = list(df['cleaned_doc'])
###############################################################

print('create instances with javadoc and method code...')
# create instances
all_instances = []
for i in tqdm(range(len(cleaned_functions))):
    all_instances.append(create_instance(cleaned_doc_summary[i], cleaned_functions[i]))

print('not Latin Javadocs : ', len(not_latin_doc))
print('empty Javadocs     : ', empty_doc_summary)
print('short Javadocs     : ', len(short_doc_indexes))
print('-----------------------------------------')
print('final instances    : ', len(all_instances))

df['instance'] = all_instances

df.to_csv(PATH_OUTPUT)
print('cleaning done!')
print(len(df))



