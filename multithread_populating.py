from abc import ABC
import concurrent.futures
import requests
import os
from os import sep
import json
import time
import random
import requests_cache
import backoff
class populateJson(ABC):
    def __init__(self) -> None:
        requests_cache.install_cache('multithread_cache')
        self.api = "https://api.crossref.org/works/"
    
    @backoff.on_exception(backoff.expo, requests.exceptions.ReadTimeout, max_tries=20)
    def query_crossref(self, doi):
        
        query = self.api + doi
        time.sleep(random.randint(1,5))
        
        req = requests.get(query, timeout=60)
        return req, doi
    
    def _json_reader(self, file, skip = False):
        result = dict()
        data = None           
        with open(file, encoding='utf8', mode='r') as json_data:
            data = json.load(json_data)
            if skip:
                with open(skip, 'r') as read:
                    done = json.load(read)
                    for key in done:
                        data.pop(key)

        try:
            for i in range(0,len(data.keys()),1000):
                print(i)
                end = i + 999
                if end > len(data)-1:
                    end = len(data)
                to_analyse = list(data.keys())[i:end]
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    
                        for response, doi in executor.map(self.query_crossref, to_analyse):
                            index = " ".join(data[doi]['issns'])
                            if response.headers["content-type"].strip().startswith("application/json"):
                                if response.status_code != 200:
                                    tmp = {'crossref': 0, 'year': data[doi]['year'], 'reference': 0}
                                    if index not in result:
                                        
                                        result[index] = {doi: tmp}
                                    else:
                                        result[index][doi] = tmp
                                else:
                                    info = response.json()['message']
                                    
                                    tmp = {'crossref': 1, 'year': data[doi]['year'], 'reference': 0}

                                    if 'reference' in info:
                                        for element in info['reference']:
                                            tmp['reference'] = {element['key']:{}}
                                            if 'DOI' in element:
                                                tmp['reference'] = {element['key']:{'doi':element['DOI']}}
                                            else:
                                                tmp['reference'] = {element['key']:{'doi':'not-specified'}}
                                            if 'doi-asserted-by' in element:
                                                tmp['reference'][element['key']].update({'doi-asserted-by': element['doi-asserted-by']})
                                            else:
                                                tmp['reference'][element['key']].update({'doi-asserted-by': 'not-specified'})

                                    
                                    if index not in result:
                                        
                                        result[index] = {doi: tmp}
                                    else:
                                        result[index][doi] = tmp
                            else:
                                print('error', response.status_code)
            return result
        except:
            print(f'Error in processing {file}: what has been processed for now is in temp{sep+file}.')
            json.dump(result)
    
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
                done = get_all_in_dir('temp')
                name= file.split(sep)[1]
                idx +=1
                print(f'Opening {name}, file {idx} out of {length}')
                skip = False
                if file in done:
                    skip = 'temp' + sep + file
                tmp = self._json_reader(file, skip = skip)
                
                for key in tmp.keys():
                    if key in result:
                        result[key].update(tmp[key])
                    else:
                        result[key] = tmp[key]
                print(f"{name} took {time.time()-start_sub}s")
                

                start_sub = time.time()
            print(f"Response phase ended after {time.time()-start}s")
            if not os.path.isdir('output'):
                os.makedirs('output')
            with open('output'+sep+f'batch.json', 'w', encoding='utf8') as out:
                json.dump(result, out) 

def get_all_in_dir(dir, format = 'json'):
    try:
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)
            if os.path.isfile(f) and f[-4:] == format:
                yield f
    except:
        os.makedirs(dir)


            
        
        
            
        
            




        

