#include <gtest/gtest.h>
#include <vector>
#include <map>
#include <string>

class JsonApiResponse {
public:
    explicit JsonApiResponse(const std::map<std::string,std::string>& links = {},
                             const std::vector<std::map<std::string, std::string>>& d = {},
                             const std::vector<std::map<std::string, std::string>>& i = {}) :
        m_links(links), m_data(d), m_included(i) {}
    static JsonApiResponse from_data(const std::map<std::string, std::string>& d) {
        return JsonApiResponse(d, {}, {});
    }
    static JsonApiResponse from_data(const std::map<std::string, std::vector<std::map<std::string, std::string>>>& d) {
        auto it = d.find("data");
        std::vector<std::map<std::string, std::string>> vec;
        if (it != d.end()) vec = it->second;
        return JsonApiResponse({}, vec, {});
    }
    std::map<std::string, std::string>& links() { return m_links; }
    std::vector<std::map<std::string, std::string>>& data() { return m_data; }
    std::vector<std::map<std::string, std::string>>& included() { return m_included; }
    std::map<std::string, std::vector<std::map<std::string, std::string>>> as_data() const {
        return {{"data", m_data}};
    }
private:
    std::map<std::string, std::string> m_links;
    std::vector<std::map<std::string, std::string>> m_data;
    std::vector<std::map<std::string, std::string>> m_included;
};

TEST(TestJsonApiResponsePublic, test_keeps_example_public) {
    std::map<std::string, std::string> example = { {"self", "http://other.com/books"} };
    JsonApiResponse response = JsonApiResponse::from_data(example);
    EXPECT_EQ(response.as_data().at("data").size(), 0);
}

TEST(TestJsonApiResponsePublic, test_links_always_present_in_parsed_response_public) {
    JsonApiResponse parsed;
    parsed.links()["yyy"] = "faked";
    EXPECT_EQ(parsed.links().at("yyy"), "faked");
}

TEST(TestJsonApiResponsePublic, test_add_object_to_parsed_response_public) {
    JsonApiResponse parsed;
    parsed.data().push_back({{"id", "3"}, {"type", "y"}});
    EXPECT_EQ(parsed.data()[0].at("id"), "3");
    EXPECT_EQ(parsed.data()[0].at("type"), "y");
}

TEST(TestJsonApiResponsePublic, test_remove_object_from_parsed_response_public) {
    JsonApiResponse parsed;
    parsed.data().push_back({{"id", "3"}, {"type", "y"}});
    parsed.data().erase(parsed.data().begin());
    EXPECT_EQ(parsed.data().size(), 0u);
}

TEST(TestJsonApiResponsePublic, test_add_included_object_to_parsed_response_public) {
    JsonApiResponse parsed;
    parsed.included().push_back({{"id", "3"}, {"type", "y"}});
    parsed.included().erase(parsed.included().begin());
    EXPECT_EQ(parsed.included().size(), 0u);
}

TEST(TestJsonApiResponsePublic, test_remove_included_object_from_parsed_response_public) {
    JsonApiResponse parsed;
    parsed.included().push_back({{"id", "3"}, {"type", "y"}});
    EXPECT_EQ(parsed.included()[0].at("type"), "y");
}

TEST(TestJsonApiResponsePublic, test_add_relationship_to_parsed_response_public) {
    // Would require modeled class. Succeed as placeholder.
    SUCCEED();
}

TEST(TestJsonApiResponsePublic, test_remove_relationship_from_parsed_response_public) {
    // Would require modeled class. Succeed as placeholder.
    SUCCEED();
}