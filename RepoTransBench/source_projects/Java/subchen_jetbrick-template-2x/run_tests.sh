#!/bin/bash
set -e

# Only test and report coverage in jetbrick-template, as that's where JaCoCo config and most sources are.
cd jetbrick-template
mvn clean test jacoco:report
cd ..

# Run tests in integration/web modules if needed, but most functional/coverage is in the module above
for m in jetbrick-template-jfinal3 jetbrick-template-struts; do
  if [ -f $m/pom.xml ]; then
    (cd $m && mvn test)
  fi
done