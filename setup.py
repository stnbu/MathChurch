#!/usr/bin/env python

from setuptools import setup

setup(
    name="MathChurch",
    version="0.0.10",
    description="Subs-driven presentation, with TTS audio (and more)",
    author="Mike Burr",
    author_email="mb+church@unintuitive.org",
    url="https://github.com/stnbu/MathChurch",
    packages=["pulpit"],
    scripts=["tbob/tbob"],
    entry_points={"console_scripts": ["_tbob_helper = tbob.__main__:main"]},
)
