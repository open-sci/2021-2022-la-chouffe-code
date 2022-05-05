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
        time.sleep(random.randint(1,3))
        
        req = requests.get(query, timeout=60)
        return req, doi
    
    def _json_reader(self, file, skip = False):
        result = dict()
        filename = file.split(sep)[1]
        data = None           
        with open(file, encoding='utf8', mode='r') as json_data:
            data = json.load(json_data)
            if skip:
                with open(skip, 'r') as read:
                    result = json.load(read)
                    for key in result:
                        data.pop(key)
        

        try:
            for i in range(0,len(data.keys()),1000):
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
            with open(f"temp{sep}completed{sep +filename}", 'w+') as out:
                json.dump(result, out, indent=4)
            return result
        except Exception as e:
            print(f'Error in processing {file}: what has been processed for now is in temp{sep+file}. \nError: {e}')
            with open(f"temp{sep +filename}", 'w+') as out:
                json.dump(result, out, indent=4)
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
                json.dump(result, out, indent=4) 

def get_all_in_dir(dir, format = 'json'):
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f) and f[-4:] == format:
            yield f
    


            
        
        
            
        
            




        

