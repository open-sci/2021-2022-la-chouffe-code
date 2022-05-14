import os
from os import sep
import json
import argparse
def get_all_in_dir(dir, format = 'json'):
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)

        if os.path.isfile(f) and f[-len(format):] == format:
            yield f


def clean(files):
    for filename in files:
        if filename != '.DS_Store':
            file = open(filename)
            data =  json.load(file)
            file.close()
            result = dict()
            x = 0
            for article in data:
                x+=1
                check = False #checker if the article has doi, if not it will be skipped as we cannot query Crossref without it 
                
                for item in article['bibjson']['identifier']:
                    if 'doi' in item.values():
                        if 'id' in item:
                            doi = item['id']
                            check = True
                            Mydict = dict()

                if check: #doi is present
                    
                    if 'year' in article['bibjson']:
                        year = article['bibjson']['year']
                        Mydict['year'] = year
                
                    else:
                        Mydict['year'] = 0
                    
                    if 'issns' in article['bibjson']['journal']:
                        issns = article['bibjson']['journal']['issns']
                        Mydict['issns'] = issns
                        
                    else:
                        Mydict['issns'] = 0

                    
                    result[doi] = Mydict
            
                else: #doi is not present
                    pass
            f = open("cleaned"+sep+filename.split(sep)[1], 'w+')
            json.dump(result, f, indent=4)
            f.close()
        # output.write(result)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files to populate with Crossref information about presence.')
    parser.add_argument('path', metavar='path',type=str, 
                    help='Path to the file or to the directory')
    
    args = parser.parse_args()
    if not os.path.isdir(f'.{sep}cleaned'):
        os.makedirs(f'.{sep}cleaned')
    clean(args.path)
    