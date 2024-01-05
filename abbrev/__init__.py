"""
# 🐜 `abbrev`: Expand abbreviations 🐜

Expand a `Sequence` or `Mapping` of string abbreviations.

Handy when the user has a choice of commands with long names.

## Example 1: Use a list of choices

    import abbrev

    a = ['one', 'two', 'three']

    assert abbrev(a, 'one') == 'one'
    assert abbrev(a, 'o') == 'one'
    assert abbrev(a, 'tw') == 'two'

    abbrev(a, 'four')  # Raises a KeyError: no such key
    abbrev(a, 't')  # Raises a KeyError: ambiguous key ('two' or 'three'?)


## Example 2: Use a dictionary of choices

    import abbrev

    d = {'one': 100, 'two': 200, 'three': 300}

    assert abbrev(d, 'one') == 100
    assert abbrev(d, 'o') == 100
    assert abbrev(d, 'tw') == 200

## Example 3: Make an abbreviator to re-use

    import abbrev

    d = {'one': 100, 'two': 200, 'three': 300}

    abbreviator = abbrev(d)

    assert abbreviator('one') == my_abbrevs('o') == 100
    assert abbreviator('tw') == 200

## Example 4: Get all matches, when `multi=True`

    import abbrev

    a = ['one', 'two, 'three'}

    multi = abbrev(a, multi=True)  # Make an abbreviator

    assert multi('t') == abbrev(d, 't', multi=True) == ('two', three')
    assert multi('o') == abbrev(d, 'o', multi=True) == ('one', )

    multi('four')  # Still raises a key error

## Example 5: Get only the first result, when `unique=False`

    import abbrev

    d = {'one': 100, 'two': 200, 'three': 300}

    assert abbrev(d, 't', unique=False) == (200, 300)
"""

from typing import Any, Mapping, Optional, Sequence, Union
import functools
import xmod

__all__ = 'abbrev', 'NONE'

NONE = object()


@xmod
def abbrev(
    abbrevs: Union[ Mapping[str, Any], Sequence[str] ],
    key: Optional[str] = None,
    default: Any = NONE,
    multi: bool = False,
    unique: bool = True,
) -> Any:
    """
    Returns:
       An expanded abbreviation if `key` is given, else an abbreviator

    Args:
      abbrevs:  A dictionary with string keys or a sequence of strings

      key: An abbreviated key to look up in `abbrevs`,

        If `key` is omitted, `abbrev` returns a callable that looks up
        abbreviations in `abbrevs`

      default: if `key` is not found in the dictionary, `default` is returned,
        if it is set.

        If `default` is not set, missing keys throw a `KeyError`

      multi: If True, a tuple of matching keys is returned on a match.

        If False, the default, only a single matching value is returned

      unique: If True, the default, `abbrev` raises a KeyError if more than one
        key matches.

        If False, `abbrev` returns the first match.

        `unique` is ignored if `multi` is set
    """
    if key is None:
        return functools.partial(
            abbrev, abbrevs, default=default, multi=multi, unique=unique
        )

    if not isinstance(abbrevs, dict):
        abbrevs = {i: i for i in abbrevs}

    r = abbrevs.get(key, NONE)
    if r is not NONE:
        return (r,) if multi else r

    kv = [(k, v) for k, v in abbrevs.items() if k.startswith(key)]
    if kv:
        keys, values = zip(*kv)

    elif multi:
        return []

    elif default is not NONE:
        return default

    else:
        raise KeyError(key)

    if multi:
        return values

    if unique and len(values) > 1:
        raise KeyError(key, f'was ambiguous: {keys}')

    return values[0]
