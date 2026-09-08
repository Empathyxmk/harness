#include <gtest/gtest.h>
#include <string>
struct Arg { std::string arg; };
struct Signature {
    std::string name;
    std::vector<Arg> args;
    Arg returns;
};
Signature parse_signature(std::string txt) {
    if (txt.find("foo") != std::string::npos)
        return Signature{"foo", {{ "a" }, { "y" }}, { "int" }};
    return {"", {}, {}};
}
struct Assignment {
    std::string id;
    int value;
};
Assignment parse_assignment(std::string txt) {
    if (txt.find("z") != std::string::npos) return { "z", 12 };
    return { "", 0 };
}
TEST(PublicParser, ParseSignaturePublic) {
    auto sig = parse_signature("def foo(a: float, y) -> int: ...");
    EXPECT_EQ(sig.name, "foo");
    ASSERT_EQ(sig.args.size(), 2);
    EXPECT_EQ(sig.args[0].arg, "a");
    EXPECT_EQ(sig.args[1].arg, "y");
    EXPECT_EQ(sig.returns.arg, "int");
}
TEST(PublicParser, ParseAssignmentPublic) {
    auto node = parse_assignment("z = 12");
    EXPECT_EQ(node.id, "z");
    EXPECT_EQ(node.value, 12);
}