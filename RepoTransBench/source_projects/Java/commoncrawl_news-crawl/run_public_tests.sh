#!/bin/bash
# Runs ONLY public tests using Maven
mvn -B -Dtest='*PublicTest' test