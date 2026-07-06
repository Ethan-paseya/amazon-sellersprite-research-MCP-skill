#!/usr/bin/env python3
from sellersprite_skill_tools import main

raise SystemExit(main(["check-runtime-config", *(__import__("sys").argv[1:])]))
