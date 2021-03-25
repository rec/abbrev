from unittest import TestCase
import abbrev


class TestAbbrev(TestCase):
    def test_function(self):
        d = {'one': 1, 'two': 2, 'three': 3}
        abr = abbrev(d)

        assert abbrev(d, 'o') == abr('on') == abr('one') == 1
        assert abbrev(d, 'two') == abr('tw') == 2
        assert abbrev(d, 'th') == abr('three') == 3

    def test_error(self):
        abr = abbrev({'one': 1, 'two': 2, 'three': 3})

        with self.assertRaises(KeyError) as m:
            abr('four')
        assert m.exception.args == ('four',)

        with self.assertRaises(KeyError) as m:
            abr('t')
        assert m.exception.args == ('t', "was ambiguous: ('two', 'three')")

    def test_unique(self):
        abr = abbrev({'one': 1, 'two': 2, 'three': 3}, unique=False)

        assert abr('t') == 2
        assert abr('o') == 1
        with self.assertRaises(KeyError):
            abr('t', unique=True)

    def test_multi(self):
        d = {'one': 1, 'two': 2, 'three': 3}
        abr = abbrev(d, multi=True)

        assert abr('one') == (1,)
        assert abr('on') == (1,)
        assert abr('tw') == (2,)
        assert abr('three') == (3,)
        assert abr('t') == (2, 3)
        assert abr('') == (1, 2, 3)
