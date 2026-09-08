#!/bin/bash
export PYTHONPATH=.
coverage run --branch --source=tools,convert2onnx,onnxapi -m unittest discover -v
coverage report -m