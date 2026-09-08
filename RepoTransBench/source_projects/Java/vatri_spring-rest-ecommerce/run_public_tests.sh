#!/bin/bash
# Run only public tests (filtering by '*PublicTest.java')
mvn -Dtest='**/*PublicTest' test