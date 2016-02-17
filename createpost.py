#!/usr/bin/python3.5

from subprocess import call
from datetime import datetime as d
import sys


def write_to_file(path, lines):
    file = open(path, 'w', encoding="UTF8")
    file.writelines(lines)
    file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply name of post")
        exit(1)

    post = sys.argv[-1]

    now = d.now()
    date_str = "{0}-{1}-{2}".format(now.year, now.month, now.day)

    lines = [
        "---\n",
        "layout: post\n",
        "title: \"%s\"\n" % post,
        "date: %s\n" % date_str,
        "categories: experimental\n",
        "---\n"
    ]

    postname = "_posts/{0}-{1}.markdown".format(date_str, post)

    call(["touch", postname])
    write_to_file(postname, lines)
    call(["gvim", postname])
