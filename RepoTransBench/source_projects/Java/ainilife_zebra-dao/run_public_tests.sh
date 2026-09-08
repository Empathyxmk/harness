#!/bin/bash
# Only runs '*PublicTest' classes as public test suite
mvn -Dtest='*PublicTest' test