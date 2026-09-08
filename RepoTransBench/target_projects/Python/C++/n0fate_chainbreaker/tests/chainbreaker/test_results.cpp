// add at top:
#include <cstdlib>

// ... In WriteCollectionToFile test:
TEST(ResultsTest, WriteCollectionToFile) {
    std::map<std::string, std::string> coll;
    std::string content = "content";

    // Create a unique tmp directory for this test
    std::string dir_base = "/tmp/";
    std::string dirname = dir_base + "chainbreaker_test_" + std::to_string(rand());
    std::filesystem::create_directory(dirname);

    coll["header"] = "HHH";
    coll["write_directory"] = dirname;
    auto f = results::write_collection_to_file(coll, content);

    std::ifstream in(f);
    std::stringstream buffer;
    buffer << in.rdbuf();
    ASSERT_NE(buffer.str().find("content"), std::string::npos);

    std::filesystem::remove(f); // Cleanup
    std::filesystem::remove(dirname);
}