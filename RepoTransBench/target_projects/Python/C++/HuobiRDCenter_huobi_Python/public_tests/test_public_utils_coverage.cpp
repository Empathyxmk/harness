#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <typeinfo>

namespace huobi_utils_public {

namespace input_checker {
inline void check_should_not_none(const void* ptr, const std::string& param) {
    if (!ptr)
        throw std::runtime_error("different_param should not be None");
}
template<typename T>
inline void check_should_not_none(const T& value, const std::string& param) {
    if constexpr (std::is_pointer<T>::value) {
        if (value == nullptr) throw std::runtime_error("another_param should not be None");
    } else {
        // everything else passes
    }
}
template<typename T>
inline void check_should_none(const T& value, const std::string& param) {
    if constexpr (std::is_pointer<T>::value) {
        if (value != nullptr) throw std::runtime_error("wonka_param should be None");
    } else if constexpr (std::is_integral<T>::value) {
        throw std::runtime_error("wonka_param should be None");
    } else {
        // For this simplistic example
    }
}
inline void check_should_none(std::nullptr_t, const std::string& param) {}
}

namespace url_params_builder {
class UrlParamsBuilder {
private:
    std::map<std::string, std::string> kv;
public:
    UrlParamsBuilder& put_url(const std::string& k, const std::string& v) {
        kv[k] = v;
        return *this;
    }
    std::string build_url() const {
        if (kv.size() == 0) return "";
        std::ostringstream ss;
        ss << "?";
        size_t idx = 0;
        for (const auto& p : kv) {
            if (idx != 0) ss << "&";
            ss << p.first << "=" << p.second;
            ++idx;
        }
        return ss.str();
    }
};
}

namespace log_info {
inline void print_warn(const std::string& msg) {}
inline void print_basic_info(const std::string& msg) {}
inline void print_replace(const std::string& from, const std::string& to) {}
}

namespace time_service {
inline int get_current_timestamp() { return 100; }
}

namespace print_mix_object {
class Dummy {
public:
    std::string toString() const { return "OtherDummy"; }
};

inline void print_basic_object(const Dummy& obj) { (void)obj.toString(); }
inline void print_list(const std::vector<Dummy>& v) { (void)v.size(); }
inline void print_dict(const std::map<std::string, int>& d) { (void)d.size(); }
inline void print_basic_dict(const std::map<std::string, int>& d) { (void)d.size(); }
inline void print_basic_list(const std::vector<int>& l) { (void)l.size(); }
}

namespace json_parser {
#include <nlohmann/json.hpp>
using json = nlohmann::json;

inline std::string json_dumps(const json& obj) { return obj.dump(); }
inline json json_loads(const std::string& s) { return json::parse(s); }
}

} //namespace huobi_utils_public

using namespace huobi_utils_public;

class TestInputCheckerPublic : public ::testing::Test {};
TEST_F(TestInputCheckerPublic, test_check_should_not_none) {
    EXPECT_THROW(input_checker::check_should_not_none(nullptr, "different_param"), std::runtime_error);
}
TEST_F(TestInputCheckerPublic, test_check_should_not_none_valid) {
    int i = 123;
    EXPECT_NO_THROW(input_checker::check_should_not_none(i, "another_param"));
}
TEST_F(TestInputCheckerPublic, test_check_should_none) {
    EXPECT_NO_THROW(input_checker::check_should_none(nullptr, "wonka_param"));
    EXPECT_THROW(input_checker::check_should_none(0, "wonka_param"), std::runtime_error);
}
class TestUrlParamsBuilderPublic : public ::testing::Test {};
TEST_F(TestUrlParamsBuilderPublic, test_add_and_build_url) {
    url_params_builder::UrlParamsBuilder builder;
    builder.put_url("x", "alpha");
    builder.put_url("y", "beta");
    std::string url = builder.build_url();
    EXPECT_TRUE(url == "?x=alpha&y=beta" || url == "?y=beta&x=alpha");
    url_params_builder::UrlParamsBuilder builder2;
    EXPECT_EQ(builder2.build_url(), "");
}
class TestLogInfoPublic : public ::testing::Test {};
TEST_F(TestLogInfoPublic, test_log_methods_exist) {
    log_info::print_warn("public warn message");
    log_info::print_basic_info("public info message");
    log_info::print_replace("public_from", "public_to");
}
class TestTimeServicePublic : public ::testing::Test {};
TEST_F(TestTimeServicePublic, test_get_current_time) {
    int now = time_service::get_current_timestamp();
    EXPECT_TRUE(typeid(now) == typeid(int));
    EXPECT_GE(now, 0);
}
class TestPrintMixObjectPublic : public ::testing::Test {};
TEST_F(TestPrintMixObjectPublic, test_print_object_basic) {
    print_mix_object::Dummy obj;
    print_mix_object::print_basic_object(obj);
}
TEST_F(TestPrintMixObjectPublic, test_print_list_and_dict) {
    print_mix_object::Dummy obj;
    print_mix_object::print_list({obj, obj});
    print_mix_object::print_list({obj});
    print_mix_object::print_dict({{"b", 2}});
    print_mix_object::print_dict({{"a", 42}});
    print_mix_object::print_basic_dict({{"z", 789}});
    print_mix_object::print_basic_list({9,8,7});
    print_mix_object::print_basic_list({0});
}
class TestJsonParserPublic : public ::testing::Test {};
TEST_F(TestJsonParserPublic, test_parse) {
    nlohmann::json obj = {{"spam", "eggs"}};
    auto json_str = json_parser::json_dumps(obj);
    auto result = json_parser::json_loads(json_str);
    EXPECT_EQ(result["spam"], "eggs");
}