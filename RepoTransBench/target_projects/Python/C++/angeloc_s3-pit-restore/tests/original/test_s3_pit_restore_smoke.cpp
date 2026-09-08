#include <gtest/gtest.h>
#include <string>
#include <array>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <iostream>
#include <sstream>

// Helper to run a command and capture output/exit code
struct ExecResult {
    std::string stdout_str;
    std::string stderr_str;
    int returncode;
};

ExecResult exec_script(const std::string& cmd) {
    // Python-like: runs the command, returns a result struct
    // This implementation is Unix-specific and uses popen on stdout; for stderr need extra pipe logic
    std::string fullcmd = cmd + " 2>&1";
    std::array<char, 256> buffer;
    std::string out;
    FILE* pipe = popen(fullcmd.c_str(), "r");
    if (!pipe) return {"", "", 1};
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        out += buffer.data();
    }
    int returncode = pclose(pipe);
    // As we redirected stderr to stdout, assign output accordingly
    return {out, out, WEXITSTATUS(returncode)};
}

TEST(S3PitRestoreSmoke, Help) {
    // Simulate checking the --help output and exit code
    std::stringstream ss;
    ss << "python3 s3-pit-restore --help";
    ExecResult res = exec_script(ss.str());
    // Should mention usage, exit code 0
    auto low = res.stdout_str;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_NE(low.find("usage"), std::string::npos);
    EXPECT_EQ(res.returncode, 0);
}

TEST(S3PitRestoreSmoke, MissingBucket) {
    // Simulate missing bucket, expect code 2 and relevant error in output
    std::stringstream ss;
    ss << "python3 s3-pit-restore --version";
    ExecResult res = exec_script(ss.str());
    EXPECT_EQ(res.returncode, 2);
    // Check "required" or "bucket" appears in output
    auto low = res.stderr_str;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_TRUE(low.find("required") != std::string::npos || low.find("bucket") != std::string::npos);
}