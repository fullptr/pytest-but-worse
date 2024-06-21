def assert_eq(left, right, left_str, right_str):
    if left != right:
        print(f"Assertion failed: {left_str} == {right_str}")
        print(f"    Value of {left_str}: {left}")
        print(f"    Value of {right_str}: {right}")