import random
import time
import sys
import os
import pandas
from colorama import Fore, Back, Style
from utils.core import load_pipelines_from_project, get_params, load_pipelines_from_project, get_transformation


pipeline, source = get_params()
if pipeline is None:
    all = load_pipelines_from_project()
    raise Exception(f'Please specify pipline to load from the following options: ' +
                    ",".join([p['slug'] for p in all]))
else:
    pipeline = load_pipelines_from_project(pipeline)[0]


if source is None:
    raise Exception(
        f'Missing CSV File to for source from when running pipeline {pipeline}.\n Hint: please specify the name of the CSV file name')
else:
    if ".csv" not in source:
        source = source + ".csv"

df = pandas.read_csv("sources/"+source)
for t in pipeline['transformations']:
    print(Fore.WHITE+f"[] Applying {t}...")
    run, _in, _out = get_transformation(pipeline['slug'], t)
    df = run(df)

file_name = source.split('.')[0]
df.to_csv(
    f"output/{file_name}-{pipeline['slug']}{str(round(time.time()))}.csv")
