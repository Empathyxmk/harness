#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <regex>
#include <tuple>
#include <algorithm>

struct Command {
    std::string action;
    std::string actor;
    std::string commit;
    int priority = -1;
    std::string delegate_to;
};

static std::vector<std::string> split_lines(const std::string& s) {
    std::vector<std::string> lines;
    size_t l = 0;
    while (l < s.size()) {
        size_t n = s.find('\n', l);
        if (n == std::string::npos) n = s.size();
        std::string line = s.substr(l, n-l);
        lines.push_back(line);
        l = n+1;
    }
    return lines;
}

// Simulate parse_issue_comment for testing
std::vector<Command> parse_issue_comment(const std::string& author, const std::string& body, const std::string& commit, const std::string& bot) {
    std::vector<Command> commands;
    auto lines = split_lines(body);
    for (const auto& l : lines) {
        std::string line = l;
        size_t start = line.find_first_not_of(" \t\r\n");
        if (start != std::string::npos) line = line.substr(start);
        size_t end = line.find_last_not_of(" \t\r\n");
        if (end != std::string::npos) line = line.substr(0, end+1);

        std::smatch m;
        if (std::regex_match(line, m, std::regex(R"(^@bors:? r\+$)"))) {
            commands.push_back(Command{"approve", author, commit});
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors r\+ ([a-f0-9]{40})$)"))) {
            std::regex r(R"(^@bors r\+ ([a-f0-9]{40})$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                commands.push_back(Command{"approve", author, m2[1]});
            }
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors r=(?:@)?(\w+)$)"))) {
            std::regex r(R"(^@bors r=(?:@)?(\w+)$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                if (m2[1] == "me") continue;
                commands.push_back(Command{"approve", std::string(m2[1]), ""});
            }
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors r-$)"))) {
            commands.push_back(Command{"unapprove", author, ""});
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors p=(\d+)$)"))) {
            std::regex r(R"(^@bors p=(\d+)$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                Command c{"prioritize", author, ""};
                c.priority = std::stoi(m2[1]);
                commands.push_back(c);
            }
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors r\+ p=(\d+)$)"))) {
            std::regex r(R"(^@bors r\+ p=(\d+)$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                commands.push_back(Command{"approve", author, commit});
                Command c{"prioritize", author, ""};
                c.priority = std::stoi(m2[1]);
                commands.push_back(c);
            }
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors r\+ ([a-f0-9]{40}) p=(\d+)$)"))) {
            std::regex r(R"(^@bors r\+ ([a-f0-9]{40}) p=(\d+)$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                commands.push_back(Command{"approve", author, m2[1]});
                Command c{"prioritize", author, ""};
                c.priority = std::stoi(m2[2]);
                commands.push_back(c);
            }
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors delegate\+$)"))) {
            commands.push_back(Command{"delegate-author", author, ""});
        }
        else if (std::regex_match(line, m, std::regex(R"(^@bors delegate=(?:@)?(\w+)$)"))) {
            std::regex r(R"(^@bors delegate=(?:@)?(\w+)$)");
            std::smatch m2;
            if (std::regex_match(line, m2, r)) {
                Command c{"delegate", author, ""};
                c.delegate_to = m2[1];
                commands.push_back(c);
            }
        }
        else if (line.find("<!-- @bors r=") != std::string::npos) {
            std::regex r("<!-- @bors r=(\\w+) ([a-f0-9]{40}) -->");
            std::smatch m2;
            if (std::regex_search(line, m2, r)) {
                commands.push_back(Command{"approve", std::string(m2[1]), std::string(m2[2])});
            }
        }
    }
    return commands;
}

const std::string commit = "5ffafdb1e94fa87334d4851a57564425e11a569e";
const std::string other_commit = "4e4c9ddd781729173df2720d83e0f4d1b0102a94";

TEST(ParseIssueCommentTest, RPlus) {
    auto author = "jack";
    auto body = "@bors r+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
}

TEST(ParseIssueCommentTest, RPlusWithColon) {
    auto author = "jack";
    auto body = "@bors: r+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, commit);
}

TEST(ParseIssueCommentTest, RPlusWithSha) {
    auto author = "jack";
    auto body = "@bors r+ " + other_commit;
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, other_commit);
}

TEST(ParseIssueCommentTest, REquals) {
    auto author = "jack";
    auto body = "@bors r=jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jill");
}

TEST(ParseIssueCommentTest, REqualsAtUser) {
    auto author = "jack";
    auto body = "@bors r=@jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jill");
}

TEST(ParseIssueCommentTest, HiddenREquals) {
    auto author = "bors";
    auto body = ":pushpin: Commit " + commit + " has been approved by `jack`\nIt is now in the [queue](rust) for this repository.\n\n<!-- @bors r=jack " + commit + " -->";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, commit);
}

TEST(ParseIssueCommentTest, RMeIgnored) {
    auto author = "jack";
    auto body = "@bors r=me";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 0);
}

TEST(ParseIssueCommentTest, RMinus) {
    auto author = "jack";
    auto body = "@bors r-";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "unapprove");
}

TEST(ParseIssueCommentTest, Priority) {
    auto author = "jack";
    auto body = "@bors p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "prioritize");
    EXPECT_EQ(commands[0].priority, 5);
}

TEST(ParseIssueCommentTest, ApproveAndPriority) {
    auto author = "jack";
    auto body = "@bors r+ p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 2);
    auto approve_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action == "approve";});
    auto prior_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action == "prioritize";});
    ASSERT_TRUE(approve_cmd != commands.end());
    ASSERT_TRUE(prior_cmd != commands.end());
    EXPECT_EQ(approve_cmd->actor, "jack");
    EXPECT_EQ(prior_cmd->priority, 5);
}

TEST(ParseIssueCommentTest, ApproveSpecificAndPriority) {
    auto author = "jack";
    auto body = "@bors r+ " + other_commit + " p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 2);
    auto approve_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action == "approve";});
    auto prior_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action == "prioritize";});
    ASSERT_TRUE(approve_cmd != commands.end());
    ASSERT_TRUE(prior_cmd != commands.end());
    EXPECT_EQ(approve_cmd->actor, "jack");
    EXPECT_EQ(approve_cmd->commit, other_commit);
    EXPECT_EQ(prior_cmd->priority, 5);
}

TEST(ParseIssueCommentTest, DelegatePlus) {
    auto author = "jack";
    auto body = "@bors delegate+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate-author");
}

TEST(ParseIssueCommentTest, DelegateEquals) {
    auto author = "jack";
    auto body = "@bors delegate=jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate");
    EXPECT_EQ(commands[0].delegate_to, "jill");
}

TEST(ParseIssueCommentTest, DelegateEqualsAtUser) {
    auto author = "jack";
    auto body = "@bors delegate=@jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate");
    EXPECT_EQ(commands[0].delegate_to, "jill");
}