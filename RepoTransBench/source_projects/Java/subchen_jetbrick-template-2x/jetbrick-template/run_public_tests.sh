#!/bin/bash
# Run ONLY public tests across all jetbrick-template modules

# Run *PublicTest.java in all modules (root and submodules)
mvn -Dtest=*PublicTest test