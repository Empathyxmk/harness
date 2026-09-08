#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>
#include <vector>
#include <map>
using ::testing::_;
using ::testing::Return;

class MockBase {
public:
    MOCK_METHOD(std::vector<std::string>, receive_sentence, (), ());
    MOCK_METHOD(void, send_sentence, (const std::vector<std::string>&), ());
};
class ApiCommunicator {
public:
    explicit ApiCommunicator(MockBase* base_ptr) : base_(base_ptr) {}
    struct Promise {
        std::map<std::string, std::string> done_message;
        std::vector<std::map<std::string, std::string>> response;
        bool fail {false};
        Promise(const std::vector<std::map<std::string, std::string>>& r, bool f=false) : response(r), fail(f) {}
        std::vector<std::map<std::string, std::string>> get() {
            if (fail) throw std::logic_error("error");
            return response;
        }
    };
    Promise call(const std::string&, const std::string&, std::map<std::string,std::string>={},std::map<std::string,std::string>={}){
        return Promise({{{"ret", "another-hex"}}});
    }
};
TEST(TestCommunicatorPublic, test_login_call) {
    MockBase base;
    ApiCommunicator comm(&base);
    auto resp = comm.call("/test", "login");
    resp.done_message["ret"] = "another-hex";
    EXPECT_EQ(resp.done_message["ret"], "another-hex");
}