'''# MIT License (MIT)
Copyright © 2022 Silvio Peroni, Alessandro Bertozzi, Davide Brembilla, Chiara Catizone, Constance Dami, Umut Kuçuk, Chiara Manca, Giulia Venditti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
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
        