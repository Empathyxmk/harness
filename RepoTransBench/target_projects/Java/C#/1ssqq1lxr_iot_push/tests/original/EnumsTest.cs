using Xunit;

namespace OriginalTests
{
    public class EnumsTest
    {
        [Fact]
        public void TestConfirmStatusEnum()
        {
            Assert.Equal(2, System.Enum.GetValues(typeof(ProjectName.ConfirmStatus)).Length);
            Assert.Equal(ProjectName.ConfirmStatus.PUBLISH, ProjectName.ConfirmStatus.PUBLISH);
            Assert.Equal(ProjectName.ConfirmStatus.PUBREL, ProjectName.ConfirmStatus.PUBREL);
        }

        [Fact]
        public void TestProtocolEnum()
        {
            Assert.Equal(2, System.Enum.GetValues(typeof(ProjectName.ProtocolEnum)).Length);
            Assert.Equal(ProjectName.ProtocolEnum.MQTT, ProjectName.ProtocolEnum.MQTT);
            Assert.Equal(ProjectName.ProtocolEnum.WEBSOCKET, ProjectName.ProtocolEnum.WEBSOCKET);
        }

        [Fact]
        public void TestQosStatus()
        {
            Assert.Equal(3, System.Enum.GetValues(typeof(ProjectName.QosStatus)).Length);
            Assert.Equal(ProjectName.QosStatus.QOS0, ProjectName.QosStatus.QOS0);
            Assert.Equal(ProjectName.QosStatus.QOS1, ProjectName.QosStatus.QOS1);
            Assert.Equal(ProjectName.QosStatus.QOS2, ProjectName.QosStatus.QOS2);
            Assert.Equal(0, (int)ProjectName.QosStatus.QOS0);
            Assert.Equal(1, (int)ProjectName.QosStatus.QOS1);
            Assert.Equal(2, (int)ProjectName.QosStatus.QOS2);
        }

        [Fact]
        public void TestSessionStatus()
        {
            Assert.Equal(2, System.Enum.GetValues(typeof(ProjectName.SessionStatus)).Length);
            Assert.Equal(ProjectName.SessionStatus.CLOSE, ProjectName.SessionStatus.CLOSE);
            Assert.Equal(ProjectName.SessionStatus.OPEN, ProjectName.SessionStatus.OPEN);
        }

        [Fact]
        public void TestSubStatus()
        {
            Assert.Equal(2, System.Enum.GetValues(typeof(ProjectName.SubStatus)).Length);
            Assert.Equal(ProjectName.SubStatus.CANCEL, ProjectName.SubStatus.CANCEL);
            Assert.Equal(ProjectName.SubStatus.SUBSCRIBE, ProjectName.SubStatus.SUBSCRIBE);
        }
    }
}