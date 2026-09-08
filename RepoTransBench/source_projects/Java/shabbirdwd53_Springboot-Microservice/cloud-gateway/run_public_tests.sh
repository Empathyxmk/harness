#!/bin/bash
# This script runs only the public test class(es) for cloud-gateway
./mvnw -f ./pom.xml -Dtest=com.dailycodebuffer.cloud.gateway.FallBackMethodControllerPublicTest test