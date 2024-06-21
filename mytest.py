import argparse
import importlib.util as iu
import ast
import inspect
import sys
import types
from pathlib import Path


class AssertRewriter(ast.NodeTransformer):

    def visit_Assert(self, node):
        if isinstance(node.test, ast.Compare):
            left = node.test.left
            right = node.test.comparators[0]
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="mytest_asserts", ctx=ast.Load()),
                    attr="assert_eq",
                    ctx=ast.Load(),
                ),
                args=[
                    left,
                    right,
                    ast.unparse(left),
                    ast.unparse(right)
                ],
                kwargs={},
            )


def import_module(source_path: Path):

    name = source_path.stem
    if name in sys.modules:
        return sys.modules[name]

    with open(source_path) as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    source_code = ast.unparse(tree)

    mod = types.ModuleType(name)
    mod.__file__ = source_path
    code = compile(source_code, source_path, "exec")
    sys.modules[name] = mod
    exec(code, mod.__dict__)
    return sys.modules[name]


def discover_python_files(directory: Path):
    for root, sub_dir, files in directory.walk():
        for file_name in files:
            if file_name.endswith(".py"):
                yield root / file_name


def main(test_dir: Path):
    for file in discover_python_files(test_dir):
        m = import_module(file)
        m.matt()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_dir", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.test_dir)
