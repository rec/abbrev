from typing import Any, Dict
import functools
import xmod

__version__ = '1.0.1'
__all__ = 'abbrev', 'NONE'

NONE = object()


@xmod
def abbrev(
    abbrevs: Dict[str, Any],
    key: Any = NONE,
    default: Any = NONE,
    multi: bool = False,
    unique: bool = True,
) -> Any:
    """
    Expand abbreviations in a dictionary.

    Handy when the user has a choice of commands with long names.

    Examples:

    ```
    import abbrev
    d = {'one': 1, 'two': 2, 'three': 3}

    assert abbrev(d, 'one') == 1
    assert abbrev(d, 'o') == 1
    assert abbrev(d, 'tw') == 2

    abbrev(d, 'four')  # Raises a KeyError: no such key
    abbrev(d, 't')  # Raises a KeyError: ambiguous key ('two' or 'three'?)

    # You can "curry" with a specific dictionary to get a callable
    # abbreviation example - like this:
    my_abbrevs = abbrev(d)

    assert my_abbrevs('one') == 1
    assert my_abbrevs('tw') == 2

    # In multi mode, you get all the results that match:
    multi = abbrev(d, multi=True)

    assert multi('t') == abbrev(d, 't', multi=True) == ('two', 'three')
    assert multi('o') == abbrev(d, 'o', multi=True) == ('one', )

    multi('four')  # Still raises a key error

    # Or if you turn off unique, you get the first result only:
    assert abbrev(d, 't', unique=False) == ('two',)
    ```

    Args:

      abbrevs:  A dictionary with string keys or a sequence of strings

      key: An abbreviated key to look up in `abbrevs`,
        If `key` is omitted, `abbrev` returns a callable that looks up
        abbreviations in `abbrevs`

      default: if `key` is not found in the dictionary, `default` is returned,
        if it's set.  Otherwise, missing keys throw a KeyError

      multi: If True, a tuple of matching keys is returned on a match
        If False, the default, only a single matching value is returned

      unique: If True, the default, `abbrev` raises a KeyError if more than one
        key matches.  If False, `abbrev` returns the first match.
        `unique` is ignored if `multi` is set
    """
    if key is NONE:
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