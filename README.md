# 2021-2022-la-chouffe-code
The repository for the team La Chouffe of the Open Science course a.a. 2021/2022

## Information about the Project

### Data Management Plan
- Venditti Giulia, Catizone Chiara, & Brembilla Davide. (2022). La Chouffe - Data Management Plan (0.0.3). Zenodo. https://doi.org/10.5281/zenodo.6570286

### Protocol introducing the methodology
- Davide Brembilla, Chiara Catizone, & Giulia Venditti. (2022). PROTOCOL – Availability of Open Access Metadata from Open Journals – A case study in DOAJ and Crossref V.4. Protocol. protocols.io. https://doi.org/10.17504/protocols.io.kxygxz7ywv8j/v4

### Software developed
- GiuliaVenditti, dbrembilla, ChiaraCati, & Silvio Peroni. (2022). open-sci/2021-2022-la-chouffe-code: v.0.0.1 (prerelease). Zenodo. https://doi.org/10.5281/zenodo.6857310


### Data Gathered
- Davide Brembilla, Chiara Catizone, & Giulia Venditti.  (2022). La Chouffe Dataset (0.0.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.6562909

### Article Presenting the Research
- Davide Brembilla, Chiara Catizone & Giulia Venditti. (2022). Availability of Article Metadata from Open Journals – A case study in DOAJ and Crossref. https://doi.org/10.5281/zenodo.6570290


### Slides supporting the presentation
- Chiara Catizone, Davide Brembilla, & Giulia Venditti. (2022, May 25). Presentation La Chouffe team. Zenodo. https://doi.org/10.5281/zenodo.6579263

## Software requirements

Tested on Python > 3.9.

requests==2.27.1
requests-cache == 0.9.4
tqdm==4.62.3
backoff==2.0.1
pandas == 1.4.2

You can install these  with <code>pip install -r requirements.txt</code>

## Launching the software

To use this software you can use from the command line you need first to download both the journals' and the articles' dump from the [DOAJ](https://doaj.org/docs/public-data-dump/). 

Specifics of the computer used for the Estimated Time Allocated (ETA) values:
- Laptop Lenovo Ideapad 5
- Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz 8 core
- 8 GB RAM
- Windows 10 64 bit

These are the commands used in order to create the final dump:

<code>py -m batches_cleaner "path/to/articles/dump"</code>
ETA: 30s

<code>py -m main "cleaned"</code>
ETA: about 1h per batch (In our case: ca. 78h)

<code>py -m  stats "temp/completed"</code>
ETA: 5m

<code>py -m journal_cleaner "path/to/journal/dump" </code>
ETA: 1m

<code>py -m populator "stats"</code>
ETA: 1,30h

In the end, the pickle file was created through the Python interpreter:

<code>py #open the python shell</code>  <br>
<code>import pandas as pd
from stats import get_all_in_dir
dir = get_all_in_dir('results','csv')
df = pd.concat([pd.read_csv(file, encoding='utf8') for file in dir])
df.to_pickle('result.pkl')</code>
ETA: 10m
