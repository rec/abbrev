"""
🐜 abbrev: look up abbreviations in a dictionary
"""

import functools
import xmod

_NONE = object()


@xmod
def abbrev(dc, key=_NONE, multi=False, unique=True):
    """Expand abbreviated prefixes in a dict if possible"""
    if key is _NONE:
        return functools.partial(abbrev, dc, multi=multi, unique=unique)

    try:
        r = dc[key]
    except KeyError:
        pass
    else:
        return (r,) if multi else r

    kv = [(k, v) for k, v in dc.items() if k.startswith(key)]
    if kv:
        keys, values = zip(*kv)
    else:
        keys = values = []

    if multi:
        return values

    if not values:
        raise KeyError(key)

    if unique and len(values) > 1:
        raise KeyError(key, f'was ambiguous: {keys}')

    return values[0]
