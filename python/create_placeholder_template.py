#!/usr/bin/env python3
from sellersprite_skill_tools import main

raise SystemExit(main(["create-placeholder-template", *(__import__("sys").argv[1:])]))
