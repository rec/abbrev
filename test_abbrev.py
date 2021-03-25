from unittest import TestCase
import abbrev


class TestAbbrev(TestCase):
    def test_function(self):
        d = {'one': 1, 'two': 2, 'three': 3}
        ab = abbrev(d)

        assert abbrev(d, 'o') == ab('on') == ab('one') == 1
        assert abbrev(d, 'two') == ab('tw') == 2
        assert abbrev(d, 'th') == ab('three') == 3

    def test_error(self):
        ab = abbrev({'one': 1, 'two': 2, 'three': 3})

        with self.assertRaises(KeyError) as m:
            ab('four')
        assert m.exception.args == ('four',)

        with self.assertRaises(KeyError) as m:
            ab('t')
        assert m.exception.args == ('t', "was ambiguous: ['two', 'three']")
