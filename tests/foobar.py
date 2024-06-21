import mytest_asserts


def test_foo():
    assert 1 == 4 - 3


def test_other():
    x = mytest_asserts.assert_eq()


def not_a_test():
    print("not a test function")


def matt():
    print("foobar")