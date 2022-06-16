import main


def test_solve():
    #1 Unsolvable
    lst = main.solve(1, 0, 1)
    assert len(lst) == 0
    #2 2 roots of multiplicity 1
    lst = sorted(main.solve(1, 0, -1))
    assert (lst[0] == -1) and (lst[1] == 1)
    #3 1 root of multiplicity 2
    lst = (main.solve(1, 2, 1))
    assert (lst[0] == -1) and (lst[1] == -1)
    #4 Zero 'a' coefficient
    try:
        lst = main.solve(0, 1, 1)
    except Exception:
        None
    else:
        assert False
    #5 Discriminant less than epsilon
    lst = (main.solve(1e-8, 1e-8, -1e-9))
    assert (abs(lst[0] - lst[1]) < main.sys.float_info.epsilon)
    #6 Non-numeric coefficients
    try:
        lst = main.solve(1, main.math.nan, 1)
    except Exception:
        None
    else:
        assert False
    #6 Non-numeric coefiicients
    for incorret in main.math.nan, main.math.inf, -main.math.inf:
        for i in range(3):
            coef = [1, 1, 1]
            coef[i] = incorret
            try:
                lst = main.solve(coef[0], coef[1], coef[2])
            except Exception:
                None
            else:
                assert False