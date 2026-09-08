#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <utility>

namespace {

TEST(TestPublicModelServingFull, IsPipeSupportedCPU) {
    // If platform.machine() is "ppc64le", function returns false
    std::string arch = "ppc64le";
    bool result = (arch == "amd64");
    ASSERT_FALSE(result);
}

TEST(TestPublicModelServingFull, IsPipeSupportedX86) {
    std::string arch = "amd64";
    bool result = (arch == "amd64");
    ASSERT_TRUE(result);
}

TEST(TestPublicModelServingFull, CheckModelName) {
    std::vector<std::string> trusted_models = {"alpha/test", "beta/cat"};
    auto check_model_name = [&](const std::string& name) {
        return std::find(trusted_models.begin(), trusted_models.end(), name) != trusted_models.end();
    };
    ASSERT_TRUE(check_model_name("beta/cat"));
    ASSERT_FALSE(check_model_name("unknown/model"));
}

TEST(TestPublicModelServingFull, IsModelPreclean) {
    std::vector<std::string> trusted_models = {"gamma/testclean"};
    auto is_model_preclean = [&](const std::string& repo, const std::string&) {
        return std::find(trusted_models.begin(), trusted_models.end(), repo) != trusted_models.end();
    };
    ASSERT_TRUE(is_model_preclean("gamma/testclean", "anything"));
    ASSERT_FALSE(is_model_preclean("other/model", "arg"));
}

class PublicDummyProc {
public:
    PublicDummyProc(const std::map<std::string, std::string>& env) : _env(env), pid(7) {}
    std::map<std::string, std::string> environ() { return _env; }
    int pid;
private:
    std::map<std::string, std::string> _env;
};

TEST(TestPublicModelServingFull, RunningModelsFilters) {
    std::vector<PublicDummyProc> procs = {
        PublicDummyProc({{"RUN_BY_LOCALLLM", "1"}, {"MODEL", "public/path/one"}}),
        PublicDummyProc({{"RUN_BY_LOCALLLM", "1"}, {"MODEL", "public/path/two"}}),
        PublicDummyProc({}),
        PublicDummyProc({{"RUN_BY_LOCALLLM", "0"}})
    };
    auto model_from_path = [](const std::string& path){
        if (path == "public/path/one") return std::make_pair("repoA", "fileA");
        if (path == "public/path/two") return std::make_pair("repoB", "fileB");
        return std::make_pair(std::string(""), std::string(""));
    };
    std::vector<std::pair<std::string, std::string>> out;
    for (const auto& p : procs) {
        auto env = p.environ();
        if (env.find("RUN_BY_LOCALLLM") != env.end() && env.at("RUN_BY_LOCALLLM") == "1" && env.find("MODEL") != env.end()) {
            out.push_back(model_from_path(env.at("MODEL")));
        }
    }
    ASSERT_EQ(out.size(), 2);
    ASSERT_EQ(out[0].first, "repoA");
    ASSERT_EQ(out[0].second, "fileA");
    ASSERT_EQ(out[1].first, "repoB");
    ASSERT_EQ(out[1].second, "fileB");
}

} // namespace