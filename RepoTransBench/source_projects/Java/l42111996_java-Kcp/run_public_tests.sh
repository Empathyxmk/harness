#!/bin/bash
set -e
echo "Running public tests for kcp-fec..."
cd kcp-fec
mvn -Dtest=com.backblaze.erasure.FecPublicTest,com.backblaze.erasure.ReedSolomonPublicTest,com.backblaze.erasure.GaloisPublicTest,com.backblaze.erasure.MatrixPublicTest test
cd ..

echo "Running public tests for kcp-example..."
cd kcp-example
mvn -Dtest=test.KcpServerExamplesPublicTest test
cd ..