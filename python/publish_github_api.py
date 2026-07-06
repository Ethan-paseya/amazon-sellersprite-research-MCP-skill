#!/usr/bin/env python3
from sellersprite_skill_tools import main

raise SystemExit(main(["publish-github-api", *(__import__("sys").argv[1:])]))
