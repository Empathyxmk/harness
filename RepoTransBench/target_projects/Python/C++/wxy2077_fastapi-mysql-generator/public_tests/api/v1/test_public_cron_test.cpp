#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

// Same structure as private, but with public_job_id and different arguments
namespace {
struct JobEntry {
    int seconds;
    std::string job_id;
};
std::vector<JobEntry> public_job_list;
struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
    std::map<std::string, std::string> json_strings;
    std::vector<JobEntry> jobs;
};

Response post_add_job_public(const std::string& job_id) {
    public_job_list.push_back({8, job_id});
    return Response{200, {{"code", 200}}, {{"id", job_id}}, {}, };
}

Response get_all_jobs_public() {
    Response r;
    r.status_code = 200;
    r.json_numbers["code"] = 200;
    r.jobs = public_job_list;
    return r;
}

Response post_del_job_public(const std::string& job_id) {
    std::vector<JobEntry> new_list;
    for (auto& job : public_job_list) {
        if (job.job_id != job_id)
            new_list.push_back(job);
    }
    public_job_list.swap(new_list);
    return Response{200, {{"code", 200}}, {}, {}, };
}
}

TEST(PublicCronApiTest, AddJobPublic) {
    std::string public_job_id = "public_job_786";
    auto response = post_add_job_public(public_job_id);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_EQ(response.json_strings["id"], public_job_id);
}
TEST(PublicCronApiTest, GetAllJobPublic) {
    std::string public_job_id = "public_job_786";
    post_add_job_public(public_job_id);
    auto response = get_all_jobs_public();
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_TRUE(response.jobs.size() > 0);
}
TEST(PublicCronApiTest, DelJobPublic) {
    std::string public_job_id = "public_job_786";
    auto response = post_del_job_public(public_job_id);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}