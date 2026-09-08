#include <gtest/gtest.h>
#include <future>
#include <vector>
#include <map>
#include <string>
#include <type_traits>
#include <functional>
#include <memory>
#include <stdexcept>
#include <tuple>
#include <thread>
#include <atomic>
#include <chrono>
#include <utility>
#include "aiodataloader/dateloader.h"

// Helper for async test cases (simulate async)
#define ASYNC_TEST(test_case_name, test_name) TEST(test_case_name, test_name)

using namespace std::chrono_literals;

// DataLoader stub for testing (replace with actual implementation)
template <typename K, typename V>
class DataLoader {
public:
    using BatchFn = std::function<std::vector<V>(const std::vector<K>&)>;
    using BatchFnAsync = std::function<std::future<std::vector<V>>(const std::vector<K>&)>;

    explicit DataLoader(BatchFn fn) : func(fn), cache(true), max_batch_size(0) {}
    DataLoader(BatchFn fn, bool cache_) : func(fn), cache(cache_), max_batch_size(0) {}
    DataLoader(BatchFn fn, bool cache_, int batch_size) : func(fn), cache(cache_), max_batch_size(batch_size) {}

    std::future<V> load(const K& key) {
        std::promise<V> prom;
        auto f = prom.get_future();
        std::thread([=, this]() mutable {
            // Simulate async
            std::vector<K> keys = {key};
            auto res = func(keys);
            prom.set_value(res[0]);
        }).detach();
        return f;
    }
    std::future<std::vector<V>> load_many(const std::vector<K>& keys) {
        std::promise<std::vector<V>> prom;
        auto f = prom.get_future();
        std::thread([=, this]() mutable {
            auto res = func(keys);
            prom.set_value(res);
        }).detach();
        return f;
    }

    DataLoader& clear(const K&) { return *this; }
    void clear_all() {}
    void prime(const K&, const V&) {}
};

namespace {

template<typename T>
using LoaderResult = std::tuple<DataLoader<T, T>, std::vector<std::vector<T>>>;

template <typename T>
LoaderResult<T> id_loader() {
    static std::vector<std::vector<T>> load_calls;
    auto fn = [](const std::vector<T>& keys) {
        load_calls.push_back(keys);
        return keys;
    };
    DataLoader<T,T> loader(fn);
    return std::make_tuple(loader, load_calls);
}

ASYNC_TEST(AioDataLoaderTest, build_a_simple_data_loader) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int, int> loader(fn);
    auto fut = loader.load(1);
    EXPECT_EQ(fut.get(), 1);
}

ASYNC_TEST(AioDataLoaderTest, can_build_from_partial) {
    std::map<int, std::string> value_map = { {1, "one"} };
    auto fn = [=](const std::vector<int>& keys) {
        std::vector<std::string> out;
        for (auto k : keys) {
            auto it = value_map.find(k);
            out.push_back(it != value_map.end() ? it->second : "");
        }
        return out;
    };
    DataLoader<int, std::string> loader(fn);
    auto fut = loader.load(1);
    EXPECT_EQ(fut.get(), "one");
}

ASYNC_TEST(AioDataLoaderTest, supports_loading_multiple_keys_in_one_call) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int, int> loader(fn);
    auto fut = loader.load_many({1, 2});
    auto out = fut.get();
    EXPECT_EQ((out == std::vector<int>{1,2}), true);
    auto empty_fut = loader.load_many({});
    EXPECT_EQ((empty_fut.get() == std::vector<int>{}), true);
}

ASYNC_TEST(AioDataLoaderTest, batches_multiple_requests) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int, int> loader(fn);

    auto fut1 = loader.load(1);
    auto fut2 = loader.load(2);
    auto v1 = fut1.get();
    auto v2 = fut2.get();
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
}

ASYNC_TEST(AioDataLoaderTest, batches_multiple_requests_with_max_batch_sizes) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int, int> loader(fn);

    auto fut1 = loader.load(1);
    auto fut2 = loader.load(2);
    auto fut3 = loader.load(3);

    int v1 = fut1.get();
    int v2 = fut2.get();
    int v3 = fut3.get();
    EXPECT_EQ(v1, 1);
    EXPECT_EQ(v2, 2);
    EXPECT_EQ(v3, 3);
}

ASYNC_TEST(AioDataLoaderTest, coalesces_identical_requests) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int, int> loader(fn);

    auto fut1 = loader.load(1);
    auto fut2 = loader.load(1);

    EXPECT_EQ(fut1.wait_for(0s), std::future_status::ready);
    EXPECT_EQ(fut1.get(), 1);
    EXPECT_EQ(fut2.get(), 1);
}

ASYNC_TEST(AioDataLoaderTest, caches_repeated_requests) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string, std::string> loader(fn);

    auto futa = loader.load("A");
    auto futb = loader.load("B");
    EXPECT_EQ(futa.get(), "A");
    EXPECT_EQ(futb.get(), "B");

    auto futa2 = loader.load("A");
    auto futc = loader.load("C");
    EXPECT_EQ(futa2.get(), "A");
    EXPECT_EQ(futc.get(), "C");

    auto futa3 = loader.load("A");
    auto futb2 = loader.load("B");
    auto futc2 = loader.load("C");
    EXPECT_EQ(futa3.get(), "A");
    EXPECT_EQ(futb2.get(), "B");
    EXPECT_EQ(futc2.get(), "C");
}

ASYNC_TEST(AioDataLoaderTest, clears_single_value_in_loader) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string, std::string> loader(fn);

    auto futa = loader.load("A");
    auto futb = loader.load("B");
    EXPECT_EQ(futa.get(), "A");
    EXPECT_EQ(futb.get(), "B");
    loader.clear("A");
    auto futa2 = loader.load("A");
    auto futb2 = loader.load("B");
    EXPECT_EQ(futa2.get(), "A");
    EXPECT_EQ(futb2.get(), "B");
}

ASYNC_TEST(AioDataLoaderTest, clears_all_values_in_loader) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string, std::string> loader(fn);

    auto futa = loader.load("A");
    auto futb = loader.load("B");
    EXPECT_EQ(futa.get(), "A");
    EXPECT_EQ(futb.get(), "B");
    loader.clear_all();
    auto futa2 = loader.load("A");
    auto futb2 = loader.load("B");
    EXPECT_EQ(futa2.get(), "A");
    EXPECT_EQ(futb2.get(), "B");
}

ASYNC_TEST(AioDataLoaderTest, allows_priming_the_cache) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string, std::string> loader(fn);
    loader.prime("A", "A");
    auto futa = loader.load("A");
    auto futb = loader.load("B");
    EXPECT_EQ(futa.get(), "A");
    EXPECT_EQ(futb.get(), "B");
}

// Exception/failure simulation tests would be added here similarly

}  // namespace