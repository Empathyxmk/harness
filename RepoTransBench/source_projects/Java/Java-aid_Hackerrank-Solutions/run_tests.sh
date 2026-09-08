#!/bin/bash
set -e
cd HackerRankDashboard/Interview-Preparation-Kit
mvn clean test
cd ../../..
cd HackerRankDashboard/CoreCS/Implementation
mvn clean test
cd ../../..