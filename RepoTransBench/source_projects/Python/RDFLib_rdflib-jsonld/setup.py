#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import re

from os.path import dirname
from setuptools import setup

ROOT = dirname(__file__)

RE_REQUIREMENT = re.compile(r"^\s*-r\s*(?P<filename>.*)$")

RE_MD_CODE_BLOCK = re.compile(r"