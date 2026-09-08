#!/bin/bash
# Run ONLY public tests
# Uses Maven's -Dtest flag to run *PublicTest classes only

mvn -Dtest='*PublicTest' test