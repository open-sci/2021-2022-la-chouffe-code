# MIT License (MIT)
#Copyright © 2022 Silvio Peroni, Alessandro Bertozzi, Davide Brembilla, Chiara Catizone, Constance Dami, Umut Kuçuk, Chiara Manca, Giulia Venditti

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import concurrent.futures
from re import sub
from urllib.parse import unquote
from tqdm.contrib.concurrent import thread_map
import requests
import os
from os import sep
import json
import time
import random
import requests_cache
import backoff
from tqdm import tqdm


def normalise(id_string):
        try:
            doi_string = sub("\0+", "", sub("\s+", "", unquote(id_string[id_string.index("10."):])))
            return doi_string.lower().strip()
        except:  # Any error in processing the DOI will return None
            return "False"


def merge(dict1,dict2):
    for el in dict2:
        if el in dict1:
            dict1[el].update(dict2[el])
    return dict1

class populateJson:
    '''
    This class is used to query Crossref and populate the Json Files.
    '''
    def __init__(self) -> None:
        requests_cache.install_cache('multithread_cache')
        self.api = "https://api.crossref.org/works/"
    
    @backoff.on_exception(backoff.expo, requests.exceptions.ReadTimeout, max_tries=20)
    def query_crossref(self, doi):
        '''
        This method queries crossref by adding to the API url the DOI. It returns the result the request and the doi added. In order to avoid being blocked by the API.
        '''
        query = self.api + normalise(doi)
        #time.sleep(random.randint(1,3))
        try: 
            req = requests.get(query, timeout=60)
        except:
            return 1234, doi
        return req, doi
    
    def _json_reader(self, file, skip = False):
        '''
        This method manages the queries on the file level. If there is a temporary file (in the temp folder), skips the rows done; once the file is completed, it is loaded in the temp/completed folder. This method employs multithreading to speed up the requests at the API. It checks whether a DOI is on Crossref, if there are references and who is responsible for asserting the DOI.
        '''
        result = dict()
        data = None
        if isinstance(file, str):  
            with open(file, encoding='utf8', mode='r') as json_data:
                data = json.load(json_data)
                if skip:
                    with open(skip, 'r') as read:
                        done = json.load(read)
                        result = done
                        for elements in done.values():
                            for doi in elements:
                                data.pop(doi)
        else:
            data = file
        to_do = dict()
        try:
            for i in tqdm(range(0,len(data),1000)):
                end = i + 999
                if end > len(data)-1:
                    end = len(data)
                to_analyse = list(data.keys())[i:end]
                with tqdm(total=len(to_analyse)) as pbar:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        for response, doi in executor.map(self.query_crossref, to_analyse):
                            if response == 1234:
                                to_do[doi] = data[doi]
                                time.sleep(5)
                                continue
                            pbar.update(1)
                            index = " ".join(data[doi]['issns'])
                            if response.headers["content-type"].strip().startswith("application/json"):
                                
                                if response.status_code == 404:
                                    tmp = {'crossref': 0, 'year': data[doi]['year'], 'reference': 0}
                                    if index not in result:
                                        
                                        result[index] = {doi: tmp}
                                    else:
                                        result[index][doi] = tmp
                                elif response.status_code == 200:
                                    info = response.json()['message']
                                    
                                    tmp = {'crossref': 1, 'year': data[doi]['year'], 'reference': 0, 'type': info['type']}

                                    if 'reference' in info:
                                        tmp['reference'] = dict()
                                        for element in info['reference']:
                                            tmp['reference'][element['key']] = dict()
                                            if 'DOI' in element:
                                                tmp['reference'][element['key']] = {'doi':element['DOI']}
                                            else:
                                                tmp['reference'][element['key']] = {'doi':'not-specified'}
                                            if 'doi-asserted-by' in element:
                                                tmp['reference'][element['key']].update({'doi-asserted-by': element['doi-asserted-by']})
                                            else:
                                                tmp['reference'][element['key']].update({'doi-asserted-by': 'not-specified'})

                                    
                                    if index not in result:
                                        
                                        result[index] = {doi: tmp}
                                    else:
                                        result[index][doi] = tmp
                                else:
                                    print(response.status_code)
                                    to_do[doi] = data[doi]

                            else:
                                print('error', response.status_code)
            if len(to_do) == 0:
                return result
            else:
                time.sleep(5)
                to_add = self._json_reader(to_do)
                return merge(result, to_add)

                
        except Exception as e:
            print(e)
            time.sleep(5)
            to_add = self._json_reader(to_do)
            return merge(result, to_add)
            

    
    def populate(self, path):
        '''
        This method manages the population of all the files in a directory. It loads temporary or completed files (temp and temp/completed respectively) if present. The output .json file can be found in the output directory.
        '''

        start = time.time()
        #result = dict()
        if os.path.isdir(path):
            queue = list(get_all_in_dir(path))
            length = len(queue)
            idx = 0
            if length < 1:
                raise NotImplementedError
            start_sub = time.time()
            for file in queue:
                part_done = get_all_in_dir('temp')
                done = get_all_in_dir(f'temp{sep}completed')
                name= file.split(sep)[1]
                idx +=1
                print(f'Opening {name}, file {idx} out of {length}')
                tmp = None
                skip = False
                if f'temp{sep}completed' + sep + name in done:
                    with open(f'temp{sep}completed{sep+name}', 'r') as infile:
                        tmp = json.load(infile)
                elif f'temp{sep}' + name in part_done:
                    skip = 'temp' + sep + name
                    tmp = self._json_reader(file, skip = skip)
                else:
                    tmp = self._json_reader(file, skip = skip)
                with open(f"temp{sep}completed{sep +file.split(sep)[1]}", 'w+') as out:
                    json.dump(tmp, out, indent=4)
                #for key in tmp.keys():
                #    if key in result:
                #        result[key].update(tmp[key])
                #    else:
                #        result[key] = tmp[key]
                print(f"{name} took {time.time()-start_sub}s")
                

                start_sub = time.time()
            print(f"Response phase ended after {time.time()-start}s")
            if not os.path.isdir('output'):
                os.makedirs('output')
            #with open('output'+sep+f'batch.json', 'w', encoding='utf8') as out:
            #    json.dump(result, out, indent=4) 

def get_all_in_dir(dir, format = 'json'):
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)

        if os.path.isfile(f) and f[-len(format):] == format:
            yield f


            
        
        
            
        
            




        

