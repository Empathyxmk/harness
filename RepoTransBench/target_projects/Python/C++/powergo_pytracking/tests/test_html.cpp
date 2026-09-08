#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include "pytracking/tracking.h"
#include "pytracking/html.h"
#include "tests/test_pytracking_utils.h"
#include "util/html_parser.h" // (hypothetical simple HTML/XML parser)

using namespace pytracking;

// Reuse all globals for config/data from test_pytracking

const std::string TEST_HTML_EMAIL =
R"(<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"></meta>
<head>
</head>
<body>
<h1>Hello World Some éàù and &eacute; entities.</h1>
<p>
<a href="http://www.example.com/foo/?question=response">This is an inline link
</a> with some text.
</p>
<p>
<a href="mailto:bob@bob.com">Mail to Bob!</a>
</p>
<ul>
<li><a href="http://www.domain2.com">
<img src="http://www.test.com/test.jpg"></a></li>
</ul>
</body>
</html>
)";

std::map<std::string, util::Any> DEFAULT_SETTINGS = {
    {"webhook_url", DEFAULT_WEBHOOK_URL},
    {"base_open_tracking_url", DEFAULT_BASE_OPEN_TRACKING_URL},
    {"base_click_tracking_url", DEFAULT_BASE_CLICK_TRACKING_URL},
    {"default_metadata", DEFAULT_DEFAULT_METADATA}
};

void TestClickTracking(const util::HtmlDoc& tree) {
    auto links = tree.xpath("//a");
    std::string first_link_url_path = get_click_tracking_url_path(
        links[0]->attrib["href"], DEFAULT_SETTINGS
    );
    auto click_result = get_click_tracking_result(
        first_link_url_path, DEFAULT_SETTINGS
    );
    EXPECT_EQ(click_result.metadata, EXPECTED_METADATA);
    EXPECT_EQ(click_result.tracked_url.value(), "http://www.example.com/foo/?question=response");

    EXPECT_EQ(links[1]->attrib["href"], "mailto:bob@bob.com");

    std::string second_link_url_path = get_click_tracking_url_path(
        links[2]->attrib["href"], DEFAULT_SETTINGS
    );
    auto click_result2 = get_click_tracking_result(
        second_link_url_path, DEFAULT_SETTINGS
    );
    EXPECT_EQ(click_result2.metadata, EXPECTED_METADATA);
    EXPECT_EQ(click_result2.tracked_url.value(), "http://www.domain2.com");
}

void TestOpenTracking(const util::HtmlDoc& tree) {
    auto pixel_img = tree.xpath("//img").back();
    auto open_url_path = get_open_tracking_url_path(
        pixel_img->attrib["src"], DEFAULT_SETTINGS
    );
    auto open_result = get_open_tracking_result(
        open_url_path, DEFAULT_SETTINGS
    );
    EXPECT_EQ(open_result.metadata, EXPECTED_METADATA);
}

TEST(Html, AdaptHtmlFull) {
    std::string new_html = tracking_html::adapt_html(
        TEST_HTML_EMAIL, DEFAULT_METADATA, DEFAULT_SETTINGS
    );
    util::HtmlDoc tree = util::HtmlDoc::FromString(new_html);
    TestOpenTracking(tree);
    TestClickTracking(tree);

    EXPECT_NE(new_html.find("<!DOCTYPE html>"), std::string::npos);
    EXPECT_NE(new_html.find("<meta charset=\"UTF-8\">"), std::string::npos);
}

TEST(Html, AdaptHtmlClickOnly) {
    std::string new_html = tracking_html::adapt_html(
        TEST_HTML_EMAIL, DEFAULT_METADATA, DEFAULT_SETTINGS, false, true
    );
    util::HtmlDoc tree = util::HtmlDoc::FromString(new_html);
    EXPECT_EQ(tree.xpath("//img").size(), 1);
    TestClickTracking(tree);
}

TEST(Html, AdaptHtmlOpenOnly) {
    std::string new_html = tracking_html::adapt_html(
        TEST_HTML_EMAIL, DEFAULT_METADATA, DEFAULT_SETTINGS, true, false
    );
    util::HtmlDoc tree = util::HtmlDoc::FromString(new_html);
    TestOpenTracking(tree);

    auto links = tree.xpath("//a");
    EXPECT_EQ(links[0]->attrib["href"], "http://www.example.com/foo/?question=response");
    EXPECT_EQ(links[1]->attrib["href"], "mailto:bob@bob.com");
    EXPECT_EQ(links[2]->attrib["href"], "http://www.domain2.com");
}