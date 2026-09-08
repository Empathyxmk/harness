using Xunit;
using HackerrankSolutions;

public class StringsMakingAnagramsPublicTests
{
    [Fact]
    public void TestNoOverlap()
    {
        string s1 = "abcxyz";
        string s2 = "defuvw";
        Assert.Equal(12, StringsMakingAnagrams.NumberNeeded(s1, s2));
    }

    [Fact]
    public void TestPartialOverlap()
    {
        string s1 = "banana";
        string s2 = "bandana";
        Assert.Equal(2, StringsMakingAnagrams.NumberNeeded(s1, s2));
    }

    [Fact]
    public void TestOneEmpty()
    {
        string s1 = "laptop";
        string s2 = "";
        Assert.Equal(6, StringsMakingAnagrams.NumberNeeded(s1, s2));
    }
}