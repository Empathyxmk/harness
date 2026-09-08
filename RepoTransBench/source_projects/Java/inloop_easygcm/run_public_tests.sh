#!/bin/bash
cd easygcm-lib
./gradlew clean testDebugUnitTest --no-daemon --console=plain -Dtest.single="*PublicTest"
cd ..
echo "Public tests run."