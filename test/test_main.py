import main


def test_solve():
    #1
    lst = main.solve(1, 0, -1)
    assert len(lst) == 0
    #2
    lst = sorted(main.solve(1, 0, -1))
    assert (lst[0] == -1) and (lst[1] == 1)
    #3
    lst = (main.solve(1, 2, 1))
    assert (lst[0] == -1) and (lst[1] == -1)
    #4
    try:
        lst = main.solve(0, 1, 1)
    except Exception:
        None
    else:
        assert False
    #5
    try:
        lst = main.solve(1, main.math.nan, 1)
    except Exception:
        None
    else:
        assert False
    #6
    try:
        lst = main.solve(1, 1, main.math.inf)
    except Exception:
        None
    else:
        assert False