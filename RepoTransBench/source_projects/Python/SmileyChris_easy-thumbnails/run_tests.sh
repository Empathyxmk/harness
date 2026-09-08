#!/bin/bash
coverage run --branch --source=easy_thumbnails -m pytest easy_thumbnails/tests
coverage report