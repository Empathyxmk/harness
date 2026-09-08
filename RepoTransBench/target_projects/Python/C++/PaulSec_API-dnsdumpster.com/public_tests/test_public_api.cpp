#include <gtest/gtest.h>
#include "DNSDumpsterAPI.h"
#include <any>
#include <string>
#include <map>
#include <vector>

class DummyAPI : public DNSDumpsterAPI {
public:
    std::map<std::string, std::any> search(const std::string& domain) override {
        // Faked results for public test (domain-specific)
        if (domain == "openai.com") {
            std::map<std::string, std::any> output;
            output["domain"] = std::string("openai.com");
            std::map<std::string, std::any> dns_records;
            dns_records["dns"] =
                std::vector<std::map<std::string, std::string>>{ {{"domain", "ns1.openai.com"}} };
            dns_records["mx"] =
                std::vector<std::map<std::string, std::string>>{ {{"exchange", "aspmx.l.google.com"}} };
            dns_records["host"] =
                std::vector<std::map<std::string, std::string>>{ {{"host", "mail.openai.com"}} };
            output["dns_records"] = dns_records;
            return output;
        } else if (domain == "duckduckgo.com") {
            std::map<std::string, std::any> output;
            output["domain"] = std::string("duckduckgo.com");
            std::map<std::string, std::any> dns_records;
            dns_records["dns"] =
                std::vector<std::map<std::string, std::string>>{ {{"domain", "ns1.duckduckgo.com"}} };
            dns_records["mx"] =
                std::vector<std::map<std::string, std::string>>{ {{"exchange", "duckduckgo-com.mail.protection.outlook.com"}} };
            dns_records["host"] =
                std::vector<std::map<std::string, std::string>>{ {{"host", "imap.duckduckgo.com"}} };
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

TEST(DNSDumpsterAPIPublicTest, SearchResultStructureOpenAI) {
    DummyAPI api;
    auto result = api.search("openai.com");
    ASSERT_TRUE(result.find("domain") != result.end());
    EXPECT_EQ(std::any_cast<std::string>(result["domain"]), "openai.com");
    ASSERT_TRUE(result.find("dns_records") != result.end());
    auto& dns_records = std::any_cast<std::map<std::string, std::any>&>(result["dns_records"]);
    EXPECT_TRUE(dynamic_cast<std::map<std::string, std::any>*>(&dns_records) != nullptr);

    // At least one record list is not empty
    bool found = false;
    for (const auto& kv : dns_records) {
        if (kv.second.type() == typeid(std::vector<std::map<std::string, std::string>>)) {
            auto vec = std::any_cast<const std::vector<std::map<std::string, std::string>>&>(kv.second);
            if (!vec.empty()) {
                found = true;
                break;
            }
        }
    }
    EXPECT_TRUE(found);
}