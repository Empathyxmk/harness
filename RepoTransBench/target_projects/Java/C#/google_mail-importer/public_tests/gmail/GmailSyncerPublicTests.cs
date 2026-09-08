using System.Collections.Generic;
using Moq;
using Xunit;

namespace GoogleMailImporter.PublicTests.Gmail
{
    public class GmailSyncerPublicTests
    {
        [Fact]
        public void TestDifferentInitTriggersSyncPublic()
        {
            var syncerMock = new Mock<IGmailSyncer>();
            syncerMock.Object.Init();
            syncerMock.Verify(x => x.Init());
            syncerMock.Object.Sync(new List<object>());
            syncerMock.Verify(x => x.Sync(It.Is<List<object>>(l => l.Count == 0)));
        }
    }

    public interface IGmailSyncer
    {
        void Init();
        void Sync(IList<object> messages);
    }
}