#!/bin/bash
cd pikaq-demos/pikaq-web-demo
# Run only public tests by specifying *PublicTest pattern
mvn -Dtest=*PublicTest test