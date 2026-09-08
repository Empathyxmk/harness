#!/bin/bash
coverage erase
coverage run --branch -m pytest test/
coverage report -m