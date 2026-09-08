#!/bin/bash
# Runs ALL existing (private) tests using Maven
mvn -B -Dtest='*Test' test