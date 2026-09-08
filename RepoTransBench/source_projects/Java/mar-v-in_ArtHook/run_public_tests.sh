#!/bin/bash
# Run ONLY public test classes for the xposed module

cd xposed
./../gradlew test --tests "de.larma.arthook.xposed.XposedPublicTest"
./../gradlew test --tests "de.larma.arthook.xposed.RuntimeInitPublicTest"
./../gradlew test --tests "de.larma.arthook.xposed.UtilsPublicTest"
./../gradlew test --tests "de.larma.arthook.xposed.ZygoteInitPublicTest"
cd ..