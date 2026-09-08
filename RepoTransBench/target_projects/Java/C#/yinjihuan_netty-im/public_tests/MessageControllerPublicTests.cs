using Xunit;
using NettyImServer.Api;
using Microsoft.AspNetCore.Mvc;

namespace NettyImServer.PublicTests
{
    public class MessageControllerPublicTests
    {
        [Fact]
        public void TestSendMessageWithDifferentContent()
        {
            var controller = new MessageController();
            string receiveId = "public-user-dest";
            string msg = "Hello from public test!";
            // Use different data than original likely did (see source, not just test)
            var response = controller.SendMessage(receiveId, msg);

            Assert.NotNull(response);
            var objectResult = response as ObjectResult ?? throw new System.Exception("Expected ObjectResult");
            Assert.Equal(200, objectResult.StatusCode);
            Assert.Contains("success", objectResult.Value.ToString(), System.StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestSendMessageWithEmptyReceiveId()
        {
            var controller = new MessageController();
            string receiveId = "";
            string msg = "Message to no one";
            var response = controller.SendMessage(receiveId, msg);

            Assert.NotNull(response);
            var objectResult = response as ObjectResult ?? throw new System.Exception("Expected ObjectResult");
            Assert.Equal(200, objectResult.StatusCode);
        }
    }
}