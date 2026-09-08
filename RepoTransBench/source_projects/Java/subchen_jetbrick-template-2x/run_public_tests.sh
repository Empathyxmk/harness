#!/bin/bash
set -e

cd jetbrick-template-jfinal3
mvn -Dtest='*PublicTest' test
cd ..