from abc import ABC
import concurrent.futures
import requests
import argparse
import os
from os import sep
from collections import deque
import json
import time
import random
import requests_cache
NUM_THREADS = 5

class populateJson(ABC):
    def __init__(self) -> None:
        requests_cache.install_cache('multithread_cache')
        self.api = "https://api.crossref.org/works/"
    
    def query_crossref(self, doi):
        
        query = self.api + doi
        time.sleep(random.randint(1,5))
        req = requests.get(query, timeout=60)
        return req, doi
    
    def _json_reader(self, file):
        result = dict()
        with open(file, encoding='utf8', mode='r') as json_data:
            data = json.load(json_data)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for response, doi in executor.map(self.query_crossref, data):
                    index = " ".join(data[doi]['issns'])
                    if response.headers["content-type"].strip().startswith("application/json"):
                        if response.status_code != 200:
                            tmp = {'crossref': 0, 'year': data[doi]['year'], 'references': 0}
                            if index not in result:
                                
                                result[index] = {doi: tmp}
                            else:
                                result[index][doi] = tmp
                        else:
                            info = response.json()['message']
                            
                            tmp = {'crossref': 1, 'year': data[doi]['year']}

                            if 'references' in info:
                                tmp['references'] = info['references']
                            else:
                                tmp['references'] = []
                            if index not in result:
                                
                                result[index] = {doi: tmp}
                            else:
                                result[index][doi] = tmp
                    else:
                        print('error', response.headers["content-type"])
        return result
    
    def populate(self, path):
        start = time.time()
        result = dict()
        if os.path.isdir(path):
            
            queue = list(get_all_in_dir(path))
            length = len(queue)
            idx = 0
            if length<1:
                raise NotImplementedError
            start_sub = time.time()
            for file in queue:
                name= file.split(sep)[1]
                idx +=1
                print(f'Opening {name}, file {idx} out of {length}')
                tmp = self._json_reader(file)
                for key in tmp:
                    if key in result:
                        result[key].update(tmp[key])
                    else:
                        result[key] = tmp[key]
                print(f"{name} took {time.time()-start_sub}s")
                start_sub = time.time()
            print(f"Response phase ended after {time.time()-start}s")
            if not os.path.isdir('output'):
                os.makedirs('output')
            with open('output'+sep+'batch', 'w', encoding='utf8') as out:
                json.dump(result, out) 

def get_all_in_dir(dir, format = 'json'):
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f) and f[-4:] == format:
            yield f


            
        
        
            
        
            




        

