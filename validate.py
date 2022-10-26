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


def to_df(_lists):
    _dfs = []
    for l in _lists:
        if isinstance(l, list):
            try:
                _dfs.append(pd.DataFrame(l))
            except Exception as e:
                print(l)
                raise e
        elif isinstance(l, pd.DataFrame):
            _dfs.append(l)
        else:
            raise Exception(
                f'Invalid type {type(l)} for variable "expected_inputs" or "ouput" (expected list or DataFrame)')
    return _dfs


def lo_list(_dfs):
    if len(_dfs) > 0:
        if isinstance(_dfs[0], dict):
            _dfs = [_dfs]

    _lists = []
    for df in _dfs:
        if isinstance(df, list):
            _lists.append(df)
        elif isinstance(df, pd.DataFrame):
            _lists.append(df.to_dict('records'))
        else:
            raise Exception(
                f'Invalid type {type(df)} for variable "expected_inputs" or "ouput" (expected list or DataFrame)')
    return _lists


def validate_trans(q, t, _errors):
    try:
        run, _in, _out = get_transformation(q, t)
        if not isinstance(_in, list):
            raise Exception("Transformation expected_inputs must be a list")

        if len(_in) == 0:
            raise Exception("Transformation expected_inputs are empty")

        if len(_in) == 1:
            if not isinstance(_in[0], list):
                _in = [_in]
        else:
            for i in range(len(_in)):
                if not isinstance(_in[i], list):
                    raise Exception(
                        "You have more than one expected_inputs, each of them must be a list but the {i} position it's not")

        output = run(*to_df(_in))
        if output is None:
            raise Exception("Transformation needs to return a dataset")
        output = output.to_dict('records')

        in_out_same = DeepDiff(lo_list(_in)[0], lo_list(_out)[0])
        diff = DeepDiff(lo_list(output)[0], lo_list(_out)[0])
    except Exception as e:
        _errors[q + '.' + t] = e

    if (q + '.' + t) in _errors:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
    elif len(diff.keys()) != 0:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
        if "values_changed" in diff:
            diff = diff["values_changed"]
        _errors[q + '.' + t] = "\n".join(f"{k}: {v}" for k, v in diff.items())
    elif len(in_out_same.keys()) == 0:
        print(Fore.RED + q + '.' + t + ' ❌', end='')
        _errors[q + '.' + t] = 'The expected_inputs and expected_output variables have the same values'
    else:
        print(Fore.GREEN + q + '.' + t + ' ✅', end='')

    print(Style.RESET_ALL)
    print('')

    return _errors


pipeline, sources = get_params()
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
