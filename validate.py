import random
import sys
import pandas as pd
import os
import traceback


from colorama import Fore, Back, Style
from utils.core import (
    load_pipelines_from_project, get_params, get_transformation, scan_for_pipelines,
    scan_pipeline_transformations
)
from deepdiff import DeepDiff


def to_df(df):
    if isinstance(df, list):
        try:
            return pd.DataFrame(df)
        except Exception as e:
            print(df)
            raise e
    elif isinstance(df, pd.DataFrame):
        return df
    else:
        raise Exception(
            f'Invalid type {type(df)} for variable "expected_input" or "ouput" (expected list or DataFrame)')


def lo_list(df):
    if isinstance(df, list):
        return df
    elif isinstance(df, pd.DataFrame):
        return df.to_dict('records')
    else:
        raise Exception(
            f'Invalid type {type(df)} for variable "expected_input" or "ouput" (expected list or DataFrame)')


def validate_trans(q, t, _errors):
    try:
        run, _in, _out = get_transformation(q, t)
        output = run(to_df(_in)).to_dict('records')

        in_out_same = DeepDiff(lo_list(_in), lo_list(_out))
        diff = DeepDiff(lo_list(output), lo_list(_out))
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
        if not isinstance(errors[e], str):
            traceback.print_exception(
                type(errors[e]), errors[e], errors[e].__traceback__)

    print(Style.RESET_ALL + '\n')
    exit(1)
else:
    print(Back.GREEN +
          f'Report: All {len(pipelines)} transformations return the expected outputs 🙂', end='')
    print(Style.RESET_ALL)
    exit(0)
