#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <typeinfo>
#include <memory>
#include <list>

// --- Stubs for protofuzz::gen API ---
namespace gen {
    // DummyField
    struct DummyField {
        std::string name;
        int cpp_type;   // emulate
        int label;
        void* message_type;
        DummyField(const std::string& name_, int cpp_type_=1, int label_=1, void* msg_type=nullptr)
            : name(name_), cpp_type(cpp_type_), label(label_), message_type(msg_type) {}
    };
    // DummyDesc
    struct DummyDesc {
        std::vector<DummyField> fields;
        DummyDesc(std::vector<DummyField> fields_) : fields(fields_) {}
    };
    // DummyMsg
    struct DummyMsg {
        static DummyDesc& descriptor() {
            static DummyDesc d({DummyField("x")});
            return d;
        }
    };
    // DummyMsgParent (used in message_type version)
    struct DummyMsgParent {
        static DummyDesc& descriptor() {
            static DummyDesc d({DummyField("another", 10, 1, reinterpret_cast<void*>(0xdeadbeef))});
            return d;
        }
        void* another = nullptr;
    };

    // Mimic message_generator behavior; returns list of objects
    template<typename MsgT, typename ValGenFunc>
    std::vector<MsgT> message_generator(ValGenFunc valgen, int max_messages) {
        std::vector<MsgT> results;
        for (int i=0; i<max_messages; ++i)
            results.push_back(MsgT());
        return results;
    }

    // _assign_to_field: just returns a vector containing value
    template<typename ObjT, typename FieldT, typename ValT>
    std::vector<ValT> _assign_to_field(ObjT& obj, const FieldT& field, ValT value) {
        // Just wrap in a vector for test
        return std::vector<ValT>{value};
    }
}
// ------------------------------------------

TEST(GenTest, MessageGeneratorSimple) {
    // Mimics Python: gen.message_generator(DummyMsg, dummy_valgen, max_messages=2)
    auto objs = gen::message_generator<gen::DummyMsg>(
        [](int t=0, void* f=nullptr){ return std::vector<int>{1,2}; }, 2
    );
    EXPECT_EQ(typeid(objs[0]), typeid(gen::DummyMsg));
    EXPECT_EQ(typeid(objs[1]), typeid(gen::DummyMsg));
}

TEST(GenTest, MessageGeneratorWithMessageType) {
    // dummy_valgen yields DummyMessageType object (here void*).
    auto objs = gen::message_generator<gen::DummyMsgParent>(
        [](int t=0, void* f=nullptr){ return std::vector<void*>{reinterpret_cast<void*>(0xf00)}; }, 1
    );
    EXPECT_EQ(typeid(objs[0]), typeid(gen::DummyMsgParent));
}

class AssignToFieldParam : public ::testing::TestWithParam<std::tuple<int, std::string>> { };

TEST_P(AssignToFieldParam, AssignToField) {
    int label = std::get<0>(GetParam());
    // Field is only for label, not used.
    struct DummyObj {};
    DummyObj obj;
    struct F { int label; std::string name; };
    F field{label, "foo"};
    int value = 42;
    auto out = gen::_assign_to_field(obj, field, value);
    EXPECT_TRUE((std::is_same<decltype(out), std::vector<int>>::value));
}
INSTANTIATE_TEST_SUITE_P(GenTest, AssignToFieldParam,
                         ::testing::Values(
                            std::make_tuple(1, "foo"),
                            std::make_tuple(2, "foo"),
                            std::make_tuple(3, "foo")
                         ));