#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <map>
#include <memory>
#include "lib/Scanner.h"

// Dummy class to mimic TLV8Box in the scanner tests
class DummyTLVBox {
public:
    explicit DummyTLVBox(std::map<int, std::vector<uint8_t>> d) : _d(std::move(d)) {}
    std::map<int, std::vector<uint8_t>> toDict() const { return _d; }
    std::map<int, std::vector<uint8_t>> _d;
};

class DummyScanEntry {
public:
    DummyScanEntry() : addr("AA:BB:01:FA:EE:DC"), scan_data({}) {}
    std::string addr;
    std::vector<std::tuple<int, void*, std::string>> scan_data;
    std::vector<std::tuple<int, void*, std::string>> getScanData() const { return scan_data; }
};

TEST(Scanner, GetPWSTLV_WrongCompany) {
    PWSScanner scanner("testssid");
    EXPECT_EQ(scanner.getPWSTLV({0x00, 0x00, 'A', 'B', 'C'}), std::vector<uint8_t>());
}

TEST(Scanner, GetPWSTLV_RightCompany) {
    // Patch TLV8Box::decodeFromData to always return DummyTLVBox with expected dict
    // Assume dependency injection or a static interface to swap the decodeFromData function for tests.
    auto oldDecode = TLV8Box::decodeFromData;
    TLV8Box::decodeFromData = [](const std::vector<uint8_t>&) {
        return DummyTLVBox({{0x0F, {'P','A','Y','L','O','A','D'}}});
    };
    PWSScanner scanner("testssid");
    std::vector<uint8_t> res = scanner.getPWSTLV({0x4c, 0x00, 0xab, 0xcd, 0xef});
    EXPECT_EQ(res, std::vector<uint8_t>({'P','A','Y','L','O','A','D'}));
    TLV8Box::decodeFromData = oldDecode; // restore
}

TEST(Scanner, IsSSIDInTLV) {
    PWSScanner scanner("SSID42");
    std::vector<uint8_t> val = {scanner.ssidHash[0], scanner.ssidHash[1], scanner.ssidHash[2]};
    // Input ending matches ssidHash[:3]
    std::vector<uint8_t> input = {'x','x','x','x'};
    input.insert(input.end(), val.begin(), val.end());
    EXPECT_EQ(scanner.isSSIDInTLV(input), true);
    // Input that does not match
    std::vector<uint8_t> bad_input = {'a','b','c','1','2','3'};
    EXPECT_EQ(scanner.isSSIDInTLV(bad_input), false);
}

TEST(Scanner, HandleDiscoverySetsResult) {
    // getPWSTLV returns matching TLV
    class DummyScan : public DummyScanEntry {
    public:
        std::string addr;
        DummyScan() : addr("Z") {}
        std::vector<std::tuple<int, void*, std::string>> getScanData() const override {
            return {{255, nullptr, "4c00abcdef"}};
        }
    };
    PWSScanner scanner("ssidX");
    scanner.getPWSTLV = [](const std::vector<uint8_t>&) {
        std::vector<uint8_t> hash = {scanner.ssidHash[0], scanner.ssidHash[1], scanner.ssidHash[2]};
        hash.insert(hash.end(), hash.begin(), hash.end());
        return hash;
    };
    scanner.isSSIDInTLV = [](const std::vector<uint8_t>&){ return true; };
    DummyScan scanEntry;
    scanner.handleDiscovery(std::make_shared<DummyScan>(scanEntry), true, true);
    EXPECT_EQ(scanner.result, &scanEntry);
}

TEST(Scanner, HandleDiscoveryNonmatching) {
    class DummyScan : public DummyScanEntry {
    public:
        std::vector<std::tuple<int, void*, std::string>> getScanData() const override {
            return {{255, nullptr, "4c00abcdef"}};
        }
    };
    PWSScanner scanner("ssid");
    scanner.getPWSTLV = [](const std::vector<uint8_t>&) { return std::vector<uint8_t>(); };
    DummyScan scan;
    scanner.handleDiscovery(std::make_shared<DummyScan>(scan), true, true);
    EXPECT_EQ(scanner.result, nullptr);
}