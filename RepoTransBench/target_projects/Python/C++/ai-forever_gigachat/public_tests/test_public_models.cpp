#include <gtest/gtest.h>
#include "gigachat/Model.h"
using gigachat::Model;

TEST(PublicModelsTest, InitAndFields) {
    Model model("special_object", "test_id_2", 1234567, "SuperGigaModel", "public_giga_owner");
    ASSERT_EQ(model.id, "test_id_2");
    ASSERT_EQ(model.object, "special_object");
    ASSERT_EQ(model.name, "SuperGigaModel");
    ASSERT_EQ(model.owned_by, "public_giga_owner");
    ASSERT_EQ(model.created, 1234567);
    // Skipping x_headers, not used in this stub.
}

TEST(PublicModelsTest, StrAndReprPublic) {
    Model model("public_object", "AAA_public", 1010101, "PublicModel", "someone_else");
    std::string text = model.to_string();
    ASSERT_TRUE(text.find("AAA_public") != std::string::npos || text.find("PublicModel") != std::string::npos);
    std::string rep = model.to_string();
    ASSERT_TRUE(rep.find("AAA_public") != std::string::npos || rep.find("PublicModel") != std::string::npos);
}