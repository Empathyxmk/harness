#include <gtest/gtest.h>
#include "tests/factories.h"
#include "tests/api/overholt_api_test_case.h"

class StoreApiTestCase : public OverholtApiTestCase {
protected:
    void SetUp() override {
        OverholtApiTestCase::SetUp();
        product = ProductFactory();
        store = StoreFactory({product});
    }
    Product product;
    Store store;
};

TEST_F(StoreApiTestCase, GetStores) {
    ApiResponse r = jget("/stores");
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(StoreApiTestCase, GetStore) {
    ApiResponse r = jget("/stores/" + std::to_string(store.id));
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(StoreApiTestCase, CreateStore) {
    ApiResponse r = jpost("/stores", {
        {"name", "My Store"},
        {"address", "123 Overholt Drive"},
        {"city", "Brooklyn"},
        {"state", "New York"},
        {"zip_code", "12345"}
    });
    ASSERT_TRUE(assertOkJson(r));
    ASSERT_NE(r.data.find("\"name\": \"My Store\""), std::string::npos);
}

TEST_F(StoreApiTestCase, CreateInvalidStore) {
    ApiResponse r = jpost("/stores", {{"name", "My Store"}});
    ASSERT_TRUE(assertBadJson(r));
    ASSERT_NE(r.data.find("\"errors\": {"), std::string::npos);
}

TEST_F(StoreApiTestCase, UpdateStore) {
    ApiResponse r = jput("/stores/" + std::to_string(store.id), {{"name", "My New Store"}});
    ASSERT_TRUE(assertOkJson(r));
    ASSERT_NE(r.data.find("\"name\": \"My New Store\""), std::string::npos);
}

TEST_F(StoreApiTestCase, DeleteStore) {
    ApiResponse r = jdelete("/stores/" + std::to_string(store.id));
    ASSERT_TRUE(assertStatusCode(r, 204));
}

TEST_F(StoreApiTestCase, GetProducts) {
    ApiResponse r = jget("/stores/" + std::to_string(store.id) + "/products");
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(StoreApiTestCase, AddProduct) {
    Product p = ProductFactory();
    std::string e = "/stores/" + std::to_string(store.id) + "/products/" + std::to_string(p.id);
    ApiResponse r = jput(e);
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(StoreApiTestCase, RemoveProduct) {
    std::string e = "/stores/" + std::to_string(store.id) + "/products/" + std::to_string(product.id);
    ApiResponse r = jdelete(e);
    ASSERT_TRUE(assertStatusCode(r, 204));
}

TEST_F(StoreApiTestCase, AddManager) {
    std::string e = "/stores/" + std::to_string(store.id) + "/managers/" + std::to_string(user.id);
    ApiResponse r = jput(e);
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(StoreApiTestCase, AddExistingManager) {
    std::string e = "/stores/" + std::to_string(store.id) + "/managers/" + std::to_string(user.id);
    jput(e);
    ApiResponse r = jput(e);
    ASSERT_TRUE(assertBadJson(r));
}

TEST_F(StoreApiTestCase, RemoveManager) {
    std::string e = "/stores/" + std::to_string(store.id) + "/managers/" + std::to_string(user.id);
    jput(e);
    ApiResponse r = jdelete(e);
    ASSERT_TRUE(assertStatusCode(r, 204));
}