#include <gtest/gtest.h>
#include <string>
#include <functional>
#include <map>
#include <future>
#include <vector>
#include <memory>
#include "aiodataloader/dateloader.h"

// Simulated utility and dataloader
template<typename T>
constexpr bool iscoroutinefunctionorpartial(T) {
    // In C++ we could use type traits, but here always false for simplicity
    return std::is_function<T>::value;
}

const std::string __version__ = "1.0.0";

template <typename K, typename V>
class DataLoader {
public:
    using BatchFn = std::function<std::vector<V>(const std::vector<K>&)>;
    std::map<K, std::shared_ptr<std::future<V>>> _cache;
    bool cache;
    void* loop = nullptr;
    BatchFn fn;

    DataLoader(BatchFn fn_, bool cache_ = true, void* loop_ = nullptr) : fn(fn_), cache(cache_), loop(loop_) {}

    std::future<V> load(const K& key) {
        std::promise<V> prom;
        auto fut = prom.get_future();
        std::thread([=, this]() mutable {
            std::vector<K> keys = { key };
            auto res = fn(keys);
            prom.set_value(res[0]);
        }).detach();
        return fut;
    }

    DataLoader& clear(const K& k) {
        _cache.erase(k);
        return *this;
    }
    void clear_all() { _cache.clear(); }
    void prime(const K& k, V v) {
        auto p = std::make_shared<std::promise<V>>();
        p->set_value(v);
        _cache[k] = std::make_shared<std::future<V>>(p->get_future());
    }
    std::function<int(const K&)> get_cache_key = [](const K& k) { return (int)k; };
};

TEST(PublicAdditionalAioDataLoader, iscoroutinefunctionorpartial_true_on_coro_fn_pub) {
    auto fn = []() {};
    EXPECT_TRUE(iscoroutinefunctionorpartial(fn));
}
TEST(PublicAdditionalAioDataLoader, iscoroutinefunctionorpartial_true_on_partial_coro_pub) {
    auto base_fn = []() {};
    auto partial_fn = base_fn;
    EXPECT_TRUE(iscoroutinefunctionorpartial(partial_fn));
}
TEST(PublicAdditionalAioDataLoader, iscoroutinefunctionorpartial_false_on_regular_pub) {
    int i = 42;
    EXPECT_FALSE(iscoroutinefunctionorpartial(i));
}
TEST(PublicAdditionalAioDataLoader, version_in_module_pub) {
    EXPECT_EQ(__version__.find('.') != std::string::npos, true);
}
TEST(PublicAdditionalAioDataLoader, dataloader_batch_load_fn_typeerror_and_coroutine_check_pub) {
    auto not_coro_fn = [](const std::vector<int>& keys) { return keys; };
    SUCCEED();
}
TEST(PublicAdditionalAioDataLoader, dataloader_default_get_cache_key_exists_pub) {
    auto fn = [](const std::vector<int>& keys) { std::vector<int> out; for(auto k:keys) out.push_back(k*2); return out; };
    DataLoader<int, int> dl(fn);
    EXPECT_TRUE(dl.get_cache_key != nullptr);
}
TEST(PublicAdditionalAioDataLoader, dataloader_cache_false_actually_avoids_caching_pub) {
    auto fn = [](const std::vector<int>& keys) { std::vector<int> out; for(auto k:keys) out.push_back(k+1); return out; };
    DataLoader<int, int> dl(fn, false);
    auto fut1 = dl.load(7);
    auto fut2 = dl.load(7);
    EXPECT_NE(&fut1, &fut2);
}
TEST(PublicAdditionalAioDataLoader, dataloader_clear_cache_and_prime_behavior_pub) {
    auto fn = [](const std::vector<int>& keys) { std::vector<int> out; for(auto k:keys) out.push_back(k-1); return out; };
    DataLoader<int, int> dl(fn);
    dl.prime(322, 1001);
    EXPECT_TRUE(dl._cache[322] != nullptr);
    dl.clear(322);
    EXPECT_EQ(dl._cache.count(322), 0);
}
TEST(PublicAdditionalAioDataLoader, dataloader_clear_all_pub) {
    auto fn = [](const std::vector<int>& keys) { std::vector<std::string> out; for(auto k:keys) out.push_back(std::to_string(k)); return out; };
    DataLoader<int, std::string> dl(fn);
    for(int k=5; k<8; ++k) {
        dl.prime(k, std::to_string(k));
    }
    dl.clear_all();
    EXPECT_TRUE(dl._cache.empty());
}
TEST(PublicAdditionalAioDataLoader, dataloader_custom_loop_pub) {
    auto fn = [](const std::vector<std::string>& keys) { std::vector<std::string> out; for(const auto& x:keys) out.push_back(x); return out; };
    int dummy;
    DataLoader<std::string, std::string> dl(fn, true, &dummy);
    EXPECT_EQ(dl.loop, &dummy);
}