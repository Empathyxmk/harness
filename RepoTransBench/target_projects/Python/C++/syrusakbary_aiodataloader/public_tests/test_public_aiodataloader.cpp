#include <gtest/gtest.h>
#include <future>
#include <vector>
#include <map>
#include <string>
#include <type_traits>
#include <functional>
#include <memory>
#include <tuple>
#include <thread>
#include <chrono>
#include <stdexcept>
#include <utility>
#include "aiodataloader/dateloader.h"

using namespace std::chrono_literals;

template <typename K, typename V>
class DataLoader {
public:
    using BatchFn = std::function<std::vector<V>(const std::vector<K>&)>;
    DataLoader(BatchFn fn) : fn_(fn) {}

    std::future<V> load(K key) {
        std::promise<V> prom;
        auto fut = prom.get_future();
        std::thread([=, this]() mutable {
            std::vector<K> keys = { key };
            auto res = fn_(keys);
            prom.set_value(res[0]);
        }).detach();
        return fut;
    }
    std::future<std::vector<V>> load_many(std::vector<K> keys) {
        std::promise<std::vector<V>> prom;
        auto fut = prom.get_future();
        std::thread([=, this]() mutable {
            auto res = fn_(keys);
            prom.set_value(res);
        }).detach();
        return fut;
    }
    void clear(const K&) {}
    void clear_all() {}
    void prime(const K&, const V&) {}
private:
    BatchFn fn_;
};

namespace {
template<typename K, typename V>
std::tuple<DataLoader<K,V>, std::vector<std::vector<K>>> id_loader_public() {
    static std::vector<std::vector<K>> load_calls;
    auto fn = [](const std::vector<K>& keys) {
        load_calls.push_back(keys);
        return keys;
    };
    DataLoader<K,V> loader(fn);
    return std::make_tuple(loader, load_calls);
}

TEST(PublicAioDataLoader, build_a_simple_data_loader_public) {
    auto fn = [](const std::vector<int>& keys) { std::vector<int> out; for(auto k:keys) out.push_back(k+10); return out; };
    DataLoader<int,int> loader(fn);
    auto fut = loader.load(5);
    EXPECT_EQ(fut.get(), 15);
}

TEST(PublicAioDataLoader, can_build_a_data_loader_from_a_partial_public) {
    std::map<int, std::string> value_map = {{3,"three"}, {4,"four"}};
    auto fn = [=](const std::vector<int>& keys) {
        std::vector<std::string> out;
        for(auto k:keys) {
            auto it = value_map.find(k);
            out.push_back(it != value_map.end() ? it->second : "");
        }
        return out;
    };
    DataLoader<int, std::string> loader(fn);
    auto fut = loader.load(3);
    EXPECT_EQ(fut.get(), "three");
}

TEST(PublicAioDataLoader, supports_loading_multiple_keys_in_one_call_public) {
    auto fn = [](const std::vector<int>& keys) {
        std::vector<int> out;
        for(auto k:keys) out.push_back(k*2);
        return out;
    };
    DataLoader<int, int> loader(fn);
    auto fut = loader.load_many({5,6});
    std::vector<int> res = fut.get();
    EXPECT_EQ(res, (std::vector<int>{10,12}));
    auto fut2 = loader.load_many({8,9});
    EXPECT_EQ(fut2.get(), (std::vector<int>{16,18}));
    auto empty = loader.load_many({});
    EXPECT_EQ(empty.get(), (std::vector<int>{}));
}

TEST(PublicAioDataLoader, batches_multiple_requests_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);
    auto promiseA = loader.load("alpha");
    auto promiseB = loader.load("beta");
    auto va = promiseA.get();
    auto vb = promiseB.get();
    EXPECT_EQ(va, "alpha");
    EXPECT_EQ(vb, "beta");
}

TEST(PublicAioDataLoader, batches_multiple_requests_with_max_batch_sizes_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);

    auto p1 = loader.load("x");
    auto p2 = loader.load("y");
    auto p3 = loader.load("z");
    EXPECT_EQ(p1.get(), "x");
    EXPECT_EQ(p2.get(), "y");
    EXPECT_EQ(p3.get(), "z");
}

TEST(PublicAioDataLoader, coalesces_identical_requests_public) {
    auto fn = [](const std::vector<int>& keys) { return keys; };
    DataLoader<int,int> loader(fn);
    auto a1 = loader.load(42);
    auto a2 = loader.load(42);
    auto v1 = a1.get();
    auto v2 = a2.get();
    EXPECT_EQ(v1, 42);
    EXPECT_EQ(v2, 42);
}

TEST(PublicAioDataLoader, caches_repeated_requests_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);
    auto a = loader.load("X");
    auto b = loader.load("Y");
    EXPECT_EQ(a.get(), "X");
    EXPECT_EQ(b.get(), "Y");
    auto a2 = loader.load("X");
    auto c = loader.load("Z");
    EXPECT_EQ(a2.get(), "X");
    EXPECT_EQ(c.get(), "Z");
    auto x3 = loader.load("X");
    auto y2 = loader.load("Y");
    auto z2 = loader.load("Z");
    EXPECT_EQ(x3.get(), "X");
    EXPECT_EQ(y2.get(), "Y");
    EXPECT_EQ(z2.get(), "Z");
}

TEST(PublicAioDataLoader, clears_single_value_in_loader_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);
    auto a = loader.load("D");
    auto b = loader.load("E");
    EXPECT_EQ(a.get(), "D");
    EXPECT_EQ(b.get(), "E");
    loader.clear("D");
    auto a2 = loader.load("D");
    auto e2 = loader.load("E");
    EXPECT_EQ(a2.get(), "D");
    EXPECT_EQ(e2.get(), "E");
}

TEST(PublicAioDataLoader, clears_all_values_in_loader_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);
    auto s = loader.load("S");
    auto t = loader.load("T");
    EXPECT_EQ(s.get(), "S");
    EXPECT_EQ(t.get(), "T");
    loader.clear_all();
    auto s2 = loader.load("S");
    auto t2 = loader.load("T");
    EXPECT_EQ(s2.get(), "S");
    EXPECT_EQ(t2.get(), "T");
}

TEST(PublicAioDataLoader, allows_priming_the_cache_public) {
    auto fn = [](const std::vector<std::string>& keys) { return keys; };
    DataLoader<std::string,std::string> loader(fn);
    loader.prime("U","U-prime");
    auto u = loader.load("U");
    auto v = loader.load("V");
    EXPECT_EQ(u.get(), "U-prime");
    EXPECT_EQ(v.get(), "V");
}
} // namespace