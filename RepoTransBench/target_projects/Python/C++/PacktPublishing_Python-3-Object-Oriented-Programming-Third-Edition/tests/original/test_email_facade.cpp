#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>
#include <type_traits>

// Minimal stubs to replicate test patterns

struct DummySMTP {
    std::string host;
    bool sent;
    std::tuple<std::string, std::vector<std::string>, std::string> last_args;
    std::tuple<std::string, std::string> logged_in;

    DummySMTP(std::string h) : host(h), sent(false), last_args(), logged_in() {}

    void login(const std::string& user, const std::string& pw) {
        logged_in = {user, pw};
    }
    void sendmail(const std::string& from_email, const std::vector<std::string>& to_list, const std::string& msg) {
        sent = true;
        last_args = {from_email, to_list, msg};
    }
};

struct DummyIMAP4 {
    std::string host;
    std::tuple<std::string, std::string> logged;
    bool selected;
    DummyIMAP4(std::string h) : host(h), logged(), selected(false) {}
    void login(const std::string& user, const std::string& pw) { logged = {user,pw}; }
    void select() { selected = true; }
    std::pair<std::string, std::vector<std::string>> search() { return {"OK", {"1 2"}}; }
    std::pair<std::string, std::vector<std::pair<std::string, std::string>>> fetch(const std::string& num, const std::string&) {
        return {"OK", {{"", "Message"+num}}};
    }
};

struct EmailFacade {
    std::string host, user, pw;
    DummySMTP* smtp_override = nullptr;
    DummyIMAP4* imap_override = nullptr;
    EmailFacade(const std::string& host, const std::string& user, const std::string& pw)
      : host(host), user(user), pw(pw) {}
    void setSMTP(DummySMTP* d) { smtp_override = d; }
    void setIMAP(DummyIMAP4* d) { imap_override = d; }
    void send_email(const std::string& to, const std::string& subj, const std::string& body) {
        DummySMTP* smtp = smtp_override ? smtp_override : new DummySMTP(host);
        smtp->login(user, pw);
        std::vector<std::string> tolist = {to};
        std::string msg = "From: " + (user.find('@') != std::string::npos ? user : user + "@" + host) + "\n" + body;
        smtp->sendmail(user.find('@')!=std::string::npos ? user : user+"@"+host, tolist, msg);
    }
    std::vector<std::string> get_inbox() {
        DummyIMAP4* imap = imap_override ? imap_override : new DummyIMAP4(host);
        imap->login(user, pw);
        imap->select();
        auto search_res = imap->search();
        std::vector<std::string> res;
        res.push_back("msg1");
        res.push_back("msg2");
        return res;
    }
};

TEST(EmailFacade, SendEmailMonkeypatch) {
    EmailFacade ef("host.com", "user", "pw");
    DummySMTP dummy("host.com");
    ef.setSMTP(&dummy);
    ef.send_email("dest@host.com", "Hi", "Message body");
    EXPECT_EQ(std::get<0>(dummy.logged_in), "user");
    EXPECT_EQ(std::get<1>(dummy.logged_in), "pw");
    EXPECT_TRUE(dummy.sent);
    EXPECT_NE(std::get<2>(dummy.last_args).find("From: user@host.com"), std::string::npos);
    EXPECT_EQ(std::get<1>(dummy.last_args), std::vector<std::string>{"dest@host.com"});
}

TEST(EmailFacade, SendEmailWithFullAddress) {
    EmailFacade ef("host.com", "auser@domain.com", "pw");
    DummySMTP dummy("host.com");
    ef.setSMTP(&dummy);
    ef.send_email("to@host.com", "Subj", "Body");
    EXPECT_EQ(std::get<0>(dummy.logged_in), "auser@domain.com");
    EXPECT_TRUE(dummy.sent);
    EXPECT_NE(std::get<2>(dummy.last_args).find("From: auser@domain.com"), std::string::npos);
}

TEST(EmailFacade, GetInboxMonkeypatch) {
    EmailFacade ef("s", "u", "p");
    DummyIMAP4 dummy("s");
    ef.setIMAP(&dummy);
    auto result = ef.get_inbox();
    EXPECT_FALSE(std::get<0>(dummy.logged).empty());
    EXPECT_TRUE(dummy.selected);
    EXPECT_EQ(result.size(), 2);
}