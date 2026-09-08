#include <gtest/gtest.h>
#include "injector.h"
#include <memory>
#include <typeindex>
#include <unordered_set>
#include <functional>

using namespace injector_ns;

TEST(PublicInjectorTest, SingletonBindingUniqueValue) {
    class Alpha {};
    class Beta {};

    Injector inj;
    std::shared_ptr<Alpha> alpha_obj = std::make_shared<Alpha>();
    std::shared_ptr<Beta> beta_obj = std::make_shared<Beta>();
    inj.bind_instance<Alpha>(alpha_obj);
    inj.bind_instance<Beta>(beta_obj);
    auto a1 = inj.get_instance<Alpha>();
    auto b1 = inj.get_instance<Beta>();
    ASSERT_TRUE(a1 != nullptr);
    ASSERT_TRUE(b1 != nullptr);
    ASSERT_EQ(alpha_obj.get(), a1.get());
    ASSERT_EQ(beta_obj.get(), b1.get());
    // Re-get to check they are the same instance
    ASSERT_EQ(alpha_obj.get(), inj.get_instance<Alpha>().get());
    ASSERT_EQ(beta_obj.get(), inj.get_instance<Beta>().get());
}

TEST(PublicInjectorTest, InjectDecoratorWithPrimitive) {
    // Simulate decorator as just invoking the function
    auto provide = []() -> int {
        return 77;
    };
    ASSERT_EQ(call_with_injection(provide), 77);
}

TEST(PublicInjectorTest, ProviderReuseTypes) {
    class Foo {};
    Injector inj;
    std::shared_ptr<Foo> foo_obj = std::make_shared<Foo>();
    inj.bind_instance<Foo>(foo_obj);
    auto foo1 = inj.get_instance<Foo>();
    auto foo2 = inj.get_instance<Foo>();
    ASSERT_EQ(foo1.get(), foo2.get());
}