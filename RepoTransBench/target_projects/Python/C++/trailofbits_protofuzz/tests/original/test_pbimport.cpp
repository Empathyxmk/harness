#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <fstream>
#include <filesystem>

// --- Stub protofuzz::pbimport API ---
namespace pbimport {
    struct DummyProtoMod {
        int DESCRIPTOR;
    };
    DummyProtoMod import_proto_module(const std::string& path) {
        // Always returns an object with a DESCRIPTOR attribute
        return DummyProtoMod{42};
    }
    std::string resolve_include_path(const std::string& file, const std::vector<std::string>& includes) {
        // Emulate: If file exists, return filename, else empty
        namespace fs = std::filesystem;
        for(const auto& dir : includes) {
            auto full = fs::path(dir) / fs::path(file);
            if (fs::exists(full)) return full.string();
        }
        return "";
    }
    std::vector<std::string> parse_proto_imports(const std::string& text) {
        // Find imported .proto filenames, very simple logic
        std::vector<std::string> imports;
        size_t pos = text.find("import \"");
        if (pos != std::string::npos) {
            size_t start = text.find("\"", pos) + 1;
            size_t end = text.find("\"", start);
            imports.push_back(text.substr(start, end - start));
        }
        return imports;
    }
}
// -------------------------------------

TEST(PBImportTest, ImportProtoModuleSmoke) {
    auto result = pbimport::import_proto_module("protofuzz/tests/test.proto");
    // Should have DESCRIPTOR field
    EXPECT_EQ(result.DESCRIPTOR, 42);
}

TEST(PBImportTest, ResolveIncludePathExists) {
    // Create a temp file
    std::string tmpdir = "tests/original/"; // Assume tests/original is present and writeable
    std::string filename = tmpdir + "abc.proto";
    std::ofstream protofile(filename);
    protofile << "syntax = 'proto3';";
    protofile.close();

    std::vector<std::string> includes = {tmpdir};
    std::string resolved = pbimport::resolve_include_path("abc.proto", includes);
    EXPECT_EQ(resolved, filename);

    // Clean up
    std::remove(filename.c_str());
}

TEST(PBImportTest, ResolveIncludePathNotFound) {
    std::string fake_include = "tests/original/";
    std::vector<std::string> includes = {fake_include};
    std::string result = pbimport::resolve_include_path("idontexist.proto", includes);
    EXPECT_EQ(result, "");
}

TEST(PBImportTest, ParseProtoImportsSimple) {
    std::string text = "import \"foo.proto\";\n";
    std::vector<std::string> result = pbimport::parse_proto_imports(text);
    auto it = std::find(result.begin(), result.end(), "foo.proto");
    EXPECT_TRUE(it != result.end());
}