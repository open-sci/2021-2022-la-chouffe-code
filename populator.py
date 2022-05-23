'''
# MIT License (MIT)
Copyright © 2022 Silvio Peroni, Alessandro Bertozzi, Davide Brembilla, Chiara Catizone, Constance Dami, Umut Kuçuk, Chiara Manca, Giulia Venditti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from stats import get_all_in_dir
import json
import pandas as pd
from os import makedirs, sep
import os
from tqdm import tqdm
import argparse
def pop(path):
    journals = dict()
    with open('cleanJournalsDump.json', 'r') as input:
        journals = json.load(input)
    dir = get_all_in_dir('results','csv')
    df = pd.concat([pd.read_csv(file, encoding='utf8') for file in dir])
    my_issn = set(df.issn)

    batch_num = 0
    df = df.set_index('issn')
    for issn in tqdm(my_issn):
        out = df[df.index == issn]
        check = issn.split(' ')
        for el in check:
            if el in journals:
                out.at[issn, 'country'] = journals[el]['country']
                out.at[issn, 'subject'] = journals[el]['subject']['code'][0]   
        batch_num += 1
        if not os.path.isdir('tmp'):
            makedirs('tmp')
        out.to_csv(f'tmp{sep}batch_{batch_num}.csv', encoding='utf8', chunksize=10000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files to populate with Crossref information about presence.')
    parser.add_argument('path', metavar='path',type=str, 
                    help='Path to the file or to the directory')
    
    args = parser.parse_args()
    if not os.path.isdir(f'.{sep}cleaned'):
        os.makedirs(f'.{sep}cleaned')
    pop(args.path)
        
    
    

