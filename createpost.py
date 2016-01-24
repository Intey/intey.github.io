#!/usr/bin/python3.5

from subprocess import call
from datetime import datetime as d
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply name of post")
        exit(1)

    post = sys.argv[-1]
    now = d.now()

    call(["touch", "_posts/{0}-{1}-{2}-{3}.markdown".format(now.year,
                                                            now.month,
                                                            now.day,
                                                            post)])
