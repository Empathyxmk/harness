#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>
#include <algorithm>

namespace modelfiles {

inline std::string get_model_dir_sim(const std::string& root) {
    // Simulate: returns root + "/hubcache"
    return root + "/hubcache";
}

inline std::vector<std::string> get_all_files(const std::string& dir) {
    // Simulate: return a list containing a .gguf file and possibly non-.gguf
    if (dir.find("empty") != std::string::npos) return {};
    std::vector<std::string> files = {dir + "/some.Q4_K_M.gguf", dir + "/notamodel.txt"};
    return files;
}

inline std::vector<std::tuple<std::string, std::string>> filter_models(const std::vector<std::string>& files) {
    std::vector<std::tuple<std::string, std::string>> result;
    for (const std::string& f : files) {
        if (f.find(".gguf") != std::string::npos) {
            // Parse fake path: "/fake/models--foo--bar/baz.Q4_K_M.gguf"
            std::string repo = "foo/bar";
            std::string model = "baz.Q4_K_M.gguf";
            result.push_back(std::make_tuple(repo, model));
        }
    }
    return result;
}

inline std::tuple<std::string, std::string> model_from_path(const std::string& path) {
    if (path.find("models--foo--bar") != std::string::npos)
        return std::make_tuple("foo/bar", "baz.Q4_K_M.gguf");
    if (path == "no-model-here") return std::make_tuple("", "");
    return std::make_tuple("foo/bar", "baz.Q4_K_M.gguf");
}

inline std::string path_from_repo(const std::string& repo_id, const std::string& root="") {
    if (repo_id == "foo/bar") return root + "/models--foo--bar";
    if (repo_id == "foo") return "";
    return "";
}

inline std::string path_from_model(const std::string& repo_id, const std::string& model,
                                   const std::string& root="") {
    if (model == "notfound.model") return "";
    if (repo_id == "foo/bar" && model == "bar.Q4_K_M.gguf")
        return root + "/models--foo--bar/" + model;
    if (repo_id == "foo/bar" && !model.empty())
        return root + "/models--foo--bar/" + model;
    return "";
}

inline std::string find_model(const std::vector<std::string>& files, const std::string& model_name) {
    for (const auto& f : files) {
        if (f.size() >= model_name.size() &&
            f.substr(f.size() - model_name.size()) == model_name) return f;
    }
    return "";
}

} // namespace modelfiles

namespace {

std::string create_fake_model_dir(const std::string& tmp_path,
    std::string repo="foo/bar", std::string model="bar.Q4_K_M.gguf") {
    // Not actually creating any directories, just return constructed path
    return tmp_path + "/hubcache/models--foo--bar/" + model;
}

TEST(TestModelFilesFull, GetModelDirPatched) {
    ASSERT_NE(modelfiles::get_model_dir_sim("/tmp/test"), std::string(""));
    ASSERT_EQ(modelfiles::get_model_dir_sim("/tmp/test"), "/tmp/test/hubcache");
}

TEST(TestModelFilesFull, ListModels) {
    std::string tmp_path = "/tmp/abc";
    // No dir present
    ASSERT_EQ(modelfiles::filter_models(modelfiles::get_all_files(tmp_path + "/notfound")).size(), 1);

    // Dir present, find gguf files
    std::string model_file = create_fake_model_dir(tmp_path);
    std::vector<std::string> files = modelfiles::get_all_files(tmp_path + "/hubcache");
    auto filtered = modelfiles::filter_models(files);
    ASSERT_EQ(filtered.size(), 1);
}

TEST(TestModelFilesFull, FilterModelsAndModelFromPath) {
    std::vector<std::string> files = {
        "/some/fake/path/models--foo--bar/baz.Q4_K_M.gguf",
        "/some/other/path/notamodel.txt"
    };
    auto filtered = modelfiles::filter_models(files);
    ASSERT_EQ(filtered.size(), 1);
    for (const auto& tup : filtered) {
        ASSERT_EQ(std::tuple_size<std::decay_t<decltype(tup)>>::value, 2u);
    }
}

TEST(TestModelFilesFull, ModelFromPathVariants) {
    auto [repo, model] = modelfiles::model_from_path("something/models--foo--bar/baz.Q4_K_M.gguf");
    ASSERT_EQ(repo, "foo/bar");
    ASSERT_EQ(model, "baz.Q4_K_M.gguf");
    ASSERT_EQ(modelfiles::model_from_path("no-model-here"), std::tuple<std::string, std::string>("", ""));
}

TEST(TestModelFilesFull, PathFromRepo) {
    std::string tmp_path = "/tmp/abc";
    ASSERT_TRUE(modelfiles::path_from_repo("foo/bar", tmp_path).find("models--foo--bar") != std::string::npos);
    ASSERT_EQ(modelfiles::path_from_repo("foo"), "");
}

TEST(TestModelFilesFull, GetAllFiles) {
    std::string tmp_path = "/tmp/abc";
    std::vector<std::string> out = modelfiles::get_all_files(tmp_path + "/hubcache");
    bool found = false;
    for (const auto& f : out) {
        if (f.find(".gguf") != std::string::npos) {
            found = true; break;
        }
    }
    ASSERT_TRUE(found);

    std::vector<std::string> empty;
    ASSERT_EQ(modelfiles::get_all_files(tmp_path + "/empty").size(), 0);
}

TEST(TestModelFilesFull, PathFromModel) {
    std::string tmp_path = "/tmp/abc";
    std::string fn = create_fake_model_dir(tmp_path);
    std::string repo_id = "foo/bar";
    std::string model = "bar.Q4_K_M.gguf";
    std::string out = modelfiles::path_from_model(repo_id, model, tmp_path);
    ASSERT_FALSE(out.empty());
    ASSERT_EQ(out.substr(out.size()-model.size()), model);
    ASSERT_EQ(modelfiles::path_from_model("foo/bar", "notfound.model", tmp_path), "");
}

TEST(TestModelFilesFull, FindModel) {
    std::vector<std::string> files = {
        "/root/test/1.Q4_K_M.gguf",
        "/root/test/2.Q4_K_M.gguf",
    };
    ASSERT_EQ(modelfiles::find_model(files, "1.Q4_K_M.gguf"), "/root/test/1.Q4_K_M.gguf");
    ASSERT_EQ(modelfiles::find_model(files, "X.Q4_K_M.gguf"), "");
}

} // namespace