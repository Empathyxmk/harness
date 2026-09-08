#!/bin/bash
# Run only the public tests for the comet module
cd "$(dirname "$0")"
if [ -x ./mvnw ]; then
  ./mvnw -B -Dtest='wiki.tony.chat.comet.*PublicTest, wiki.tony.chat.comet.operation.*PublicTest' test
else
  mvn -B -Dtest='wiki.tony.chat.comet.*PublicTest, wiki.tony.chat.comet.operation.*PublicTest' test
fi