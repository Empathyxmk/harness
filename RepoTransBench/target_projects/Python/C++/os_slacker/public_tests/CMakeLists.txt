add_executable(public_tests
    test_public_channels.cpp
    test_public_init.cpp
    test_public_utilities.cpp
    test_main.cpp
)
target_include_directories(public_tests PRIVATE ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(public_tests PRIVATE slacker gtest_main)

add_test(NAME PublicTests COMMAND public_tests)