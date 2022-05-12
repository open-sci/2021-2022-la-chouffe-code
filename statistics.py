import os
import argparse
import os
from os import sep
import json
from csv import DictWriter

def get_all_in_dir(dir, format = 'json'):
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f) and f[-4:] == format:
            yield f
def compute(path):
    dois_total = 0
    dois_crossref = 0
    ref_number = 0
    ref_cr = 0
    ref_nd = 0
    ref_pub = 0
    to_analyse = dict()
    aggr = []

    for file in get_all_in_dir(path):
        with open(file, 'r', encoding='utf8') as read:
            reader = json.load(read)
            for el in reader:
                if el in to_analyse:
                    to_analyse[el].extend(reader[el])
                else:
                    to_analyse[el] = reader[el]
    for issn in to_analyse:
        info = to_analyse[issn]
        
        
        for doi in info:
            to_add = {'issn' : issn, 'on_crossref':0, 'reference':0,'asserted-by-cr':0,'asserted-by-pub':0,'ref-undefined':0, 'ref-num':0}
            dois_total += 1
            if info[doi]['crossref']:
                to_add['on_crossref'] = 1
                dois_crossref += 1
            if info[doi]['reference']:
                to_add['ref-num'] = len(info[doi]['reference'])
                ref_number += 1
                
                for el in info[doi]['reference'].values():
                    if el['doi'] == 'not specified':
                        to_add['ref-undefined'] += 1
                        ref_nd += 1
                    elif el['doi-asserted-by'] == 'crossref':
                        to_add['asserted-by-cr'] += 1
                        ref_cr += 1
                    elif el['doi-asserted-by'] == 'publisher':
                        ref_pub +=1
                        to_add['asserted-by-pub'] += 1
            aggr.append(to_add)
    print(f'''
    Number of dois: {dois_total}
    Number of dois on crossref: {dois_crossref} Percentage: {dois_crossref / dois_total}
    Number of dois on crossref with references: {ref_number} Percentage : {ref_number / dois_crossref}
    Number of reference dois asserted by crossref: {ref_cr} Percentage: {ref_cr / ref_number }
    Number of reference dois asserted by publisher: {ref_pub} Percentage: {ref_pub / ref_number }
    Number of references with no doi: {ref_nd} Percentage: {ref_nd / ref_number}
    ''')
    with open('.' +sep+ 'results' +sep+'aggregate_stats.csv','w+', encoding='utf8') as aggregates:
        fieldnames = ['issn',  'on_crossref','reference','asserted-by-cr','asserted-by-pub','ref-undefined', 'ref-num']
        writer = DictWriter(aggregates, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aggr)
    

                    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files to populate with Crossref information about presence.')
    parser.add_argument('path', metavar='path',type=str, 
                    help='Path to the file or to the directory')
    
    args = parser.parse_args()
    if not os.path.isdir(f'.{sep}results'):
        os.makedirs(f'.{sep}results')
    compute(args.path)