#include <gtest/gtest.h>
#include <stdexcept>
#include "graphios_backends.h"
#include <fstream>

TEST(BackendLoad, Invalid) {
    EXPECT_THROW(load_backend("doesnotexist", ""), std::invalid_argument);
}

TEST(BackendLoad, FileBackend) {
    FileBackend* backend = static_cast<FileBackend*>(load_backend("file", "/tmp/testfile"));
    ASSERT_NE(backend, nullptr);
    EXPECT_EQ(typeid(*backend).name(), typeid(FileBackend).name());
    delete backend;
}

TEST(BackendLoad, CarbonBackend) {
    CarbonBackend* backend = static_cast<CarbonBackend*>(load_backend("carbon", "host", 1234));
    ASSERT_NE(backend, nullptr);
    EXPECT_EQ(typeid(*backend).name(), typeid(CarbonBackend).name());
    delete backend;
}

TEST(BackendLoad, UDPBackend) {
    UDPSendBackend* backend = static_cast<UDPSendBackend*>(load_backend("udp", "host", 1001));
    ASSERT_NE(backend, nullptr);
    EXPECT_EQ(typeid(*backend).name(), typeid(UDPSendBackend).name());
    delete backend;
}

TEST(BackendFile, FileBackendSendMetric) {
    FakeMetric metric{"a", "b", "c", "1", "2"};
    const std::string fpath = "test_graphios_backends_outfile.txt";
    FileBackend back(fpath);
    back.send_metric(metric);
    std::ifstream ifs(fpath);
    std::string data((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
    EXPECT_NE(data.find("a b c 1 2"), std::string::npos);
    ifs.close();
    std::remove(fpath.c_str());
}

// CarbonBackend send_metric (dummy, just succeeds)
TEST(BackendCarbon, CarbonBackendSendMetric) {
    FakeMetric metric{"h", "s", "m", "5", "18"};
    CarbonBackend back("test.host", 2003);
    back.send_metric(metric);
    SUCCEED();
}

// UDPBackend send_metric (dummy, just succeeds)
TEST(BackendUDP, UDPBackendSendMetric) {
    FakeMetric metric{"hosty", "svc", "metric", "3", "6"};
    UDPSendBackend back("testhost", 2222);
    back.send_metric(metric);
    SUCCEED();
}