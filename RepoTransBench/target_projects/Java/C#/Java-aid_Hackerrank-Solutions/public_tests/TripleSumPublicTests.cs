using Xunit;
using HackerrankSolutions;
using System.Collections.Generic;

public class TripleSumPublicTests
{
    [Fact]
    public void TestPublicInput1()
    {
        Assert.Equal(5, TripleSum.Triplets(
            new[] { 2, 3, 4, 4, 7 },
            new[] { 1, 2, 5, 5 },
            new[] { 3, 3, 5, 8 }
        ));
    }

    [Fact]
    public void TestPublicInput2()
    {
        Assert.Equal(9, TripleSum.Triplets(
            new[] { 3, 4, 7, 7, 10 },
            new[] { 1, 3, 5, 7, 9 },
            new[] { 2, 3, 6, 9 }
        ));
    }
}