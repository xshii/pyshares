import argparse

import requests

from src import VER

session = requests.Session()

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="test shares")
    parse.add_argument("--version", "-v", help="获取版本", action="store_true")
    parse.add_argument("--code", type=str, help="获取建议")
    args = parse.parse_args()
    if args.version:
        print(f"当前版本：{VER}")
    if code := args.code:
        pass
