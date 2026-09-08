#include <gtest/gtest.h>
#include "pynubank/nubank_client.h"

TEST(PublicNubankClientTest, BalanceNonNegative) {
    NubankClient cli;
    auto balance = cli.getBalance();
    EXPECT_GE(balance, 0);
}