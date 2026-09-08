#!/bin/bash
# Run only public tests in the project
mvn -Dtest=**/*PublicTest test