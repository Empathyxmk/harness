# Test executables
add_executable(original_tests
    test_channels.cpp
    test_init.cpp
    test_utilities.cpp
    test_main.cpp
)
target_include_directories(original_tests PRIVATE ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(original_tests PRIVATE slacker gtest_main)

add_test(NAME OriginalTests COMMAND original_tests)