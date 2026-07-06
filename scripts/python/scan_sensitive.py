#!/usr/bin/env python3
from sellersprite_skill_tools import main

raise SystemExit(main(["scan-sensitive", *(__import__("sys").argv[1:])]))
