#!/bin/bash
cd pikaq-demos/pikaq-web-demo
# Run only original/private tests (not *PublicTest)
mvn -Dtest='*Test,!*PublicTest' test