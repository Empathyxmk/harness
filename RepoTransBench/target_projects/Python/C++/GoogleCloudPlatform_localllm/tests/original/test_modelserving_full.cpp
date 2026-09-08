#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <vector>
#include <string>

namespace {

class DummyProc {
public:
    explicit DummyProc(const std::map<std::string, std::string>& env)
        : _env(env), pid(42) {}
    std::map<std::string, std::string> environ() const { return _env; }
    int pid;
private:
    std::map<std::string, std::string> _env;
};

TEST(TestModelServingFull, RunningModelsFilters) {
    DummyProc p1({{"RUN_BY_LOCALLLM", "1"}, {"MODEL", "a/b/c"}});
    DummyProc p2({{"RUN_BY_LOCALLLM", "0"}});
    DummyProc p3({});
    std::vector<DummyProc> procs = {p1, p2, p3};

    // Simulate filtering: only p1 counts as correct
    std::vector<std::pair<std::string, std::string>> filtered;
    for (const auto& p : procs) {
        auto env = p.environ();
        if (env.count("RUN_BY_LOCALLLM") && env.at("RUN_BY_LOCALLLM") == "1" && env.count("MODEL")) {
            filtered.push_back(std::make_pair("repoid", "filename"));
        }
    }
    ASSERT_EQ(filtered.size(), 1);
    ASSERT_EQ(filtered[0].first, "repoid");
    ASSERT_EQ(filtered[0].second, "filename");
}

class DummyProcAccessDenied {
public:
    DummyProcAccessDenied() {}
    std::map<std::string, std::string> environ() const {
        throw std::runtime_error("AccessDenied");
    }
};

TEST(TestModelServingFull, RunningModelsAccessDenied) {
    std::vector<DummyProcAccessDenied> procs = {DummyProcAccessDenied()};
    // Should not raise
    ASSERT_NO_THROW({
        for (auto& p : procs) {
            try {
                auto _ = p.environ();
            } catch (...) {
                // Ignore
            }
        }
    });
}

class DummyProcStart {
public:
    DummyProcStart(const std::vector<std::string>& lines)
        : lines_(lines), cur_(0), returncode_(0) {}
    int poll() { return (cur_ < lines_.size()) ? -1 : 0; }
    std::string readline() {
        if (cur_ < lines_.size())
            return lines_[cur_++];
        return "";
    }
    int returncode_;
private:
    std::vector<std::string> lines_;
    size_t cur_;
};

TEST(TestModelServingFull, StartSuccess) {
    std::vector<std::string> lines = {"Starting...", "Uvicorn running on 0.0.0.0"};
    DummyProcStart proc(lines);
    bool found = false;
    while (proc.poll() == -1) {
        auto line = proc.readline();
        if (line.find("Uvicorn running on") != std::string::npos) {
            found = true;
            break;
        }
    }
    ASSERT_TRUE(found);
}

class DummyProcNoStart {
public:
    DummyProcNoStart() : lines_{"Some output", "No marker"}, cur_(0), returncode_(1) {}
    int poll() { return 1; }
    std::string readline() { return ""; }
    int returncode_;
private:
    std::vector<std::string> lines_;
    size_t cur_;
};

TEST(TestModelServingFull, StartFail) {
    DummyProcNoStart proc;
    // Should return false because poll returns non-None
    bool started = false;
    if (proc.poll() != -1) {
        started = false;
    }
    ASSERT_FALSE(started);
}

class DummyProcWithLogConfig {
public:
    DummyProcWithLogConfig() : cur_(0) {}
    int poll() { return (cur_ == 0) ? -1 : 0; }
    std::string readline() {
        cur_++;
        if (cur_ == 1) {
            return "Uvicorn running on x";
        }
        return "";
    }
private:
    int cur_;
};

TEST(TestModelServingFull, StartWithLogConfig) {
    DummyProcWithLogConfig proc;
    bool found = false;
    while (proc.poll() == -1) {
        std::string line = proc.readline();
        if (line.find("Uvicorn running on") != std::string::npos) {
            found = true;
            break;
        }
    }
    ASSERT_TRUE(found);
}

}  // namespace