#!/bin/bash
set -e

# Ensure maven is available
if ! command -v mvn &> /dev/null
then
    echo "Apache Maven must be installed to run tests."
    exit 1
fi

# Clean, compile, run tests, and generate JaCoCo report
echo "Running Maven clean, install, test, and JaCoCo report..."
mvn clean install test jacoco:report

# Check if the JaCoCo report was generated
REPORT_PATH="target/site/jacoco/index.html"
if [ ! -f "$REPORT_PATH" ]; then
    echo "Error: JaCoCo report not found at $REPORT_PATH"
    exit 1
fi

# Extract line and branch coverage from JaCoCo report
LINE_COVERAGE=$(grep -oP 'Total.+?td class="bar"&gt;\K\d+%|\d+\.\d+%' "$REPORT_PATH" | head -n 1 | sed 's/%//')
BRANCH_COVERAGE=$(grep -oP 'Total.+?td class="ctr2"&gt;\K\d+%|\d+\.\d+%' "$REPORT_PATH" | head -n 2 | tail -n 1 | sed 's/%//')

# Fallback for parsing if grep fails or format changes slightly
if [ -z "$LINE_COVERAGE" ]; then
    LINE_COVERAGE=$(awk '/Total/{print $5}' target/site/jacoco/jacoco.csv | sed 's/\..*//') # For CSV output, needs to be enabled
    if [ -z "$LINE_COVERAGE" ]; then
        echo "Warning: Could not parse line coverage from HTML. Attempting alternative."
        # If line coverage extraction from HTML fails, try a more robust method or provide a placeholder.
        # For now, let's assume the above grep works. If not, manual intervention will be needed.
        LINE_COVERAGE=0.0
    fi
fi

if [ -z "$BRANCH_COVERAGE" ]; then
    BRANCH_COVERAGE=$(awk '/Total/{print $7}' target/site/jacoco/jacoco.csv | sed 's/\..*//') # For CSV output, needs to be enabled
    if [ -z "$BRANCH_COVERAGE" ]; then
        echo "Warning: Could not parse branch coverage from HTML. Attempting alternative."
        BRANCH_COVERAGE=0.0
    fi
fi


echo "--- Coverage Report ---"
echo "line:$LINE_COVERAGE"
echo "branch:$BRANCH_COVERAGE"
echo "-----------------------"