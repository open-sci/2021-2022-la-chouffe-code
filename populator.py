from stats import get_all_in_dir
import json
import pandas as pd
from os import makedirs, sep
import os
from tqdm import tqdm
journals = dict()
with open('cleanJournalsDump.json', 'r') as input:
     journals = json.load(input)
dir = get_all_in_dir('results','csv')
df = pd.DataFrame()
for file in dir:
    df = df.append(pd.read_csv(file, encoding='utf8'))
my_issn = set(df.issn)

batch_num = 0
df = df.set_index('issn')
for issn in tqdm(my_issn):
    out = df[df.index == issn]
    check = issn.split(' ')
    for el in check:
        if el in journals:
            out.at[issn, 'country'] = journals[el]['country']
            out.at[issn, 'subject'] = journals[el]['subject']   
    batch_num += 1
    if not os.path.isdir('tmp'):
        makedirs('tmp')
    out.to_csv(f'tmp{sep}batch_{batch_num}.csv', encoding='utf8', chunksize=10000)


        
    
    

