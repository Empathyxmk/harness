#!/bin/bash
set -e

# Helper function: run maven test if pom.xml exists in submodule and the corresponding public test folder exists
run_maven_public_if_found() {
  subdir="$1"
  testdir="$2"
  if [ -f "$subdir/pom.xml" ] && [ -d "$testdir" ]; then
    echo "==> Running public tests in $subdir"
    (cd "$subdir" && mvn test)
  fi
}

# 4-thread-query-master public test
if [ -f 4-thread-query-master/pom.xml ]; then
  cp 4-thread-query-master/src/test/java/com/luckysj/demo/concurrent/UserServiceImplPublicTest.java 4-thread-query-master/src/test/java/com/luckysj/demo/concurrent/UserServiceImplTest.java
  (cd 4-thread-query-master && mvn test)
  git checkout -- 4-thread-query-master/src/test/java/com/luckysj/demo/concurrent/UserServiceImplTest.java
fi

# 5-simple-thread-pool public test
if [ -f 5-simple-thread-pool/pom.xml ]; then
  cp 5-simple-thread-pool/src/test/java/com/luckysj/threadpool/MainPublicTest.java 5-simple-thread-pool/src/test/java/com/luckysj/threadpool/MainTest.java
  (cd 5-simple-thread-pool && mvn test)
  git checkout -- 5-simple-thread-pool/src/test/java/com/luckysj/threadpool/MainTest.java
fi

# 3-moniyace-master public test: Direct JUnit run (since test is not under main/test split or pom not sure)
if [ -f 3-moniyace-master/pom.xml ]; then
  mkdir -p 3-moniyace-master/src/test/java/com/luckysj/demo/concurrent/
  cp 3-moniyace-master/src/test/java/com/luckysj/demo/concurrent/ConcurrencePublicTest.java 3-moniyace-master/src/test/java/com/luckysj/demo/concurrent/ConcurrenceTest.java
  (cd 3-moniyace-master && mvn test)
  git checkout -- 3-moniyace-master/src/test/java/com/luckysj/demo/concurrent/ConcurrenceTest.java || true
fi

# 6-AQS-customize-synchronizer public test
if [ -d 6-AQS-customize-synchronizer/src/test/java/com/luckysj/synchronizer ]; then
  echo "==> Running AQS custom synchronizer public test"
  (cd 6-AQS-customize-synchronizer && mvn test)
fi

# 7-lock-performance-test public test
if [ -d 7-lock-performance-test/src/test/java/com/luckys/locktest ]; then
  echo "==> Running lock performance public test"
  (cd 7-lock-performance-test && mvn test)
fi