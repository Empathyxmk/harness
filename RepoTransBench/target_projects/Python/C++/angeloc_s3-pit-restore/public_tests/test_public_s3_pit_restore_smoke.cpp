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
    // Run command, pipe both stdout/stderr to output
    std::string fullcmd = cmd + " 2>&1";
    std::array<char, 256> buffer;
    std::string out;
    FILE* pipe = popen(fullcmd.c_str(), "r");
    if (!pipe) return {"", "", 1};
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        out += buffer.data();
    }
    int returncode = pclose(pipe);
    // Both out; we treat as error out as well
    return {out, out, WEXITSTATUS(returncode)};
}

TEST(S3PitRestoreSmokePublic, VersionPublic) {
    // Use -V instead of --version; expect code 2 + error about missing bucket
    std::stringstream ss;
    ss << "python3 s3-pit-restore -V";
    ExecResult res = exec_script(ss.str());
    EXPECT_EQ(res.returncode, 2);
    auto low = res.stderr_str;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_TRUE(low.find("required") != std::string::npos || low.find("bucket") != std::string::npos);
}

TEST(S3PitRestoreSmokePublic, InvalidArgPublic) {
    // Invalid flag; code 2, output mentions usage or error
    std::stringstream ss;
    ss << "python3 s3-pit-restore --notarealarg";
    ExecResult res = exec_script(ss.str());
    EXPECT_EQ(res.returncode, 2);
    auto low = res.stderr_str;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_TRUE(low.find("usage") != std::string::npos || low.find("error") != std::string::npos);
}