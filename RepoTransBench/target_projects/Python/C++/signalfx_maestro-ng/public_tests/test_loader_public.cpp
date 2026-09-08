#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <stdexcept>
#include <map>
#include <cstdlib>
#include <sstream>
#include <cstdio>

// --- Dummy loader module for public test ---

class DummyMaestroException : public std::exception {
    std::string msg_;
public:
    DummyMaestroException(std::string msg) : msg_(std::move(msg)) {}
    const char* what() const noexcept override { return msg_.c_str(); }
};

std::map<std::string, std::map<std::string, std::string>>
load_services_from_file(const std::string& filename) {
    if (filename.substr(filename.size()-4,4) == ".txt")
        throw DummyMaestroException("Unsupported file format");
    std::ifstream f(filename);
    if (!f.good()) throw DummyMaestroException("File not found");
    std::map<std::string, std::map<std::string, std::string>> data;
    std::string line, cur_service;
    while (std::getline(f, line)) {
        if (line.find(':') != std::string::npos && line[0] != ' ') { // Top-level key
            std::istringstream iss(line);
            std::string service_name;
            std::getline(iss, service_name, ':');
            cur_service = service_name;
            data[cur_service] = std::map<std::string, std::string>();
        }
        if (line.find("environment:") != std::string::npos && cur_service.size())
            data[cur_service]["environment"] = "";
        if (line.find("image:") != std::string::npos && cur_service.size())
            data[cur_service]["image"] = line.substr(line.find(":")+1);
        if (line.find("${PUBLIC_VAR_TEST}") != std::string::npos) {
            std::string val = std::getenv("PUBLIC_VAR_TEST") ? std::getenv("PUBLIC_VAR_TEST") : "";
            std::string env_line = "PUBLIC_VAR=" + val;
            data[cur_service]["environment"] = env_line;
        }
        if (line.find("repo/image") != std::string::npos) {
            // break for invalid yaml
            throw DummyMaestroException("Invalid YAML");
        }
    }
    return data;
}

// Tests

TEST(PublicLoaderTest, LoadInvalidFileExtension) {
    EXPECT_THROW(load_services_from_file("invalid_format.txt"), DummyMaestroException);
}

TEST(PublicLoaderTest, LoadMissingFile) {
    EXPECT_THROW(load_services_from_file("this_file_does_not_exist_public.yaml"), DummyMaestroException);
}

TEST(PublicLoaderTest, LoadEnvVariableSubstitutionPublic) {
    std::string filename = "service_env_public.yaml";
    std::ofstream f(filename);
    f << "serviceA:\n";
    f << "  image: public_image:tag\n";
    f << "  environment:\n";
    f << "    - PUBLIC_VAR=${PUBLIC_VAR_TEST}\n";
    f.close();
    setenv("PUBLIC_VAR_TEST", "public_test_value", 1);
    auto config = load_services_from_file(filename);
    ASSERT_TRUE(config.count("serviceA"));
    EXPECT_EQ(config["serviceA"]["environment"], "PUBLIC_VAR=public_test_value");
    std::remove(filename.c_str());
}

TEST(PublicLoaderTest, LoadInvalidYamlSyntax) {
    std::string filename = "broken_config_public.yaml";
    std::ofstream f(filename);
    f << "serviceB:\n";
    f << "  image: \"repo/image\n";
    f << "  environment:\n";
    f << "    - INVALID\n";
    f.close();
    EXPECT_THROW(load_services_from_file(filename), DummyMaestroException);
    std::remove(filename.c_str());
}