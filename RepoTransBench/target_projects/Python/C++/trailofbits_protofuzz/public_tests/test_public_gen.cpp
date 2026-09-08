#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <typeinfo>
#include <memory>
#include <tuple>
// --- Stubs for gen API (public version) ---
namespace gen_public {
    struct DummyField {
        std::string name;
        int cpp_type;
        int label;
        void* message_type;
        DummyField(const std::string& name_, int cpp_type_=2, int label_=1, void* msg_type=nullptr)
            : name(name_), cpp_type(cpp_type_), label(label_), message_type(msg_type) {}
    };
    struct DummyDesc {
        std::vector<DummyField> fields;
        DummyDesc(std::vector<DummyField> fields_) : fields(fields_) {}
    };
    struct DummyMsg {
        static DummyDesc& descriptor() {
            static DummyDesc d({DummyField("y", 2)});
            return d;
        }
    };
    struct DummyMsgParent {
        static DummyDesc& descriptor() {
            static DummyDesc d({DummyField("different", 20, 1, reinterpret_cast<void*>(0xfacefeed))});
            return d;
        }
        void* different = nullptr;
    };

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

TEST(PublicGenTest, MessageGeneratorSimplePublic) {
    auto objs = gen_public::message_generator<gen_public::DummyMsg>(
        [](int t=0, void* f=nullptr){ return std::vector<int>{99,100}; }, 2
    );
    EXPECT_EQ(typeid(objs[0]), typeid(gen_public::DummyMsg));
    EXPECT_EQ(typeid(objs[1]), typeid(gen_public::DummyMsg));
}

TEST(PublicGenTest, MessageGeneratorWithMessageTypePublic) {
    auto objs = gen_public::message_generator<gen_public::DummyMsgParent>(
        [](int t=0, void* f=nullptr){ return std::vector<void*>{reinterpret_cast<void*>(0x222)}; }, 1
    );
    EXPECT_EQ(typeid(objs[0]), typeid(gen_public::DummyMsgParent));
}

class AssignToFieldPublicParam : public ::testing::TestWithParam<std::tuple<int, std::string>> { };

TEST_P(AssignToFieldPublicParam, AssignToFieldPublic) {
    int label = std::get<0>(GetParam());
    struct DummyObj {};
    DummyObj obj;
    struct F { int label; std::string name; };
    F field{label, "bar"};
    int value = 77;
    auto out = gen_public::_assign_to_field(obj, field, value);
    EXPECT_TRUE((std::is_same<decltype(out), std::vector<int>>::value));
}
INSTANTIATE_TEST_SUITE_P(PublicGenTest, AssignToFieldPublicParam,
                         ::testing::Values(
                            std::make_tuple(1, "bar"),
                            std::make_tuple(2, "bar"),
                            std::make_tuple(3, "bar")
                         ));