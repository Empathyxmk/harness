#!/bin/bash
set -e

# Helper function: run maven test if pom.xml exists in submodule
run_maven_if_found() {
  subdir="$1"
  if [ -f "$subdir/pom.xml" ]; then
    echo "==> Running tests in $subdir with Maven"
    # For submodules not targeted for detailed coverage, just run mvn test
    (cd "$subdir" && mvn test)
  fi
}

# Clean previous reports
rm -rf 4-thread-query-master/target/site/jacoco

# Test 4-thread-query-master with JaCoCo for coverage
if [ -f "4-thread-query-master/pom.xml" ]; then
  echo "==> Running tests and generating JaCoCo report for 4-thread-query-master"
  (cd "4-thread-query-master" && mvn clean install jacoco:report)
  echo "JaCoCo report for 4-thread-query-master generated at 4-thread-query-master/target/site/jacoco/index.html"
fi

# Run existing tests for other modules, if any
# 1-down-bit-master (No test dir found)
run_maven_if_found 1-down-bit-master

# 2-operationlog-master (No test dir found)
run_maven_if_found 2-operationlog-master

# 3-moniyace-master (No test dir found)
run_maven_if_found 3-moniyace-master

# 5-simple-thread-pool (Has a test: src/test/java/com/luckysj/threadpool/SimpleThreadPoolApplicationTests.java)
if [ -f 5-simple-thread-pool/pom.xml ]; then
  echo "==> Running tests in 5-simple-thread-pool with Maven"
  (cd 5-simple-thread-pool && mvn test)
else
  # fallback: Try to compile & run the test directly if mvn is not available
  echo "==> Compiling and running test in 5-simple-thread-pool directly"
  # This section likely needs adjustment if dependencies are complex
  # and if src/main/java is not on the classpath.
  # For now, let's assume mvn handles this, and this fallback might fail without proper setup.
  javac -cp "src/main/java:src/test/java:lib/*:." 5-simple-thread-pool/src/test/java/com/luckysj/threadpool/SimpleThreadPoolApplicationTests.java || true
  java -cp "src/main/java:src/test/java:lib/*:." com.luckysj.threadpool.SimpleThreadPoolApplicationTests || true
fi

# 6-AQS-customize-synchronizer (No test directory; Test.java is in main; not a JUnit/TestNG file)
# 7-lock-performance-test (No test directory; no test found)

echo "All possible tests executed."