#include <gtest/gtest.h>
#include "pyzbar/pyzbar_error.h"
#include <string>

TEST(PyzbarErrorPublic, ErrorMessage) {
    PyZbarError e("Public test: barcode problem");
    EXPECT_EQ(std::string(e.what()), "Public test: barcode problem");
}

TEST(PyzbarErrorPublic, ErrorRaiseAndCatch) {
    try {
        throw PyZbarError("Test error for catching");
    } catch(const PyZbarError& e) {
        EXPECT_NE(std::string(e.what()).find("catching"), std::string::npos);
    }
}