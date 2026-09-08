#include "gtest/gtest.h"
#include "lib/sensei.h"
#include <regex>
#include <vector>
#include <tuple>
#include <string>

class AboutParrots {};
class AboutLumberjacks {};
class AboutTennis {};
class AboutTheKnightsWhoSayNi {};
class AboutMrGumby {};
class AboutMessiahs {};
class AboutGiantFeet {};
class AboutTrebuchets {};
class AboutFreemasons {};

const std::string error_assertion_with_message =
    "Traceback (most recent call last):\n"
    "  File \"/Users/Greg/hg/python_koans/koans/about_exploding_trousers.py\", line 43, in test_durability\n"
    "    self.assertEqual(\"Steel\",\"Lard\", \"Another fine mess you've got me into Stanley...\")\n"
    "AssertionError: Another fine mess you've got me into Stanley...";

const std::string error_assertion_equals =
    "\nTraceback (most recent call last):\n"
    "  File \"/Users/Greg/hg/python_koans/koans/about_exploding_trousers.py\", line 49, in test_math\n"
    "    self.assertEqual(4,99)\n"
    "AssertionError: 4 != 99\n";
const std::string error_assertion_true =
    "Traceback (most recent call last):\n"
    "  File \"/Users/Greg/hg/python_koans/koans/about_armories.py\", line 25, in test_weoponary\n"
    "    self.assertTrue(\"Pen\" > \"Sword\")\n"
    "AssertionError\n";
const std::string error_mess =
    "Traceback (most recent call last):\n"
    "  File \"contemplate_koans.py\", line 5, in <module>\n"
    "    from runner.mountain import Mountain\n"
    "  File \"/Users/Greg/hg/python_koans/runner/mountain.py\", line 7, in <module>\n"
    "    import path_to_enlightenment\n"
    "  File \"/Users/Greg/hg/python_koans/runner/path_to_enlightenment.py\", line 8, in <module>\n"
    "    from koans import *\n"
    "  File \"/Users/Greg/hg/python_koans/koans/about_asserts.py\", line 20\n"
    "    self.assertTrue(eoe\"Pen\" > \"Sword\", \"nhnth\")\n"
    "                           ^\n"
    "SyntaxError: invalid syntax";

const std::string error_with_list =
    "Traceback (most recent call last):\n"
    "  File \"/Users/Greg/hg/python_koans/koans/about_armories.py\", line 84, in test_weoponary\n"
    "    self.assertEqual([1, 9], [1, 2])\n"
    "AssertionError: Lists differ: [1, 9] != [1, 2]\n"
    "\n"
    "First differing element 1:\n"
    "9\n"
    "2\n"
    "\n"
    "- [1, 9]\n"
    "?     ^\n"
    "\n"
    "+ [1, 2]\n"
    "?     ^\n";

TEST(TestSensei, ItSuccessesOnlyCountIfPassesAreCurrentlyAllowed) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.setPassesCountMock(new Mock());
    s.addSuccess(new Mock());
    EXPECT_TRUE(s.passesCountCalled());
}

TEST(TestSensei, ItIncreasesThePassesOnEverySuccess) {
    Sensei s(new WritelnDecorator(new Mock()));
    int pass_count = s.pass_count();
    s.addSuccess(new Mock());
    EXPECT_EQ(pass_count+1, s.pass_count());
}

TEST(TestSensei, NothingIsReturnedAsSortedResultIfThereAreNoFailures) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures().clear();
    EXPECT_FALSE(s.sortFailures("AboutLife").has_value());
}

TEST(TestSensei, NothingIsReturnedAsSortedResultIfThereAreNoRelevantFailures) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures() = {
        {AboutTheKnightsWhoSayNi(), "File 'about_the_knights_whn_say_ni.py', line 24"},
        {AboutMessiahs(), "File 'about_messiahs.py', line 43"},
        {AboutMessiahs(), "File 'about_messiahs.py', line 844"}
    };
    EXPECT_FALSE(s.sortFailures("AboutLife").has_value());
}

TEST(TestSensei, NothingIsReturnedAsSortedResultIfThereAre3ShuffledResults) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures() = {
        {AboutTennis(), "File 'about_tennis.py', line 299"},
        {AboutTheKnightsWhoSayNi(), "File 'about_the_knights_whn_say_ni.py', line 24"},
        {AboutTennis(), "File 'about_tennis.py', line 30"},
        {AboutMessiahs(), "File 'about_messiahs.py', line 43"},
        {AboutTennis(), "File 'about_tennis.py', line 2"},
        {AboutMrGumby(), "File 'about_mr_gumby.py', line odd"},
        {AboutMessiahs(), "File 'about_messiahs.py', line 844"}
    };
    auto result = s.sortFailures("AboutTennis");
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(3, result->size());
    EXPECT_EQ(2, std::get<0>((*result)[0]));
    EXPECT_EQ(30, std::get<0>((*result)[1]));
    EXPECT_EQ(299, std::get<0>((*result)[2]));
}

TEST(TestSensei, WillChooseNotFindAnythingWithNonStandardErrorTraceString) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures() = {
        {AboutMrGumby(), "File 'about_mr_gumby.py', line MISSING"}
    };
    EXPECT_FALSE(s.sortFailures("AboutMrGumby").has_value());
}

TEST(TestSensei, WillChooseCorrectFirstResultWithLines9And27) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures() = {
        {AboutTrebuchets(), "File 'about_trebuchets.py', line 27"},
        {AboutTrebuchets(), "File 'about_trebuchets.py', line 9"},
        {AboutTrebuchets(), "File 'about_trebuchets.py', line 73v"}
    };
    EXPECT_EQ("File 'about_trebuchets.py', line 9", s.firstFailure()->second);
}

TEST(TestSensei, WillChooseCorrectFirstResultWithMultilineTestClasses) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures() = {
        {AboutGiantFeet(), "File 'about_giant_feet.py', line 999"},
        {AboutGiantFeet(), "File 'about_giant_feet.py', line 44"},
        {AboutFreemasons(), "File 'about_freemasons.py', line 1"},
        {AboutFreemasons(), "File 'about_freemasons.py', line 11"}
    };
    EXPECT_EQ("File 'about_giant_feet.py', line 44", s.firstFailure()->second);
}

TEST(TestSensei, ErrorReportFeaturesAStackDump) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.setScrapeInterestingStackDumpMock(new Mock());
    s.setFirstFailureMock(new Mock());
    s.firstFailureSetReturnValue({new Mock(),"FAILED"});
    s.errorReport();
    EXPECT_TRUE(s.scrapeInterestingStackDumpCalled());
}

TEST(TestSensei, ScrapingTheAssertionErrorWithNothingGivesBlankBack) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("", s.scrapeAssertionError(""));
}

TEST(TestSensei, ScrapingTheAssertionErrorWithMessagedAssert) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("  AssertionError: Another fine mess you've got me into Stanley...",
              s.scrapeAssertionError(error_assertion_with_message));
}

TEST(TestSensei, ScrapingTheAssertionErrorWithAssertEquals) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("  AssertionError: 4 != 99",
              s.scrapeAssertionError(error_assertion_equals));
}

TEST(TestSensei, ScrapingTheAssertionErrorWithAssertTrue) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("  AssertionError", s.scrapeAssertionError(error_assertion_true));
}

TEST(TestSensei, ScrapingTheAssertionErrorWithSyntaxError) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("  SyntaxError: invalid syntax", s.scrapeAssertionError(error_mess));
}

TEST(TestSensei, ScrapingTheAssertionErrorWithListError) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("  AssertionError: Lists differ: [1, 9] != [1, 2]\n\n  First differing element 1:\n  9\n  2\n\n  - [1, 9]\n  ?     ^\n\n  + [1, 2]\n  ?     ^",
              s.scrapeAssertionError(error_with_list));
}

TEST(TestSensei, ScrapingANonExistentStackDumpGivesYouNothing) {
    Sensei s(new WritelnDecorator(new Mock()));
    EXPECT_EQ("", s.scrapeInterestingStackDump(""));
}

TEST(TestSensei, IfThereAreNoFailuresSayTheFinalZenlikeRemark) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.failures_ptr() = nullptr;
    std::string words = s.say_something_zenlike();
    std::regex rex("Spanish Inquisition");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, IfThereAre0SuccessesWillSayTheFirstZenOfPythonKoans) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_pass_count(0);
    s.failures_ptr() = new Mock(); // marks as not null
    std::string words = s.say_something_zenlike();
    std::regex rex("Beautiful is better than ugly");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, IfThereIs1SuccessWillSaySecondZenOfPythonKoans) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_pass_count(1);
    s.failures_ptr() = new Mock();
    std::string words = s.say_something_zenlike();
    std::regex rex("Explicit is better than implicit");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, IfThereAre10SuccessesWillSaySixthZenOfPythonKoans) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_pass_count(10);
    s.failures_ptr() = new Mock();
    std::string words = s.say_something_zenlike();
    std::regex rex("Sparse is better than dense");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, IfThereAre36SuccessesWillSayFinalZenOfPythonKoans) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_pass_count(36);
    s.failures_ptr() = new Mock();
    std::string words = s.say_something_zenlike();
    std::regex rex("Namespaces are one honking great idea");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, IfThereAre37SuccessesWillSayFirstZenOfPythonKoansAgain) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_pass_count(37);
    s.failures_ptr() = new Mock();
    std::string words = s.say_something_zenlike();
    std::regex rex("Beautiful is better than ugly");
    EXPECT_TRUE(std::regex_search(words, rex));
}

TEST(TestSensei, TotalLessonsReturns7IfThereAre7Lessons) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_filter_all_lessons([&](){ return std::vector<int>{1,2,3,4,5,6,7}; });
    EXPECT_EQ(7, s.total_lessons());
}

TEST(TestSensei, TotalLessonsReturn0IfAllLessonsIsNone) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_filter_all_lessons([&](){ return std::vector<int>{}; });
    EXPECT_EQ(0, s.total_lessons());
}

TEST(TestSensei, TotalKoansReturn43IfThereAre43TestCases) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.tests().set_count_test_cases_return(43);
    EXPECT_EQ(43, s.total_koans());
}

TEST(TestSensei, FilterAllLessonsWillDiscoverTestClassesIfNoneHaveBeenDiscoveredYet) {
    Sensei s(new WritelnDecorator(new Mock()));
    s.set_all_lessons(0);
    auto result = s.filter_all_lessons();
    EXPECT_GT(result.size(), 10);
    EXPECT_GT(s.all_lessons().size(), 10);
}