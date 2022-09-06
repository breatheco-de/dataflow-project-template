import random
import sys
import pandas as pd
import os

from colorama import Fore, Back, Style
from utils.core import (
    load_pipelines_from_project, get_params, get_transformation, scan_for_pipelines, 
    scan_pipeline_transformations
)
from deepdiff import DeepDiff


def validate_trans(q, t, _errors):
    try:
        run, _in, _out = get_transformation(q, t)
        output = run(pd.DataFrame(_in, index=[0])).to_dict('records')

        in_out_same = DeepDiff(_in, _out)
        diff = DeepDiff(output, _out)
    except Exception as e:
        _errors[q + '.' + t] = e

    if (q + '.' + t) in _errors:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
    elif len(diff.keys()) != 0:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
        _errors[q + '.' + t] = str(diff)
    elif len(in_out_same.keys()) == 0:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
        _errors[q + '.' + t] = 'The expected_input and expected_output variables have the same values'
    else:
        print(Fore.GREEN + q + '.' + t + ' ✅', end='')
    print(Style.RESET_ALL)
    print('')
    return errors


pipeline, source = get_params()
errors = {}
pipelines = scan_for_pipelines()

for pipe in pipelines:
    print('\n\nStarting to validate every pipeline and transformation...\n')
    transformations = scan_pipeline_transformations(pipe)
    for t in transformations:
        errors = validate_trans(pipe, t, errors)

if len(errors) > 0:
    print('\n')
    print(Back.RED + f'Report: {len(errors)} errors found:', end='')
    print(Style.RESET_ALL)
    print('\n')
    count = 0
    for e in errors:
        count += 1
        print(Fore.RED + f'{count}) In {e}: ', end='')
        print(errors[e])

    print(Style.RESET_ALL + '\n')
    exit(1)
else:
    print(Back.GREEN + f'Report: All {len(pipelines)} transformations return the expected outputs 🙂', end='')
    print(Style.RESET_ALL)
    exit(0)
