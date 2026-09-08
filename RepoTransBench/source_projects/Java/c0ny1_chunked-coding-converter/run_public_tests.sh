#!/bin/bash
echo "Running only public tests..."
mvn -Dtest=ChunkedCodingConverterPublicTest test