import argparse
from pathlib import Path


def main(test_dir: Path):
    for _, _, files in test_dir.walk():
        for file in files:
            print(file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_dir", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.test_dir)
