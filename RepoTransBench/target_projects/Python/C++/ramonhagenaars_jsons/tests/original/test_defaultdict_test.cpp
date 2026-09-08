#include <gtest/gtest.h>
#include <map>
#include <string>
#include <vector>

template<typename K, typename V>
class DefaultDict : public std::map<K, V>
{
public:
    using std::map<K,V>::map;
    std::function<V()> default_factory;

    DefaultDict(std::function<V()> def = nullptr): default_factory(def) {}

    V& operator[](const K& key) {
        auto it = this->find(key);
        if(it == this->end()) {
            if (default_factory) {
                (*this)[key] = default_factory();
            }
        }
        return std::map<K,V>::operator[](key);
    }
};

TEST(DefaultDictTest, test_dump_defaultdict) {
    DefaultDict<std::string, std::string> dd([]{return std::string("");});
    dd["a"] = "A";
    dd["b"] = "B";
    std::map<std::string, std::string> dumped(dd.begin(), dd.end());
    std::map<std::string, std::string> expected{{"a", "A"}, {"b", "B"}};
    EXPECT_EQ(dumped, expected);
}

TEST(DefaultDictTest, test_load_defaultdict) {
    DefaultDict<std::string, std::vector<int>> dd([]{return std::vector<int>{};});
    dd["a"] = {1,2,3};
    std::map<std::string, std::vector<int>> data = {{"a", {1,2,3}}};
    DefaultDict<std::string, std::vector<int>> loaded([]{return std::vector<int>{};});
    loaded = dd;
    EXPECT_EQ(loaded, dd);
    EXPECT_TRUE(loaded.default_factory != nullptr);
}

TEST(DefaultDictTest, test_load_default_dict_without_args) {
    DefaultDict<std::string, std::vector<int>> dd;
    dd["a"] = {1,2,3};
    auto loaded = dd;
    EXPECT_EQ(dd.default_factory, loaded.default_factory);
}