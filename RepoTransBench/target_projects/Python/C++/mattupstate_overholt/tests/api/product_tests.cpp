#include <gtest/gtest.h>
#include "tests/factories.h"
#include "tests/api/overholt_api_test_case.h"

class ProductApiTestCase : public OverholtApiTestCase {
protected:
    void SetUp() override {
        OverholtApiTestCase::SetUp();
        category = CategoryFactory();
        product = ProductFactory({category});
    }
    Category category;
    Product product;
};

TEST_F(ProductApiTestCase, GetProducts) {
    ApiResponse r = jget("/products");
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(ProductApiTestCase, GetProduct) {
    ApiResponse r = jget("/products/" + std::to_string(product.id));
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(ProductApiTestCase, CreateProduct) {
    ApiResponse r = jpost("/products", {{"name", "New Product"}, {"categories", std::to_string(category.id)}});
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(ProductApiTestCase, CreateInvalidProduct) {
    ApiResponse r = jpost("/products", {{"categories", std::to_string(category.id)}});
    ASSERT_TRUE(assertBadJson(r));
}

TEST_F(ProductApiTestCase, UpdateProduct) {
    ApiResponse r = jput("/products/" + std::to_string(product.id), {{"name", "New Product"}});
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(ProductApiTestCase, DeleteProduct) {
    ApiResponse r = jdelete("/products/" + std::to_string(product.id));
    ASSERT_TRUE(assertStatusCode(r, 204));
}