#!/bin/bash
set -e
cd HackerRankDashboard/Interview-Preparation-Kit
mvn -Dtest=*PublicTest test
cd ../../..
cd HackerRankDashboard/CoreCS/Implementation
mvn -Dtest=*PublicTest test
cd ../../..