#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

// Example stubs for missing actual application headers/classes.
class Account {
public:
    Account(const std::string& name)
        : name_(name)
    {}

    std::string getName() const {
        return name_;
    }

    int add(int a, int b) const {
        return a + b;
    }

    void throwIfInvalid(const std::string& value) const {
        if (value.empty()) {
            throw std::invalid_argument("Value must not be empty");
        }
    }

private:
    std::string name_;
};

class AccountTest : public ::testing::Test {
protected:
    virtual void SetUp() override {
        account = new Account("testuser");
    }
    virtual void TearDown() override {
        delete account;
    }
    Account* account;
};

TEST_F(AccountTest, GetNameShouldReturnCorrectName) {
    EXPECT_EQ(account->getName(), "testuser");
}

TEST_F(AccountTest, AddShouldReturnSum) {
    EXPECT_EQ(account->add(2, 3), 5);
    EXPECT_EQ(account->add(-1, 1), 0);
}

TEST_F(AccountTest, ThrowIfInvalidThrowsForEmptyString) {
    EXPECT_THROW(account->throwIfInvalid(""), std::invalid_argument);
}

TEST_F(AccountTest, ThrowIfInvalidNoThrowForNonEmptyString) {
    EXPECT_NO_THROW(account->throwIfInvalid("apple"));
}