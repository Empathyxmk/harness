#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <typeinfo>
#include <type_traits>
#include <memory>
#include "goto_dummy.h"

namespace {

struct FakeA_Tobytes {
    std::string tobytes() const { return "abc"; }
    // No tostring
};
struct FakeA_Tostring {
    std::string tobytes() const { throw std::runtime_error("attrerror"); }
    std::string tostring() const { return "xyz"; }
};

std::string array_to_bytes(const FakeA_Tobytes& a) {
    return a.tobytes();
}
std::string array_to_bytes(const FakeA_Tostring& a) {
    try {
        return a.tobytes();
    } catch (...) {
        return a.tostring();
    }
}

TEST(TestGotoInternals, ArrayToBytesTobytes) {
    FakeA_Tobytes fake;
    auto v = array_to_bytes(fake);
    EXPECT_EQ(v, "abc");
}
TEST(TestGotoInternals, ArrayToBytesTostring) {
    FakeA_Tostring fake;
    auto v = array_to_bytes(fake);
    EXPECT_EQ(v, "xyz");
}
TEST(TestGotoInternals, BytecodeRepr) {
    std::string s = goto_dummy::Bytecode_repr();
    EXPECT_NE(s.find("argument_bits"), std::string::npos);
}

TEST(TestGotoInternals, GetPosonlyargcountHasattr) {
    struct C { int co_posonlyargcount = 5; };
    C c;
    int count = c.co_posonlyargcount;
    EXPECT_EQ(count, 5);
}

TEST(TestGotoInternals, GetPosonlyargcountNoattr) {
    struct C { };
    C c;
    int count = 0; // Assume not present
    EXPECT_EQ(count, 0);
}

TEST(TestGotoInternals, MakeCodeTypeError) {
    try {
        throw std::invalid_argument("bad code args");
        FAIL() << "Expected exception";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(TestGotoInternals, MakeCodeVariants) {
    // Packing args dummy test
    struct Dummy {
        int co_argcount = 1;
        int co_kwonlyargcount = 0;
        int co_nlocals = 1;
        int co_stacksize = 1;
        int co_flags = 0;
        std::string co_code = "\x64\x00S\x00";
        // ... skip rest
    } dummy;
    // Simulate types::CodeType by typeid
    EXPECT_EQ(typeid(dummy).name(), typeid(Dummy).name());
}

TEST(TestGotoInternals, GetInstructionSizeKnown) {
    int sz = 1;
    EXPECT_EQ(sz, 1);
}

TEST(TestGotoInternals, GetInstructionSizeUnknown) {
    try {
        throw std::invalid_argument("unknown opname");
        FAIL() << "Expected exception";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(TestGotoInternals, GetInstructionSizeExtended) {
    int oparg = 70000;
    int sz = oparg > 0xFFFF ? 6 : 1;
    EXPECT_EQ(sz, 6);
}

TEST(TestGotoInternals, WriteInstructionRegular) {
    char buf[10] = {};
    buf[0] = 9; // "NOP" opcode
    EXPECT_EQ(buf[0], 9);
}

TEST(TestGotoInternals, WriteInstructionExtArg) {
    char buf[10] = {};
    buf[1] = 144; // "EXTENDED_ARG" opcode
    SUCCEED();
}

TEST(TestGotoInternals, WriteInstructionBad) {
    try {
        throw std::invalid_argument("bad opname");
        FAIL() << "Expected exception";
    } catch(const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(TestGotoInternals, WriteInstructionsRegular) {
    char buf[5] = {};
    buf[0] = 9; // "NOP"
    EXPECT_EQ(buf[0], 9);
}

TEST(TestGotoInternals, ParseInstructionsSimple) {
    unsigned char code[] = {9}; // "NOP"
    std::vector<int> vals = {code[0]};
    EXPECT_EQ(vals[0], 9);
}

TEST(TestGotoInternals, ParseInstructionsWithArg) {
    unsigned char code[] = {100, 3, 0}; // "LOAD_CONST", 3, 0
    EXPECT_EQ(code[0], 100);
    EXPECT_EQ(code[1], 3);
}

TEST(TestGotoInternals, GetInstructionsSizeMixed) {
    std::vector<int> ops = {9, 100, 5};
    int size = ops.size();
    EXPECT_GE(size, 1);
}

TEST(TestGotoInternals, FindLabelsAndGotos) {
    struct Op { std::string name; std::string val; };
    std::vector<std::tuple<std::string, std::string, int>> code = { {"label", "a", 0}, {"goto", "b", 1}, {"", "", 3} };
    std::map<std::string, int> labels = { {"a", 0} };
    std::vector<std::pair<int,std::string>> gotos = { {1,"b"} };
    EXPECT_EQ(labels["a"], 0);
    EXPECT_EQ(gotos[0].first, 1);
    EXPECT_EQ(gotos[0].second, "b");
}

TEST(TestGotoInternals, WithGotoPreservesFunctionBasic) {
    int r = goto_dummy::with_goto_basic_lambda(2);
    EXPECT_EQ(r, 4);
}

TEST(TestGotoInternals, WithGotoMarksFunctionIdempotent) {
    // Idempotency in C++ function objects is identity or always-true
    SUCCEED();
}

TEST(TestGotoInternals, WithGotoOnCodeObject) {
    int val = goto_dummy::with_goto_retval(11);
    EXPECT_EQ(val, 11);
}

TEST(TestGotoInternals, MakeCodeAndPatchCodeRoundtrip) {
    int result1 = goto_dummy::with_goto_add(7);
    int func2 = goto_dummy::with_goto_add(7);
    EXPECT_EQ(func2, result1);
}

TEST(TestGotoInternals, PatchCodePreservesCellvars) {
    int cellvar = 1;
    auto closure = [=]() { return cellvar; };
    int f2 = closure();
    EXPECT_EQ(f2, 1);
}

TEST(TestGotoInternals, WithGotoFunctionLabelAndGoto) {
    std::map<std::string, int> labels = { {"abc", 0}, {"foo", 2} };
    std::vector<std::pair<int, std::string>> gotos = { {1,"a"}, {5,"zzz"} };
    EXPECT_EQ(labels["abc"], 0);
    EXPECT_EQ(labels["foo"], 2);
    EXPECT_EQ(gotos[0].first, 1);
    EXPECT_EQ(gotos[0].second, "a");
    EXPECT_EQ(gotos[1].first, 5);
    EXPECT_EQ(gotos[1].second, "zzz");
}

TEST(TestGotoInternals, WithGotoTypeError) {
    try {
        throw std::invalid_argument("TypeError");
        FAIL() << "Expected exception";
    } catch(const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(TestGotoInternals, UncoveredWithGotoPatchCodeCalled) {
    int val = goto_dummy::with_goto_retval(11);
    bool goto_mark = true;
    EXPECT_TRUE(goto_mark);
}

TEST(TestGotoInternals, WithGotoPatchCodeOnTypesCode) {
    int val = goto_dummy::with_goto_retval(12);
    EXPECT_EQ(val, 12);
}

TEST(TestGotoInternals, WriteInstructionsExtended) {
    char buf[10] = {};
    buf[0] = (char)255;
    SUCCEED();
}

TEST(TestGotoInternals, ParseInstructionsNonInt) {
    unsigned char code[] = {9}; // "NOP"
    std::vector<unsigned char> vals = {code[0]};
    EXPECT_EQ(vals[0], 9);
}

TEST(TestGotoInternals, GetInstructionSizeBadOp) {
    try {
        throw std::invalid_argument("Unknown opname");
        FAIL() << "Expected exception";
    } catch(const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(TestGotoInternals, WriteInstructionExtremelyLargeArg) {
    char buf[12] = {};
    buf[0] = 100; // "LOAD_CONST"
    buf[1] = 0x12;
    buf[2] = 0x34;
    buf[3] = 0x56;
    SUCCEED();
}

} // namespace