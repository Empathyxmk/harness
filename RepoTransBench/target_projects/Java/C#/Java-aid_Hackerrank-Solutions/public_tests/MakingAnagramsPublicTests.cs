using Xunit;
using HackerrankSolutions;

public class MakingAnagramsPublicTests
{
    [Fact]
    public void TestDifferentLetters()
    {
        string s1 = "game";
        string s2 = "team";
        Assert.Equal(3, MakingAnagrams.MakeAnagram(s1, s2));
    }

    [Fact]
    public void TestOneStringEmpty()
    {
        string s1 = "football";
        string s2 = "";
        Assert.Equal(8, MakingAnagrams.MakeAnagram(s1, s2));
    }

    [Fact]
    public void TestBothStringsTheSame()
    {
        string s1 = "network";
        string s2 = "network";
        Assert.Equal(0, MakingAnagrams.MakeAnagram(s1, s2));
    }
}