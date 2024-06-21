import argparse
import importlib.util as iu
import ast
import inspect
import sys
import types
from pathlib import Path


class AssertRewriter(ast.NodeTransformer):

    def visit_Assert(self, node):
        return node


def rewrite_asserts(source_code: str):
    tree = ast.parse(source_code)
    AssertRewriter().visit(tree)
    return ast.unparse(tree)


def import_module(source_path: Path):

    name = source_path.stem
    if name in sys.modules:
        return sys.modules[name]

    with open(source_path) as f:
        source_code = f.read()

    source_code = rewrite_asserts(source_code)

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
