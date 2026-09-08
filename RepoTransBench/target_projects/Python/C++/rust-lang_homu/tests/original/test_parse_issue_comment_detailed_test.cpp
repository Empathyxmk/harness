#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <regex>
#include <sstream>
#include <tuple>
#include <algorithm>

/**
 * Simulate parsed command objects:
 */
struct Command {
    std::string action;
    std::string actor;
    std::string commit;
    int priority = -1;
    std::string delegate_to;
};

// Simulate parse_issue_comment function from Python.
// For the purposes of these tests, we simulate only the patterns actually tested.
std::vector<Command> parse_issue_comment(const std::string& author, const std::string& body, const std::string& commit, const std::string& bot) {
    std::vector<Command> commands;
    std::string trimmed = body;
    // break into lines (simulate parsing)
    std::vector<std::string> lines;
    std::istringstream iss(trimmed);
    std::string line;
    while (std::getline(iss, line)) {
        // Remove leading/trailing whitespace from line
        size_t start = line.find_first_not_of(" \t\r\n");
        if (start != std::string::npos)
            line = line.substr(start);
        size_t end = line.find_last_not_of(" \t\r\n");
        if (end != std::string::npos)
            line = line.substr(0, end + 1);
        lines.push_back(line);
    }
    for (const auto& l : lines) {
        std::smatch m;
        // @bors r+
        if (std::regex_match(l, m, std::regex("@bors:? r\\+$"))) {
            Command c;
            c.action = "approve";
            c.actor = author;
            c.commit = commit;
            commands.push_back(c);
        }
        // @bors: r+
        else if (std::regex_match(l, m, std::regex("@bors: r\\+$"))) {
            Command c;
            c.action = "approve";
            c.actor = author;
            c.commit = commit;
            commands.push_back(c);
        }
        // @bors r+ {sha}
        else if (std::regex_match(l, m, std::regex("@bors r\\+ ([a-f0-9]{40})"))) {
            std::regex r("@bors r\\+ ([a-f0-9]{40})");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                Command c;
                c.action = "approve";
                c.actor = author;
                c.commit = m2[1];
                commands.push_back(c);
            }
        }
        // @bors r=jill
        else if (std::regex_match(l, m, std::regex("@bors r=(?:@)?(\\w+)$"))) {
            std::regex r("@bors r=(?:@)?(\\w+)$");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                // If r=me, we ignore
                if (m2[1] == "me") {
                    // No command returned
                    continue;
                }
                Command c;
                c.action = "approve";
                c.actor = m2[1];
                c.commit = "";
                commands.push_back(c);
            }
        }
        // @bors r- (unapprove)
        else if (std::regex_match(l, m, std::regex("@bors r-$"))) {
            Command c;
            c.action = "unapprove";
            c.actor = author;
            c.commit = "";
            commands.push_back(c);
        }
        // @bors p=5 (priority)
        else if (std::regex_match(l, m, std::regex("@bors p=([0-9]+)$"))) {
            std::regex r("@bors p=([0-9]+)$");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                Command c;
                c.action = "prioritize";
                c.actor = author;
                c.commit = "";
                c.priority = std::stoi(m2[1]);
                commands.push_back(c);
            }
        }
        // @bors r+ p=5 or @bors r+ {sha} p=5 (both present)
        else if (std::regex_match(l, m, std::regex("@bors r\\+ p=([0-9]+)$"))) {
            std::regex r("@bors r\\+ p=([0-9]+)$");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                Command c1;
                c1.action = "approve";
                c1.actor = author;
                c1.commit = commit;
                commands.push_back(c1);
                Command c2;
                c2.action = "prioritize";
                c2.actor = author;
                c2.commit = "";
                c2.priority = std::stoi(m2[1]);
                commands.push_back(c2);
            }
        }
        else if (std::regex_match(l, m, std::regex("@bors r\\+ ([a-f0-9]{40}) p=([0-9]+)$"))) {
            std::regex r("@bors r\\+ ([a-f0-9]{40}) p=([0-9]+)$");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                Command c1;
                c1.action = "approve";
                c1.actor = author;
                c1.commit = m2[1];
                commands.push_back(c1);
                Command c2;
                c2.action = "prioritize";
                c2.actor = author;
                c2.priority = std::stoi(m2[2]);
                commands.push_back(c2);
            }
        }
        // @bors delegate+
        else if (std::regex_match(l, m, std::regex("@bors delegate\\+$"))) {
            Command c;
            c.action = "delegate-author";
            c.actor = author;
            c.commit = "";
            commands.push_back(c);
        }
        // @bors delegate=jill or @bors delegate=@jill
        else if (std::regex_match(l, m, std::regex("@bors delegate=(?:@)?(\\w+)$"))) {
            std::regex r("@bors delegate=(?:@)?(\\w+)$");
            std::smatch m2;
            if (std::regex_match(l, m2, r)) {
                Command c;
                c.action = "delegate";
                c.actor = author;
                c.delegate_to = m2[1];
                c.commit = "";
                commands.push_back(c);
            }
        }
        // delegate in html comment (hidden r= in comment)
        else if (l.find("<!-- @bors r=") != std::string::npos) {
            std::regex r("<!-- @bors r=(\\w+) ([a-f0-9]{40}) -->");
            std::smatch m2;
            if (std::regex_search(l, m2, r)) {
                Command c;
                c.action = "approve";
                c.actor = m2[1];
                c.commit = m2[2];
                commands.push_back(c);
            }
        }
    }
    return commands;
}

const std::string commit = "5ffafdb1e94fa87334d4851a57564425e11a569e";
const std::string other_commit = "4e4c9ddd781729173df2720d83e0f4d1b0102a94";

TEST(ParseIssueCommentDetailedTest, RPlus) {
    std::string author = "jack";
    std::string body = "@bors r+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
}

TEST(ParseIssueCommentDetailedTest, RPlusWithColon) {
    std::string author = "jack";
    std::string body = "@bors: r+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, commit);
}

TEST(ParseIssueCommentDetailedTest, RPlusWithSha) {
    std::string author = "jack";
    std::string body = "@bors r+ " + other_commit;
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, other_commit);
}

TEST(ParseIssueCommentDetailedTest, REquals) {
    std::string author = "jack";
    std::string body = "@bors r=jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jill");
}

TEST(ParseIssueCommentDetailedTest, REqualsAtUser) {
    std::string author = "jack";
    std::string body = "@bors r=@jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jill");
}

TEST(ParseIssueCommentDetailedTest, HiddenREquals) {
    std::string author = "bors";
    std::string body = ":pushpin: Commit " + commit + " has been approved by `jack`\nIt is now in the [queue](rust) for this repository.\n\n<!-- @bors r=jack " + commit + " -->";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "approve");
    EXPECT_EQ(commands[0].actor, "jack");
    EXPECT_EQ(commands[0].commit, commit);
}

TEST(ParseIssueCommentDetailedTest, RMeIgnored) {
    std::string author = "jack";
    std::string body = "@bors r=me";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 0);
}

TEST(ParseIssueCommentDetailedTest, RMinus) {
    std::string author = "jack";
    std::string body = "@bors r-";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "unapprove");
}

TEST(ParseIssueCommentDetailedTest, Priority) {
    std::string author = "jack";
    std::string body = "@bors p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "prioritize");
    EXPECT_EQ(commands[0].priority, 5);
}

TEST(ParseIssueCommentDetailedTest, ApproveAndPriority) {
    std::string author = "jack";
    std::string body = "@bors r+ p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 2);
    auto approve_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action=="approve";});
    auto prior_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action=="prioritize";});
    ASSERT_TRUE(approve_cmd != commands.end());
    ASSERT_TRUE(prior_cmd != commands.end());
    EXPECT_EQ(approve_cmd->actor, "jack");
    EXPECT_EQ(prior_cmd->priority, 5);
}

TEST(ParseIssueCommentDetailedTest, ApproveSpecificAndPriority) {
    std::string author = "jack";
    std::string body = "@bors r+ " + other_commit + " p=5";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 2);
    auto approve_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action=="approve";});
    auto prior_cmd = std::find_if(commands.begin(), commands.end(), [](const Command& c){return c.action=="prioritize";});
    ASSERT_TRUE(approve_cmd != commands.end());
    ASSERT_TRUE(prior_cmd != commands.end());
    EXPECT_EQ(approve_cmd->actor, "jack");
    EXPECT_EQ(approve_cmd->commit, other_commit);
    EXPECT_EQ(prior_cmd->priority, 5);
}

TEST(ParseIssueCommentDetailedTest, DelegatePlus) {
    std::string author = "jack";
    std::string body = "@bors delegate+";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate-author");
}

TEST(ParseIssueCommentDetailedTest, DelegateEquals) {
    std::string author = "jack";
    std::string body = "@bors delegate=jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate");
    EXPECT_EQ(commands[0].delegate_to, "jill");
}

TEST(ParseIssueCommentDetailedTest, DelegateEqualsAtUser) {
    std::string author = "jack";
    std::string body = "@bors delegate=@jill";
    auto commands = parse_issue_comment(author, body, commit, "bors");
    ASSERT_EQ(commands.size(), 1);
    EXPECT_EQ(commands[0].action, "delegate");
    EXPECT_EQ(commands[0].delegate_to, "jill");
}