
import argparse
import os
from os import sep
import time
from multithread_populating import populateJson


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files to populate with Crossref information about presence.')
    parser.add_argument('path', metavar='path',type=str, 
                    help='Path to the file or to the directory')
   
    args = parser.parse_args()

    start = time.time()
    pop = populateJson()
    pop.populate(args.path)

