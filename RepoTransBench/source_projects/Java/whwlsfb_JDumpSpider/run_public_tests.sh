#!/bin/bash
# Run ONLY the public tests using Maven, leveraging Maven's test includes
mvn test -Dtest='*PublicTest'