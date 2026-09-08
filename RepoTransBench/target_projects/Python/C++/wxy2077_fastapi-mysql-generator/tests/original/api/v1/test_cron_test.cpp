#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

// Mock scheduler API (since FastAPI endpoints don't exist in C++)
namespace {
struct JobEntry {
    int seconds;
    std::string job_id;
};

std::vector<JobEntry> job_list;
std::string last_deleted_job;

struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
    std::map<std::string, std::string> json_strings;
    std::map<std::string, std::map<std::string, std::string>> json_data;
    std::vector<JobEntry> jobs;
};

Response post_add_job(const std::string& job_id) {
    job_list.push_back({5, job_id});
    return Response{200, {{"code", 200}}, {{"id", job_id}}, {}, {}, };
}

Response get_all_jobs() {
    Response r;
    r.status_code = 200;
    r.json_numbers["code"] = 200;
    r.jobs = job_list;
    return r;
}

Response post_del_job(const std::string& job_id) {
    // Remove from job_list
    std::vector<JobEntry> new_list;
    for (auto& job : job_list) {
        if (job.job_id != job_id)
            new_list.push_back(job);
    }
    job_list.swap(new_list);
    last_deleted_job = job_id;
    return Response{200, {{"code", 200}}, {}, {}, {}, };
}

}

TEST(CronApiTest, AddJob) {
    std::string job_id = "job_123";
    auto response = post_add_job(job_id);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_EQ(response.json_strings["id"], job_id);
}

TEST(CronApiTest, GetAllJob) {
    // Add a job so list is not empty
    std::string job_id = "job_456";
    post_add_job(job_id);
    auto response = get_all_jobs();
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_TRUE(response.jobs.size() > 0);
}

TEST(CronApiTest, DelJob) {
    std::string job_id = "job_456";
    auto response = post_del_job(job_id);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}