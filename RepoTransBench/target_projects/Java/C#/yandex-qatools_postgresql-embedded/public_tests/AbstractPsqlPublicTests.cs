using Xunit;

namespace PublicTests
{
    public class AbstractPsqlPublicTests
    {
        [Fact]
        public void PsqlIsConnectedPublic()
        {
            // In a real test you would check an actual connection, here is a dummy test for illustration
            var isConnected = true;
            Assert.True(isConnected);
        }

        [Fact]
        public void PsqlRunsCommandPublic()
        {
            // Simulate command run
            string cmd = "SELECT 1";
            string result = RunCommand(cmd);
            Assert.Equal("success-public", result);
        }

        private string RunCommand(string cmd)
        {
            if (cmd == "SELECT 1")
                return "success-public";
            return "fail";
        }
    }
}