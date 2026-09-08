#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <ctime>

// Model Stubs

struct Post {
    int id;
    std::string title;
    bool is_visible;
    Post(int id_, std::string title_, bool vis) : id(id_), title(title_), is_visible(vis) {}
    static std::vector<Post> visible(std::vector<Post>& all_posts) {
        std::vector<Post> vis;
        for (auto& p : all_posts)
            if (p.is_visible) vis.push_back(p);
        return vis;
    }
};

struct Issue {
    int id;
    std::string title;
    int issue_number;
    bool is_draft;
    std::time_t publish_date;
    Issue(int id_, std::string title_, int num, bool draft, std::time_t pdate)
        : id(id_), title(title_), issue_number(num), is_draft(draft), publish_date(pdate) {}
    bool is_published() const { return !is_draft && std::time(nullptr) > publish_date; }
    std::string get_absolute_url() const { return "/newsfeed/issues/" + std::to_string(issue_number) + "/"; }
};

struct Subscriber {
    std::string email_address;
    bool subscribed;
    bool verified;
    std::string token;
    std::time_t verification_sent_date;
    Subscriber(std::string email, bool sub, bool ver)
        : email_address(email), subscribed(sub), verified(ver), token("tok"), verification_sent_date(std::time(nullptr)) {}
    std::string str() const { return email_address; }
    bool token_expired() const {
        // token expires in 2 days
        if (verification_sent_date == 0) return true;
        std::time_t now = std::time(nullptr);
        return difftime(now, verification_sent_date) > 172800;
    }
    void reset_token() { token = "newtok"; }
    bool subscribe() { if (!token_expired()) { verified = subscribed = true; return true; } return false; }
    bool unsubscribe() { if (verified && subscribed) { verified = subscribed = false; return true; } return false; }
    std::string get_verification_url() const { return "/newsfeed/subscribe/confirm/" + token + "/"; }
};

struct Newsletter {
    std::string subject;
    Newsletter(std::string s) : subject(s) {}
};

struct PostCategory {
    std::string name;
    PostCategory(std::string n) : name(n) {}
};

TEST(PostModelTest, str) {
    Post p(1, "Article Title", true);
    ASSERT_EQ(p.title, "Article Title");
}

TEST(PostModelTest, visible_queryset) {
    std::vector<Post> posts = {
        Post(1, "Visible 1", true),
        Post(2, "Visible 2", true),
        Post(3, "Invisible 1", false),
        Post(4, "Invisible 2", false)
    };
    auto vis = Post::visible(posts);
    ASSERT_EQ(vis.size(), 2);
}

TEST(PostModelTest, all_queryset) {
    std::vector<Post> posts = {
        Post(1, "Post1", true),
        Post(2, "Post2", true),
        Post(3, "Post3", false),
        Post(4, "Post4", false)
    };
    ASSERT_EQ(posts.size(), 4);
}

TEST(IssueModelTest, str) {
    Issue issue(1, "Issue Title", 101, false, std::time(nullptr) - 86400);
    ASSERT_EQ(issue.title, "Issue Title");
}

TEST(IssueModelTest, all_queryset_and_released) {
    Issue released(1, "R", 10, false, std::time(nullptr) - 86400);
    Issue unreleased(2, "U", 11, true, std::time(nullptr));
    std::vector<Issue> vec{released, unreleased};
    ASSERT_EQ(vec.size(), 2);
    int released_count = 0;
    for (const auto& iss : vec) if (iss.is_published()) ++released_count;
    ASSERT_EQ(released_count, 1);
}

TEST(IssueModelTest, released_with_future_release_date) {
    Issue future(3, "Future", 12, false, std::time(nullptr) + 86400*2);
    ASSERT_FALSE(future.is_published());
}

TEST(IssueModelTest, is_published) {
    Issue rel(1, "Y", 1, false, std::time(nullptr) - 86400);
    Issue unrel(2, "N", 2, true, std::time(nullptr));
    ASSERT_TRUE(rel.is_published());
    ASSERT_FALSE(unrel.is_published());
}

TEST(IssueModelTest, get_absolute_url) {
    Issue iss(1, "WillLink", 42, false, std::time(nullptr) - 3600);
    ASSERT_EQ(iss.get_absolute_url(), "/newsfeed/issues/42/");
}

TEST(SubscriberModelTest, str) {
    Subscriber s("aaa@a.com", true, true);
    ASSERT_EQ(s.str(), "aaa@a.com");
}

TEST(SubscriberModelTest, token_expired_and_reset) {
    Subscriber s("b@b.com", false, false);
    s.verification_sent_date = std::time(nullptr) - 86400*3; // three days ago
    ASSERT_TRUE(s.token_expired());
    s.verification_sent_date = std::time(nullptr); // now
    ASSERT_FALSE(s.token_expired());
    s.verification_sent_date = 0;
    ASSERT_TRUE(s.token_expired());
    std::string oldtok = s.token;
    s.reset_token();
    ASSERT_NE(s.token, oldtok);
}

TEST(SubscriberModelTest, subscribe_and_unsubscribe_behavior) {
    Subscriber s("x@a.com", false, false);
    s.verification_sent_date = std::time(nullptr);
    ASSERT_TRUE(s.subscribe());
    ASSERT_TRUE(s.verified);
    ASSERT_TRUE(s.subscribed);
    // Unsubscribe and recheck
    ASSERT_TRUE(s.unsubscribe());
    ASSERT_FALSE(s.verified);
    ASSERT_FALSE(s.subscribed);
}

TEST(SubscriberModelTest, subscribe_fail_expired_token) {
    Subscriber s("fail@expired.com", false, false);
    s.verification_sent_date = std::time(nullptr) - 86400*3;
    ASSERT_FALSE(s.subscribe());
    ASSERT_FALSE(s.verified);
    ASSERT_FALSE(s.subscribed);
}

TEST(SubscriberModelTest, unsubscribe_fail_unsubscribed) {
    Subscriber s("notfound@a.com", false, false);
    ASSERT_FALSE(s.unsubscribe());
}

TEST(SubscriberModelTest, get_verification_url) {
    Subscriber s("z@z.com", false, false);
    s.token = "ttt123";
    ASSERT_EQ(s.get_verification_url(), "/newsfeed/subscribe/confirm/ttt123/");
}

TEST(NewsletterModelTest, str) {
    Newsletter n("Latest Subject");
    ASSERT_EQ(n.subject, "Latest Subject");
}

TEST(PostCategoryModelTest, str) {
    PostCategory pc("Tech");
    ASSERT_EQ(pc.name, "Tech");
}