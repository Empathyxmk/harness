#include <gtest/gtest.h>
#include <vector>
#include <string>

// Dummy stubs for demonstration.
// These would be replaced with actual implementations in a real project.

class Image {
public:
    std::vector<unsigned char> data;
    Image(const std::vector<unsigned char>& d) : data(d) {}
};

TEST(TestGetImage, GetImage) {
    std::vector<unsigned char> img_data = {0,1,2,3};
    Image response(img_data);
    ASSERT_EQ(response.data.size(), 4);
}