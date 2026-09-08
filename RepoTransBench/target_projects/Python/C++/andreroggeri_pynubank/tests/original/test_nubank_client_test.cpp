#include <gtest/gtest.h>
#include "pynubank/nubank_client.h"

TEST(NubankClientTest, CanQueryBalance) {
    NubankClient cli;
    auto balance = cli.getBalance();
    EXPECT_GT(balance, 0);
}

TEST(NubankClientTest, InvalidLoginThrows) {
    NubankClient cli;
    EXPECT_THROW(cli.login("", ""), NubankException);
}