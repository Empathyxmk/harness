#!/bin/bash
set -e

# Ensure test directory exists
if [ ! -d src/test/java ]; then
  echo "No tests to run. Exiting."
  exit 0
fi

# Add JUnit dependency and JaCoCo if missing in pom.xml
if ! grep -q 'junit' pom.xml; then
  echo "Adding JUnit and JaCoCo plugins to pom.xml..."
  # Use an in-place edit, idempotent (won't duplicate)
  awk '
    /<\/dependencies>/ && !x { print "        <dependency>\n            <groupId>junit</groupId>\n            <artifactId>junit</artifactId>\n            <version>4.13.2</version>\n            <scope>test</scope>\n        </dependency>"; x=1 }
    { print }
    /<\/plugins>/ && !y {
      print "            <plugin>\n                <groupId>org.jacoco</groupId>\n                <artifactId>jacoco-maven-plugin</artifactId>\n                <version>0.8.10</version>\n                <executions>\n                    <execution>\n                        <goals>\n                            <goal>prepare-agent</goal>\n                        </goals>\n                    </execution>\n                    <execution>\n                        <id>report</id>\n                        <phase>test</phase>\n                        <goals>\n                            <goal>report</goal>\n                        </goals>\n                    </execution>\n                </executions>\n            </plugin>"; y=1
    }
  ' pom.xml > pom.xml.tmp && mv pom.xml.tmp pom.xml
fi

# Run tests and collect coverage
mvn test jacoco:report

# Print location of report for convenience
echo "JaCoCo report generated at target/site/jacoco/index.html"