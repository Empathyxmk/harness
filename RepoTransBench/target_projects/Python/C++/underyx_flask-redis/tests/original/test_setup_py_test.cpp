#include <gtest/gtest.h>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem>
#include <regex>

// A dummy implementation of `read` and `find_meta` similar to the Python test logic.
namespace setup_py_sim {
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

TEST(TestSetupPy, test_read_reads_file) {
    // Simulate the temp directory structure
    std::filesystem::path base = std::filesystem::temp_directory_path() / "pytest_flask_redis1";
    std::filesystem::create_directories(base / "flask_redis");
    std::string test_text = "abc";
    std::filesystem::path file_path = base / "flask_redis" / "dummy.py";
    {
        std::ofstream out(file_path);
        out << test_text;
    }

    // test the read function
    std::string result = setup_py_sim::read(base, {"flask_redis", "dummy.py"});
    EXPECT_EQ(result, test_text);

    // cleanup
    std::filesystem::remove_all(base);
}

TEST(TestSetupPy, test_find_meta_success) {
    std::string fake_code = "__title__ = 'foo'\n__description__ = 'bar'";
    EXPECT_EQ(setup_py_sim::find_meta(fake_code, "title"), "foo");
    EXPECT_EQ(setup_py_sim::find_meta(fake_code, "description"), "bar");
}

TEST(TestSetupPy, test_find_meta_failure) {
    std::string fake_code = "";
    EXPECT_THROW({
        setup_py_sim::find_meta(fake_code, "whatever");
    }, std::runtime_error);
}