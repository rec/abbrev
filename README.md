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


### [API Documentation](https://rec.github.io/abbrev#abbrev--api-documentation)
