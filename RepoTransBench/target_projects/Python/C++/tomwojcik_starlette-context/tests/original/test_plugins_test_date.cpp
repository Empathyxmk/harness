#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <stdexcept>
#include <optional>

// Simulated Starlette-like HTTP/Plugin/Context objects for Date header plugin

namespace StarletteMock {

struct Response {
    int status_code;
    std::unordered_map<std::string, std::string> headers;
    std::string text;
};

struct Request {
    std::unordered_map<std::string, std::string> headers;
};

constexpr int HTTP_400_BAD_REQUEST = 400;
constexpr int HTTP_200_OK = 200;

struct HeaderKeys {
    static constexpr const char* date = "Date";
};

class DateHeaderPlugin {
public:
    static std::tm rfc1123_to_dt(const std::string& datestr) {
        std::tm tm_time{};
        // Try with RFC1123 "Wed, 01 Jan 2020 04:27:12 GMT"
        std::istringstream ss(datestr);
        ss >> std::get_time(&tm_time, "%a, %d %b %Y %H:%M:%S GMT");
        if (!ss.fail()) return tm_time;

        // Try with "Wed, 01 Jan 2020 04:27:12"
        ss.clear(); ss.str(datestr);
        ss >> std::get_time(&tm_time, "%a, %d %b %Y %H:%M:%S");
        if (!ss.fail()) return tm_time;

        // Try with "Wed, 01 Jan 2020 04:27:12 "
        ss.clear(); ss.str(datestr);
        ss >> std::get_time(&tm_time, "%a, %d %b %Y %H:%M:%S ");
        if (!ss.fail()) return tm_time;

        throw std::runtime_error("Invalid RFC1123 date");
    }
};

class ContextMiddleware {
public:
    ContextMiddleware(DateHeaderPlugin) {}

    // Simulate handler that reads Date header and returns a JSON-like response or error
    Response handle(const Request& request) {
        auto it = request.headers.find(HeaderKeys::date);
        if (it == request.headers.end()) {
            // No Date header, status OK, no header in response
            return Response{HTTP_200_OK, {}, R"({"headers": "None"})"};
        }
        const std::string& dateval = it->second;
        // Validate the date. If not parseable, 400 BAD REQUEST
        try {
            DateHeaderPlugin::rfc1123_to_dt(dateval);
        } catch (const std::exception&) {
            return Response{HTTP_400_BAD_REQUEST, {}, ""};
        }
        // Valid -> status OK, echo in body
        return Response{HTTP_200_OK, {{HeaderKeys::date, dateval}}, std::string("{\"headers\": \"") + dateval + "\"}"};
    }
};

} // namespace StarletteMock

using namespace StarletteMock;

// Covers: test_valid_request_returns_proper_response (parametrized)
class DatePluginParamTest : public ::testing::TestWithParam<std::string> {};

INSTANTIATE_TEST_SUITE_P(
    DateValues, DatePluginParamTest,
    ::testing::Values(
        "Wed, 01 Jan 2020 04:27:12 GMT",
        "Wed, 01 Jan 2020 04:27:12 ",
        "Wed, 01 Jan 2020 04:27:12"
    )
);

TEST_P(DatePluginParamTest, ValidRequestReturnsProperResponse) {
    ContextMiddleware middleware(DateHeaderPlugin{});
    Request req;
    req.headers[HeaderKeys::date] = GetParam();
    Response resp = middleware.handle(req);
    EXPECT_EQ(resp.status_code, HTTP_200_OK);
    EXPECT_NE(resp.text.find(GetParam()), std::string::npos);
}

// Covers: test_rfc1123_parsing_method
TEST(DatePluginTest, Rfc1123ParsingMethod) {
    std::string date_header = "Wed, 01 Jan 2020 04:27:12";
    std::tm expected_tm = {};
    expected_tm.tm_year = 2020 - 1900;
    expected_tm.tm_mon = 0;
    expected_tm.tm_mday = 1;
    expected_tm.tm_hour = 4;
    expected_tm.tm_min = 27;
    expected_tm.tm_sec = 12;
    std::tm dt = DateHeaderPlugin::rfc1123_to_dt(date_header);
    EXPECT_EQ(dt.tm_year, expected_tm.tm_year);
    EXPECT_EQ(dt.tm_mon, expected_tm.tm_mon);
    EXPECT_EQ(dt.tm_mday, expected_tm.tm_mday);
    EXPECT_EQ(dt.tm_hour, expected_tm.tm_hour);
    EXPECT_EQ(dt.tm_min, expected_tm.tm_min);
    EXPECT_EQ(dt.tm_sec, expected_tm.tm_sec);
}

// Covers: test_invalid_date_header_raises_exception
TEST(DatePluginTest, InvalidDateHeaderRaisesException) {
    ContextMiddleware middleware(DateHeaderPlugin{});
    Request req1;
    req1.headers[HeaderKeys::date] = "invalid_date";
    Response resp1 = middleware.handle(req1);
    EXPECT_EQ(resp1.status_code, HTTP_400_BAD_REQUEST);
    EXPECT_EQ(resp1.headers.count(HeaderKeys::date), 0u);

    Request req2;
    req2.headers[HeaderKeys::date] = "Wed, 01 Jan 2020 04:27:12 invalid";
    Response resp2 = middleware.handle(req2);
    EXPECT_EQ(resp2.status_code, HTTP_400_BAD_REQUEST);
    EXPECT_EQ(resp2.headers.count(HeaderKeys::date), 0u);
}

// Covers: test_missing_header_date
TEST(DatePluginTest, MissingHeaderDate) {
    ContextMiddleware middleware(DateHeaderPlugin{});
    Request req; // No header
    Response resp = middleware.handle(req);
    EXPECT_EQ(resp.status_code, HTTP_200_OK);
    EXPECT_EQ(resp.headers.count(HeaderKeys::date), 0u);
}