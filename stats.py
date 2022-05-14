import os
import argparse
import os
from os import sep
import json
from csv import DictWriter
import statistics
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
    aggr = []
    batch_num = 0
    ref_num_glob = 0
    ref_median = []

    for file in get_all_in_dir(path):
        print(file)
        with open(file, 'r', encoding='utf8') as read:
            to_analyse = json.load(read)
            
            for issn in to_analyse:
                info = to_analyse[issn]
                
                
                for doi in info:
                    to_add = {'doi': doi,'issn' : issn, 'doi-num': 1, 'on_crossref':0, 'reference':0,'asserted-by-cr':0,'asserted-by-pub':0,'ref-undefined':0, 'ref-num':0, 'year':''}
                    dois_total += 1
                    if to_add['year']:
                        to_add['year'] = info[doi]['year']
                    if info[doi]['crossref'] == 1:
                        to_add['on_crossref'] = 1
                        dois_crossref += 1
                    if info[doi]['reference'] != 0:
                        to_add['ref-num'] = len(info[doi]['reference'])
                        ref_num_glob += len(info[doi]['reference'])
                        ref_median.append(len(info[doi]['reference']))
                        ref_number += 1
                        to_add['reference']+=1
                        
                        try:
                            for el in info[doi]['reference'].values():
                                if el['doi'] == 'not-specified':
                                    to_add['ref-undefined'] += 1
                                    ref_nd += 1
                                elif el['doi-asserted-by'] == 'crossref':
                                    to_add['asserted-by-cr'] += 1
                                    ref_cr += 1
                                elif el['doi-asserted-by'] == 'publisher':
                                    ref_pub +=1
                                    to_add['asserted-by-pub'] += 1
                        except:
                            print(file, doi)
                       
                        aggr.append(to_add)
                if len(aggr) > 100000:
                    with open('.' +sep+ 'results' +sep+'aggregate_stats_' + str(batch_num)+'.csv','w+', encoding='utf8') as aggregates:
                        fieldnames = ['doi','issn', 'doi-num',  'on_crossref','reference','asserted-by-cr','asserted-by-pub','ref-undefined', 'ref-num','year']
                        writer = DictWriter(aggregates, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(aggr)
                    batch_num += 1
                    aggr= []
    text = f'''
    Number of dois: {dois_total}\n
    Number of dois on crossref: {dois_crossref} Percentage: {dois_crossref / dois_total}\n
    Number of dois on crossref with references: {ref_number} Percentage : {ref_number / dois_crossref}\n
    Number of total references: { ref_num_glob } Average number of references per article: {ref_num_glob/dois_total} Median: {statistics.median(ref_median)}\n
    Number of reference dois asserted by crossref: {ref_cr} Percentage: {ref_cr / ref_num_glob }\n
    Number of reference dois asserted by publisher: {ref_pub} Percentage: {ref_pub / ref_num_glob }\n
    Number of references with no doi: {ref_nd} Percentage: {ref_nd / ref_num_glob}
    '''
    with open('.' +sep+ 'results' +sep+'aggregate_stats_' + str(batch_num)+'.csv','w+', encoding='utf8') as aggregates:
        fieldnames = ['issn', 'doi-num',  'on_crossref','reference','asserted-by-cr','asserted-by-pub','ref-undefined', 'ref-num','year','doi']
        writer = DictWriter(aggregates, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aggr)
    print(text)
    with open('.' +sep+ 'results' +sep+'aggregate_stats.txt','w+', encoding='utf8') as aggregates:
        aggregates.write(text)
    

                    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files to populate with Crossref information about presence.')
    parser.add_argument('path', metavar='path',type=str, 
                    help='Path to the file or to the directory')
    
    args = parser.parse_args()
    if not os.path.isdir(f'.{sep}results'):
        os.makedirs(f'.{sep}results')
    compute(args.path)