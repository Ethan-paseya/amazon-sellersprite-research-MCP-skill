#!/usr/bin/env python3
from sellersprite_skill_tools import main


if __name__ == "__main__":
    raise SystemExit(main(["publish-github-api", *(__import__("sys").argv[1:])]))
