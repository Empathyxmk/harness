#!/bin/bash
set -e

echo "Ensuring Maven is installed..."
if ! command -v mvn &> /dev/null
then
    echo "Maven not found. Installing..."
    apt-get update && apt-get install -y maven
fi

if [ -f pom.xml ]; then
  echo "Running tests in root module with JaCoCo coverage"
  # Clean, then test and generate JaCoCo report
  mvn clean install jacoco:report
else
  echo "No pom.xml found in the root directory. Cannot run Maven tests."
  exit 1
fi

# Check if JaCoCo report was generated
JACOCO_CSV_REPORT="target/site/jacoco/jacoco.csv"
if [ -f "$JACOCO_CSV_REPORT" ]; then
    echo "JaCoCo report (jacoco.csv) generated successfully. Parsing coverage..."

    # Extracting coverage for KafkaService class from jacoco.csv
    # Assuming the line for KafkaService is present and contains the relevant data
    # The columns are typically: GROUP,PACKAGE,CLASS,INSTRUCTION_MISSED,INSTRUCTION_COVERED,BRANCH_MISSED,BRANCH_COVERED,LINE_MISSED,LINE_COVERED,COMPLEXITY_MISSED,COMPLEXITY_COVERED,METHOD_MISSED,METHOD_COVERED
    # We are interested in LINE_MISSED (col 9), LINE_COVERED (col 10), BRANCH_MISSED (col 7), BRANCH_COVERED (col 8)

    # Grep for the KafkaService line, skip header, and use awk to extract columns
    # Adjust column numbers if the CSV format varies
    REPORT_LINE=$(grep "com.example.kafkaservice,KafkaService" "$JACOCO_CSV_REPORT" | tail -n 1)

    if [ -z "$REPORT_LINE" ]; then
        echo "ERROR: Could not find KafkaService entry in jacoco.csv."
        LINE_COVERAGE=0.0
        BRANCH_COVERAGE=0.0
    else
        # Extract values using awk based on expected column indices (0-indexed for awk)
        # Columns in JaCoCo CSV are typically:
        # 0: GROUP, 1: PACKAGE, 2: CLASS,
        # 3: INSTRUCTION_MISSED, 4: INSTRUCTION_COVERED,
        # 5: BRANCH_MISSED, 6: BRANCH_COVERED,
        # 7: LINE_MISSED, 8: LINE_COVERED,
        # 9: COMPLEXITY_MISSED, 10: COMPLEXITY_COVERED,
        # 11: METHOD_MISSED, 12: METHOD_COVERED

        LINE_MISSED=$(echo "$REPORT_LINE" | awk -F',' '{print $8}')
        LINE_COVERED=$(echo "$REPORT_LINE" | awk -F',' '{print $9}')
        BRANCH_MISSED=$(echo "$REPORT_LINE" | awk -F',' '{print $6}')
        BRANCH_COVERED=$(echo "$REPORT_LINE" | awk -F',' '{print $7}')

        if [ -z "$LINE_MISSED" ] || [ -z "$LINE_COVERED" ] || [ -z "$BRANCH_MISSED" ] || [ -z "$BRANCH_COVERED" ]; then
            echo "ERROR: Failed to parse coverage numbers from jacoco.csv. Raw line: $REPORT_LINE"
            LINE_COVERAGE=0.0
            BRANCH_COVERAGE=0.0
        else
            TOTAL_LINES=$((LINE_MISSED + LINE_COVERED))
            TOTAL_BRANCHES=$((BRANCH_MISSED + BRANCH_COVERED))

            if [ "$TOTAL_LINES" -gt 0 ]; then
                LINE_COVERAGE=$(echo "scale=2; ($LINE_COVERED * 100.0) / $TOTAL_LINES" | bc)
            else
                LINE_COVERAGE=0.0
            fi

            if [ "$TOTAL_BRANCHES" -gt 0 ]; then
                BRANCH_COVERAGE=$(echo "scale=2; ($BRANCH_COVERED * 100.0) / $TOTAL_BRANCHES" | bc)
            else
                BRANCH_COVERAGE=0.0
            fi
        fi
    fi

    echo "Line Coverage: $LINE_COVERAGE%"
    echo "Branch Coverage: $BRANCH_COVERAGE%"
    echo "$LINE_COVERAGE" > line_coverage.txt
    echo "$BRANCH_COVERAGE" > branch_coverage.txt

else
    echo "ERROR: JaCoCo report ($JACOCO_CSV_REPORT) not found. Check Maven output for errors."
    exit 1
fi