#!/bin/bash
set -e

# Only run public tests (those with 'PublicTest' in the classname)
if [ ! -d src/test/java ]; then
  echo "No public tests to run."
  exit 0
fi

# Make sure dependencies & plugins exist (mimic run_tests.sh logic if needed)
if ! grep -q 'junit' pom.xml; then
  echo "Adding JUnit and JaCoCo plugins to pom.xml..."
  awk '
    /<\/dependencies>/ && !x { print "        <dependency>\n            <groupId>junit</groupId>\n            <artifactId>junit</artifactId>\n            <version>4.13.2</version>\n            <scope>test</scope>\n        </dependency>"; x=1 }
    { print }
    /<\/plugins>/ && !y {
      print "            <plugin>\n                <groupId>org.jacoco</groupId>\n                <artifactId>jacoco-maven-plugin</artifactId>\n                <version>0.8.10</version>\n                <executions>\n                    <execution>\n                        <goals>\n                            <goal>prepare-agent</goal>\n                        </goals>\n                    </execution>\n                    <execution>\n                        <id>report</id>\n                        <phase>test</phase>\n                        <goals>\n                            <goal>report</goal>\n                        </goals>\n                    </execution>\n                </executions>\n            </plugin>"; y=1
    }
  ' pom.xml > pom.xml.tmp && mv pom.xml.tmp pom.xml
fi

# Compile only the public test classes and run them
mvn -Dtest='*PublicTest' test jacoco:report

echo "JaCoCo report for public tests at target/site/jacoco/index.html"