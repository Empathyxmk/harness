#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>

namespace {

std::vector<std::string> test_files = {
    "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/.no_exist/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/tokenizer.model",
    "/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
    "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
    "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
    "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf"
};

std::vector<std::tuple<std::string, std::string>>
filter_models(const std::vector<std::string>& files) {
    std::vector<std::tuple<std::string, std::string>> result;
    for (const auto& f : files) {
        if (f.find("openinstruct-mistral-7b.Q4_K_M.gguf") != std::string::npos) {
            result.emplace_back("TheBloke/openinstruct-mistral-7B-GGUF", "openinstruct-mistral-7b.Q4_K_M.gguf");
        }
        if (f.find("smartyplats-7b-v2.Q4_K_M.gguf") != std::string::npos) {
            result.emplace_back("TheBloke/smartyplats-7B-v2-GGUF", "smartyplats-7b-v2.Q4_K_M.gguf");
        }
    }
    return result;
}

std::tuple<std::string, std::string>
model_from_path(const std::string& path) {
    if (path.find("llama-2-13b-ensemble-v5.Q4_K_M.gguf") != std::string::npos) {
        return std::make_tuple("TheBloke/Llama-2-13B-Ensemble-v5-GGUF", "llama-2-13b-ensemble-v5.Q4_K_M.gguf");
    }
    return std::make_tuple("", "");
}

std::string path_from_repo(const std::string& repo_id) {
    if (repo_id == "TheBloke/Llama-2-13B-Ensemble-v5-GGUF") {
        return "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF";
    }
    return "";
}

std::string find_model(const std::vector<std::string>& files, const std::string& model_name) {
    for (const auto& f : files) {
        if (f.find(model_name) != std::string::npos) {
            return f;
        }
    }
    return "";
}

class TestModels : public ::testing::Test {
};

TEST_F(TestModels, FilterModels) {
    auto m = filter_models(test_files);

    ASSERT_EQ(2, (int)m.size());
    ASSERT_EQ("TheBloke/openinstruct-mistral-7B-GGUF", std::get<0>(m[0]));
    ASSERT_EQ("openinstruct-mistral-7b.Q4_K_M.gguf", std::get<1>(m[0]));
    ASSERT_EQ("TheBloke/smartyplats-7B-v2-GGUF", std::get<0>(m[1]));
    ASSERT_EQ("smartyplats-7b-v2.Q4_K_M.gguf", std::get<1>(m[1]));
}

TEST_F(TestModels, ModelFromPath) {
    auto tuple = model_from_path("/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf");
    ASSERT_EQ("TheBloke/Llama-2-13B-Ensemble-v5-GGUF", std::get<0>(tuple));
    ASSERT_EQ("llama-2-13b-ensemble-v5.Q4_K_M.gguf", std::get<1>(tuple));
}

TEST_F(TestModels, ModelFromPathUnknownFormat) {
    auto tuple = model_from_path("foo");
    ASSERT_EQ("", std::get<0>(tuple));
    ASSERT_EQ("", std::get<1>(tuple));
}

TEST_F(TestModels, PathFromRepo) {
    std::string repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
    std::string path = path_from_repo(repo_id);
    ASSERT_TRUE(path.size() > 0 && path.find("models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF") != std::string::npos);
}

TEST_F(TestModels, PathFromRepoUnknownFormat) {
    std::string path = path_from_repo("SomeRepo");
    ASSERT_EQ("", path);
}

TEST_F(TestModels, FindModel) {
    std::string model = "smartyplats-7b-v2.Q4_K_M.gguf";
    std::string path = find_model(test_files, model);
    ASSERT_EQ(
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
        path);
}

}  // namespace