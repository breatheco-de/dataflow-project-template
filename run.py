import random
import time
import sys
import os
import pandas
from colorama import Fore, Back, Style
from utils.core import load_pipelines_from_project, get_params, load_pipelines_from_project, get_transformation


pipeline, sources = get_params()
if pipeline is None:
    all = load_pipelines_from_project()
    raise Exception(f'Please specify pipline to load from the following options: ' +
                    ",".join([p['slug'] for p in all]))
else:
    pipeline = load_pipelines_from_project(pipeline)[0]


if sources is None or len(sources) == 0:
    raise Exception(
        f'Missing CSV Files to for source from when running pipeline {pipeline}.\n Hint: please specify the name of the CSV files name separated by space')
else:
    for i in range(len(sources)):
        if ".csv" not in sources[i]:
            sources[i] = sources[i] + ".csv"


dfs = []
for source in sources:
    dfs.append(pandas.read_csv("sources/"+source))

df_out = None
count = 0
for t in pipeline['transformations']:
    count += 1
    print(Fore.WHITE+f"[] Applying {count} transformation {t}...")
    run, _in, _out = get_transformation(pipeline['slug'], t)
    if count == 1:
        df_out = run(*dfs)
    else:
        df_out = run(df_out, *dfs)

file_name = source.split('.')[0]
df_out.to_csv(
    f"output/{pipeline['slug']}{str(round(time.time()))}.csv")
