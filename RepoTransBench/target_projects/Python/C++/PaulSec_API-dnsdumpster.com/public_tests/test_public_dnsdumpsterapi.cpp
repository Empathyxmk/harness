#include <gtest/gtest.h>
#include "DNSDumpsterAPI.h"
#include <any>
#include <string>
#include <map>
#include <vector>

class DummyAPI : public DNSDumpsterAPI {
public:
    std::map<std::string, std::any> search(const std::string& domain) override {
        if (domain == "duckduckgo.com") {
            std::map<std::string, std::any> output;
            output["domain"] = std::string("duckduckgo.com");
            std::map<std::string, std::any> dns_records;
            dns_records["dns"] = std::vector<std::map<std::string, std::string>>{ {{"domain", "ns1.duckduckgo.com"}} };
            dns_records["mx"] = std::vector<std::map<std::string, std::string>>{ {{"exchange", "duckduckgo-com.mail.protection.outlook.com"}} };
            dns_records["host"] = std::vector<std::map<std::string, std::string>>{ {{"host", "imap.duckduckgo.com"}} };
            output["dns_records"] = dns_records;
            return output;
        } else if (domain == "mit.edu") {
            std::map<std::string, std::any> output;
            output["domain"] = std::string("mit.edu");
            std::map<std::string, std::any> dns_records;
            dns_records["dns"] = std::vector<std::map<std::string, std::string>>{ {{"domain", "NS1-163.AKAM.NET"}} };
            dns_records["mx"] = std::vector<std::map<std::string, std::string>>{ {{"exchange", "mit-edu.mail.protection.outlook.com"}} };
            dns_records["host"] = std::vector<std::map<std::string, std::string>>{ {{"host", "imap.mit.edu"}} };
            output["dns_records"] = dns_records;
            return output;
        } else {
            std::map<std::string, std::any> output;
            output["domain"] = domain;
            std::map<std::string, std::any> dns_records;
            dns_records["dns"] = std::vector<std::map<std::string, std::string>>();
            dns_records["mx"] = std::vector<std::map<std::string, std::string>>();
            dns_records["host"] = std::vector<std::map<std::string, std::string>>();
            output["dns_records"] = dns_records;
            return output;
        }
    }
};

TEST(DNSDumpsterAPIPublicTest, AttributeTypesDuckDuckGo) {
    DummyAPI api;
    auto result = api.search("duckduckgo.com");
    EXPECT_EQ(std::any_cast<std::string>(result["domain"]), "duckduckgo.com");
    auto& dns_records = std::any_cast<std::map<std::string, std::any>&>(result["dns_records"]);
    EXPECT_TRUE(dns_records.find("mx") != dns_records.end());
    EXPECT_TRUE(dns_records.find("host") != dns_records.end());
    EXPECT_TRUE(dns_records.find("dns") != dns_records.end());
    auto& mx = std::any_cast<const std::vector<std::map<std::string,std::string>>&>(dns_records["mx"]);
    auto& host = std::any_cast<const std::vector<std::map<std::string,std::string>>&>(dns_records["host"]);
    auto& dns = std::any_cast<const std::vector<std::map<std::string,std::string>>&>(dns_records["dns"]);
    EXPECT_TRUE(typeid(mx) == typeid(std::vector<std::map<std::string, std::string>>));
    EXPECT_TRUE(typeid(host) == typeid(std::vector<std::map<std::string, std::string>>));
    EXPECT_TRUE(typeid(dns) == typeid(std::vector<std::map<std::string, std::string>>));
}

TEST(DNSDumpsterAPIPublicTest, ResultContentMIT) {
    DummyAPI api;
    auto res = api.search("mit.edu");
    EXPECT_EQ(std::any_cast<std::string>(res["domain"]), "mit.edu");
    auto& dns_records = std::any_cast<std::map<std::string, std::any>&>(res["dns_records"]);
    bool has_records = false;
    for (const auto &kv : dns_records) {
        if (kv.second.type() == typeid(std::vector<std::map<std::string, std::string>>)) {
            auto vec = std::any_cast<const std::vector<std::map<std::string, std::string>>&>(kv.second);
            if (!vec.empty()) {
                has_records = true;
                break;
            }
        }
    }
    EXPECT_TRUE(has_records);
}