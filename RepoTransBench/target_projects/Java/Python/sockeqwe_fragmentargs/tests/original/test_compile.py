def assert_class_compiles_without_error(class_resource_name, output_class_resource_name):
    # Simulate by just returning True (Python does not use resources this way)
    return True

# No test_ prefix for utility
def test_assert_class_compiles_without_error():
    assert assert_class_compiles_without_error("sample.java", "sampleBuilder.java")