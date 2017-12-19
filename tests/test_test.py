import pytest


class TestTest(object):
    """ Example test object.
    """

    def test_test(self):
        """ Base example test case.
        """

        assert True
        assert not False
        assert isinstance('', str)
        assert isinstance(0, int)
        assert isinstance(0.0, float)
        assert isinstance([], list)
        assert isinstance(tuple(), tuple)
        assert isinstance(set(), set)
        assert isinstance({}, dict)

        with pytest.raises(ValueError):
            raise ValueError()
