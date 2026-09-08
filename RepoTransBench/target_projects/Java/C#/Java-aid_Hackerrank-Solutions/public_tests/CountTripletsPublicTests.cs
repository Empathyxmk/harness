using Xunit;
using HackerrankSolutions;
using System.Collections.Generic;

public class CountTripletsPublicTests
{
    [Fact]
    public void TestCaseRatio2()
    {
        List<long> arr = new List<long> { 2L, 4L, 8L, 16L, 32L, 4L, 8L };
        long r = 2L;
        Assert.Equal(6, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestCaseRatio3()
    {
        List<long> arr = new List<long> { 9L, 27L, 81L, 243L, 3L, 9L, 27L };
        long r = 3L;
        Assert.Equal(6, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestCaseNoTriplets()
    {
        List<long> arr = new List<long> { 1L, 2L, 5L, 7L };
        long r = 3L;
        Assert.Equal(0, CountTriplets.CountTripletsMethod(arr, r));
    }
}