from dataclasses import asdict

import pandas as pd

from .parser import parse_alignment_file


def read_sbalign_df(file_name):
    alignment = parse_alignment_file(file_name)
    return items_df(alignment)


def items_df(alignment, mode="string", sep=";"):
    items = [asdict(item) for item in alignment.items]
    if mode == "string":
        items = [_stringify_dict(item, sep) for item in items]
    return pd.DataFrame(items)


def _stringify_dict(item, sep):
    return {
        **item,
        **{key: _stringify(item[key], sep) for key in ["hyp", "ref", "alignment"]},
    }


def _stringify(value, sep):
    return sep.join(value)
