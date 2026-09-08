#include <gtest/gtest.h>
#include "pyzbar/scripts/read_zbar.h"
#include <string>

TEST(ReadZbarPublic, GetArgsQRCode) {
    auto args = read_zbar_get_args({"barcode_testimage.png"});
    EXPECT_EQ(args.file, "barcode_testimage.png");

    auto args2 = read_zbar_get_args({"-v", "--"});
    EXPECT_TRUE(args2.verbose);
}

TEST(ReadZbarPublic, MainNoFile) {
    EXPECT_THROW({
        read_zbar_get_args({});
    }, std::runtime_error);
}