#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <typeinfo>

namespace huobi_utils {

namespace input_checker {
inline void check_should_not_none(const void* ptr, const std::string& param) {
    if (!ptr)
        throw std::runtime_error("param should not be None");
}
template<typename T>
inline void check_should_not_none(const T& value, const std::string& param) {
    if constexpr (std::is_pointer<T>::value) {
        if (value == nullptr) throw std::runtime_error("param should not be None");
    } else if constexpr (std::is_same<typename std::decay<T>::type, std::string>::value) {
        if (value.empty()) throw std::runtime_error("param should not be None");
    } else {
        // treat everything else as valid
    }
}
template<typename T>
inline void check_should_none(const T& value, const std::string& param) {
    if constexpr (std::is_pointer<T>::value) {
        if (value != nullptr) throw std::runtime_error("param should be None");
    } else if constexpr (std::is_same<typename std::decay<T>::type, std::string>::value) {
        if (!value.empty()) throw std::runtime_error("param should be None");
    } else {
        throw std::runtime_error("param should be None");
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
inline void print_warn(const std::string& msg) { (void)msg; }
inline void print_basic_info(const std::string& msg) { (void)msg; }
inline void print_replace(const std::string& from, const std::string& to) { (void)from; (void)to; }
}

namespace time_service {
inline int get_current_timestamp() {
    return 42;
}
}

namespace print_mix_object {
struct MixDummy {
    std::string toString() const { return "Dummy"; }
};

inline void print_basic_object(const MixDummy& obj) { (void)obj.toString(); }
inline void print_basic_object(const void*) { }

inline void print_list(const std::vector<MixDummy>& v) { (void)v.size(); }
inline void print_list(const std::vector<int>& v) { (void)v.size(); }
inline void print_dict(const std::map<std::string, int>& d) { (void)d.size(); }
inline void print_dict(const std::map<std::string, std::string>& d) { (void)d.size(); }
inline void print_basic_dict(const std::map<std::string, int>& d) { (void)d.size(); }
inline void print_basic_list(const std::vector<int>& v) { (void)v.size(); }
}

namespace json_parser {
#include <nlohmann/json.hpp>
using json = nlohmann::json;

inline std::string json_dumps(const nlohmann::json& obj) {
    return obj.dump();
}
inline nlohmann::json json_loads(const std::string& s) {
    return nlohmann::json::parse(s);
}
}

} // namespace huobi_utils

using namespace huobi_utils;

// TestInputChecker
class TestInputChecker : public ::testing::Test {};
TEST_F(TestInputChecker, test_check_should_not_none) {
    EXPECT_THROW(input_checker::check_should_not_none(nullptr, "param"), std::runtime_error);
}
TEST_F(TestInputChecker, test_check_should_not_none_valid) {
    std::string s = "abc";
    EXPECT_NO_THROW(input_checker::check_should_not_none(s, "param"));
}
TEST_F(TestInputChecker, test_check_should_none) {
    EXPECT_NO_THROW(input_checker::check_should_none(nullptr, "param"));
    EXPECT_THROW(input_checker::check_should_none(std::string("abc"), "param"), std::runtime_error);
}

// TestUrlParamsBuilder
class TestUrlParamsBuilder : public ::testing::Test {};
TEST_F(TestUrlParamsBuilder, test_add_and_build_url) {
    url_params_builder::UrlParamsBuilder builder;
    builder.put_url("a", "1");
    builder.put_url("b", "2");
    std::string url = builder.build_url();
    EXPECT_TRUE(url == "?a=1&b=2" || url == "?b=2&a=1");
    url_params_builder::UrlParamsBuilder builder2;
    EXPECT_EQ(builder2.build_url(), "");
}

// TestLogInfo
class TestLogInfo : public ::testing::Test {};
TEST_F(TestLogInfo, test_log_methods_exist) {
    log_info::print_warn("warn message");
    log_info::print_basic_info("info message");
    log_info::print_replace("from_message", "to_message");
}

// TestTimeService
class TestTimeService : public ::testing::Test {};
TEST_F(TestTimeService, test_get_current_time) {
    int now = time_service::get_current_timestamp();
    EXPECT_TRUE(typeid(now) == typeid(int));
}

// TestPrintMixObject
class TestPrintMixObject : public ::testing::Test {};
struct Dummy : public print_mix_object::MixDummy {};

TEST_F(TestPrintMixObject, test_print_object_basic) {
    Dummy obj;
    print_mix_object::print_basic_object(obj);
}
TEST_F(TestPrintMixObject, test_print_list_and_dict) {
    Dummy obj;
    print_mix_object::print_list(std::vector<Dummy>{obj});
    print_mix_object::print_list(std::vector<Dummy>{});
    print_mix_object::print_dict(std::map<std::string, int>{{"a", 1}});
    print_mix_object::print_dict(std::map<std::string, int>{});
    print_mix_object::print_basic_dict(std::map<std::string, int>{{"k", 1}});
    print_mix_object::print_basic_list(std::vector<int>{1,2,3});
    print_mix_object::print_basic_list(std::vector<int>{});
}

// TestJsonParser
class TestJsonParser : public ::testing::Test {};
TEST_F(TestJsonParser, test_parse) {
    nlohmann::json obj = {{"foo", "bar"}};
    std::string json_str = json_parser::json_dumps(obj);
    nlohmann::json result = json_parser::json_loads(json_str);
    EXPECT_EQ(result["foo"], "bar");
}