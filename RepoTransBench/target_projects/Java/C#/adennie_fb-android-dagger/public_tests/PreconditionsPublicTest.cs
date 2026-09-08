using Xunit;
using ProjectName;

namespace PublicTests
{
    public class PreconditionsPublicTest
    {
        [Fact]
        public void TestCheckNotNullNotNullPublic()
        {
            string myString = "notNullPublic";
            Preconditions.CheckNotNull(myString, "Must not be null");
            Preconditions.CheckNotNull(myString);
            int myInt = 5;
            Preconditions.CheckNotNull(myInt);
        }

        [Fact]
        public void TestCheckNotNullNullPublic()
        {
            Assert.Throws<System.NullReferenceException>(() =>
                Preconditions.CheckNotNull(null, "Error: is null"));
        }

        [Fact]
        public void TestCheckStateTruePublic()
        {
            Preconditions.CheckState(2 > 1, "True expected");
            Preconditions.CheckState(true);
        }

        [Fact]
        public void TestCheckStateFalsePublic()
        {
            Assert.Throws<System.InvalidOperationException>(() =>
                Preconditions.CheckState(3 < 1, "Should fail"));
        }
    }
}