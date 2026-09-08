#!/bin/bash
# Run only public test classes using Gradle test filtering

# App module public tests
./gradlew :app:testDebugUnitTest --tests 'com.hankkin.taobaodetaildemo.ExamplePublicUnitTest'

# Library module public tests
./gradlew :library:testDebugUnitTest --tests 'com.hankkin.library.ExamplePublicUnitTest'
./gradlew :library:testDebugUnitTest --tests 'com.hankkin.library.CircleImageViewPublicTest'
./gradlew :library:testDebugUnitTest --tests 'com.hankkin.library.ScrollViewContainerPublicTest'
./gradlew :library:testDebugUnitTest --tests 'com.hankkin.library.MyImageLoaderPublicTest'
./gradlew :library:testDebugUnitTest --tests 'com.hankkin.library.StatusBarViewPublicTest'

# Optionally show summary results