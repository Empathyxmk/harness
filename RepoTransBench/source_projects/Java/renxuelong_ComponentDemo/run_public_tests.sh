#!/bin/bash
# Run all modules' *PublicTest files using compatible Java

export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"
export PATH="$JAVA_HOME/bin:$PATH"

modules=("componentbase" "login" "share" "base")

for mod in "${modules[@]}"; do
    if [ -d "$mod" ]; then
        echo "Running $mod public unit tests..."
        (cd $mod && ../gradlew test --tests '*PublicTest' || echo "No gradle?") || true
        echo "Running $mod public android instrumented tests..."
        (cd $mod && ../gradlew connectedAndroidTest --tests '*PublicTest' || echo "No gradle?") || true
    fi
done