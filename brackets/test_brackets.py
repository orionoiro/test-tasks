import subprocess
from brackets import check_with_oddness


def test_empty():
    assert check_with_oddness('') == True


def test_simple():
    assert check_with_oddness('([])') == True


def test_simple_odd():
    assert check_with_oddness('{[(]}') == False


def test_nested():
    assert check_with_oddness('[{(([[[{}]]]))}]') == True


def test_nested_wrong():
    assert check_with_oddness('[[[{((([{(}{)})}])))}]]]') == False


def test_multi_expr():
    assert check_with_oddness('([{}])({})') == True


def test_multi_expr_wrong():
    assert check_with_oddness('[{({)(})}]({[]]]})') == False


def test_odd():
    assert check_with_oddness('(({{[[{]]}}))') == False


if __name__ == '__main__':
    subprocess.run('pytest')
