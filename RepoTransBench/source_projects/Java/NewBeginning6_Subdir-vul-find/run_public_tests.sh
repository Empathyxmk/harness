#!/bin/bash
# Runs only public test classes (those matching *PublicTest.java).
mvn -Dtest='*PublicTest' test