#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <algorithm>

// Minimal stubs to simulate owncloud/owncloud.py logic
namespace oc {
    bool _is_file(const std::string& path) {
        if (path.empty()) return false;
        if (path.back() == '/') return false;
        size_t pos = path.find_last_of("/");
        std::string fname = (pos==std::string::npos) ? path : path.substr(pos+1);
        return fname.find('.') != std::string::npos;
    }
    std::string _strip_trailing_slash(const std::string& path) {
        if (path.empty()) return path;
        if (path == "/") return "";
        if (path.back() == '/') return path.substr(0, path.length()-1);
        return path;
    }
    std::vector<std::pair<std::string, std::map<std::string, std::string>>> _parse_dav_response(const std::string& xml) {
        std::vector<std::pair<std::string, std::map<std::string, std::string>>> result;
        if (xml.find("<d:response>") == std::string::npos) return {};
        size_t start = 0;
        while ((start = xml.find("<d:response>", start)) != std::string::npos) {
            size_t href1 = xml.find("<d:href>", start) + 9;
            size_t href2 = xml.find("</d:href>", start);
            std::string href = xml.substr(href1, href2-href1);
            size_t clen1 = xml.find("<d:getcontentlength>", start);
            std::string clen = "";
            if (clen1 != std::string::npos) {
                clen1 += 20;
                size_t clen2 = xml.find("</d:getcontentlength>", clen1);
                clen = xml.substr(clen1, clen2-clen1);
            }
            std::map<std::string, std::string> props;
            if (!clen.empty()) props["getcontentlength"] = clen;
            result.emplace_back(href, props);
            start = href2;
        }
        return result;
    }
    std::string _ensure_leading_slash(const std::string& s) {
        if (s.empty()) return "/";
        if (s.front() == '/') return s;
        return "/" + s;
    }
    std::string _strip_leading_slash(const std::string& s) {
        if (s.empty()) return "";
        if (s.front() == '/') return s.substr(1);
        return s;
    }
    std::string _unicode_urlquote(const std::string& s) {
        // Percent encode all non-ascii except for '.'
        std::ostringstream oss;
        for(char c : s) {
            if ((unsigned char)c > 127) {
                oss << "%" << std::uppercase << std::hex << std::setw(2) << std::setfill('0') << (int)(unsigned char)c;
            } else {
                oss << c;
            }
        }
        return oss.str();
    }
    std::string _content_range(int a, int b, int total) {
        return "bytes " + std::to_string(a) + "-" + std::to_string(b) + "/" + std::to_string(total);
    }
    std::string _strip_prefix(const std::string& s, const std::string& prefix) {
        if (s.find(prefix) == 0) return s.substr(prefix.size());
        return s;
    }
}

// Tests correspond to Python public_tests/test_public_unit.py
TEST(PublicUnit, test_is_file_public) {
    EXPECT_TRUE(oc::_is_file("/docs/readme.md"));
    EXPECT_TRUE(oc::_is_file("song.mp3"));
    EXPECT_TRUE(oc::_is_file("/folder1/test.csv"));
    EXPECT_FALSE(oc::_is_file("/folder1/subdir/"));
    EXPECT_FALSE(oc::_is_file("/anotherdir/"));
}

TEST(PublicUnit, test_strip_trailing_slash_public) {
    EXPECT_EQ(oc::_strip_trailing_slash("/tmp/testcase/"), "/tmp/testcase");
    EXPECT_EQ(oc::_strip_trailing_slash("/foo/bar/long/path/"), "/foo/bar/long/path");
    EXPECT_EQ(oc::_strip_trailing_slash("/bar/xx"), "/bar/xx");
    EXPECT_EQ(oc::_strip_trailing_slash("/"), "");
}

TEST(PublicUnit, test_parse_dav_response_valid_public) {
    std::string xml_response = R"(<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:">
      <d:response>
        <d:href>/remote.php/dav/files/bar/doc.md</d:href>
        <d:propstat>
          <d:prop>
            <d:getcontentlength>999</d:getcontentlength>
          </d:prop>
        </d:propstat>
      </d:response>
      <d:response>
        <d:href>/remote.php/dav/files/bar/image.jpeg</d:href>
        <d:propstat>
          <d:prop>
            <d:getcontentlength>2048</d:getcontentlength>
          </d:prop>
        </d:propstat>
      </d:response>
    </d:multistatus>
    )";
    auto result = oc::_parse_dav_response(xml_response);
    ASSERT_EQ(result.size(), 2u);
    EXPECT_EQ(result[0].first, "/remote.php/dav/files/bar/doc.md");
    EXPECT_EQ(result[0].second.at("getcontentlength"), "999");
    EXPECT_EQ(result[1].first, "/remote.php/dav/files/bar/image.jpeg");
    EXPECT_EQ(result[1].second.at("getcontentlength"), "2048");
}

TEST(PublicUnit, test_parse_dav_response_empty_public) {
    std::string xml_response = R"(<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:"></d:multistatus>
    )";
    auto result = oc::_parse_dav_response(xml_response);
    EXPECT_TRUE(result.empty());
}

TEST(PublicUnit, test_ensure_leading_slash_public) {
    EXPECT_EQ(oc::_ensure_leading_slash("new/path"), "/new/path");
    EXPECT_EQ(oc::_ensure_leading_slash("/starts/with/slash"), "/starts/with/slash");
    EXPECT_EQ(oc::_ensure_leading_slash(""), "/");
}

TEST(PublicUnit, test_strip_leading_slash_public) {
    EXPECT_EQ(oc::_strip_leading_slash("/strip/me"), "strip/me");
    EXPECT_EQ(oc::_strip_leading_slash("already/stripped"), "already/stripped");
    EXPECT_EQ(oc::_strip_leading_slash("/"), "");
}

TEST(PublicUnit, test_unicode_urlquote_public) {
    std::string url = oc::_unicode_urlquote("日本語ファイル.txt");
    EXPECT_EQ(url, "%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB.txt"); // works for stub logic
    std::string url2 = oc::_unicode_urlquote("plik_żółw.txt");
    EXPECT_EQ(url2, "plik_%C5%BC%C3%B3%C5%82w.txt");
}

TEST(PublicUnit, test_content_range_utility_public) {
    EXPECT_EQ(oc::_content_range(10, 29, 120), "bytes 10-29/120");
    EXPECT_EQ(oc::_content_range(200, 400, 1000), "bytes 200-400/1000");
    EXPECT_EQ(oc::_content_range(3, 7, 9), "bytes 3-7/9");
}

TEST(PublicUnit, test_strip_prefix_public) {
    EXPECT_EQ(oc::_strip_prefix("/api/v3/data", "/api/v3/"), "data");
    EXPECT_EQ(oc::_strip_prefix("api/v1/resource", "api/v1/"), "resource");
    EXPECT_EQ(oc::_strip_prefix("foo/bar", "foo/"), "bar");
    EXPECT_EQ(oc::_strip_prefix("nomatch", "x/"), "nomatch");
}