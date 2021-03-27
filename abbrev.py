"""
🐜 abbrev: look up abbreviations in a dictionary 🐜

Handy when the user has a choice of commands with long names.


EXAMPLE
=========

.. code-block:: python

    import abbrev
    d = {'one': 1, 'two': 2, 'three': 3}

    assert abbrev(d, 'one') == 1
    assert abbrev(d, 'o') == 1
    assert abbrev(d, 'tw') == 2

    abbrev(d, 'four')  # Raises a KeyError: no such key
    abbrev(d, 't')  # Raises a KeyError: ambiguous

    # You can "curry" a specific dictionary, and save it to call:
    curry = abbrev(d)

    assert curry('one') == 1
    assert curry('tw') == 2

    # In multi mode, you get all the results:
    multi = abbrev(d, multi=True)
    assert multi('t') == abbrev(d, 't', multi=True) == ('two', 'three')
    assert multi('o') == abbrev(d, 'o', multi=True) == ('one', )
    multi('four')  # Still raises a key error

    # Turn off unique, and you get the first result:
    assert abbrev(d, 't', unique=False) == ('two',)
"""

import functools
import xmod

__version__ = '0.9.2'
__all__ = 'abbrev', 'NONE'

NONE = object()


@xmod
def abbrev(abbrevs, key=NONE, default=NONE, multi=False, unique=True):
    """
    Look up abbreviations in a dictionary.  Handy when the user
    has a choice of commands with long names.

    ARGUMENTS
      abbrevs:
        A dictionary with string keys

      key:
        An abbreviated key to look up in `abbrevs`,

        If `key` is omitted, `abbrev` returns a callable that looks up
        abbreviations in `abbrevs`

      default:
        if `key` is not found in the dictionary, `default` is returned, if it's
        set.  Otherwise, missing keys throw a KeyError

      multi:
        If True, a tuple of matching keys is returned on a match
        If False, the default, only a single matching value is returned

      unique:
        If True, the default, `abbrev` raises a KeyError if more than one key
        matches.  If False, `abbrev` returns the first match.

        `unique` is ignored if `multi` is set
    """
    if key is NONE:
        return functools.partial(
            abbrev, abbrevs, default=default, multi=multi, unique=unique
        )

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


_DOKS = {NONE: 'NONE'}
