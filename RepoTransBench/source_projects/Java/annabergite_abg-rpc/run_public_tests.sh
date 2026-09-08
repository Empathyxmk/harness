#!/bin/bash
# Run public tests only for abg-register-zk, skip signing/javadoc
cd abg-register-zk
mvn -Dgpg.skip=true -Dmaven.javadoc.skip=true test -Dtest='**/*PublicTest.java'