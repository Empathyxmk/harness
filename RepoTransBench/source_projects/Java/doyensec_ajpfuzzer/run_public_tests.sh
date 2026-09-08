#!/bin/bash
set -e
mvn clean test -Dtest='*PublicTest'