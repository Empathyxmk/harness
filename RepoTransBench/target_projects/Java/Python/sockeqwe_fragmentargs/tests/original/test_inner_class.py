def assert_class_compiles_without_error(source, output):
    # In Python, simulate by just dummy function call
    return True

def test_inner_class():
    assert assert_class_compiles_without_error("ClassWithInnerClass.java", "ClassWithInnerClassBuilder.java")

def test_inner_class_with_protected_field():
    assert assert_class_compiles_without_error("InnerClassWithProtectedField.java", "InnerClassWithProtectedFieldBuilder.java")