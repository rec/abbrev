import functools
import xmod

_NONE = object()


@xmod
def abbrev(dc, key=_NONE):
    """Expand abbreviated prefixes in a dict if possible"""

    if key is _NONE:
        return functools.partial(abbrev, dc)

    try:
        return dc[key]
    except KeyError:
        pass

    kv = [(k, v) for k, v in dc.items() if k.startswith(key)]
    if not kv:
        raise KeyError(key)

    if len(kv) > 1:
        keys = [k for k, v in kv]
        raise KeyError(key, f'was ambiguous: {keys}')

    return kv[0][1]
