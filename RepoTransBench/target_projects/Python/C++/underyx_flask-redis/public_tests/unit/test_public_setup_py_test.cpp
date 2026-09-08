#include <gtest/gtest.h>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem>
#include <regex>

namespace setup_py_sim_pub {
    std::string read(const std::filesystem::path &base, const std::vector<std::string> &paths) {
        std::filesystem::path p = base;
        for(const auto& seg : paths){
            p /= seg;
        }
        std::ifstream in(p, std::ios::in);
        std::stringstream buffer;
        buffer << in.rdbuf();
        return buffer.str();
    }

    std::string find_meta(const std::string& input, const std::string& meta) {
        std::regex r("__" + meta + R"__(\s*=\s*['"]([^'"]*)['"])__");
        std::smatch m;
        if (std::regex_search(input, m, r))
            return m[1].str();
        throw std::runtime_error("Unable to find __" + meta + "__ string.");
    }
}

TEST(TestPublicSetupPy, test_read_reads_file_public) {
    std::filesystem::path base = std::filesystem::temp_directory_path() / "pytest_flask_redis2";
    std::filesystem::create_directories(base / "flask_redis");
    std::string test_text = "123xyz";
    std::filesystem::path file_path = base / "flask_redis" / "testfile_public.txt";
    {
        std::ofstream out(file_path);
        out << test_text;
    }

    std::string result = setup_py_sim_pub::read(base, {"flask_redis", "testfile_public.txt"});
    EXPECT_EQ(result, test_text);

    std::filesystem::remove_all(base);
}

TEST(TestPublicSetupPy, test_find_meta_success_public) {
    std::string fake_code = "__spam__ = 'eggs'\n__hamp__ = 'bacon'";
    EXPECT_EQ(setup_py_sim_pub::find_meta(fake_code, "spam"), "eggs");
    EXPECT_EQ(setup_py_sim_pub::find_meta(fake_code, "hamp"), "bacon");
}

TEST(TestPublicSetupPy, test_find_meta_failure_public) {
    std::string fake_code = "";
    EXPECT_THROW({
        setup_py_sim_pub::find_meta(fake_code, "somethingelse");
    }, std::runtime_error);
}