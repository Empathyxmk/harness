using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Moq;

namespace OriginalTests.Sequence
{
    public class ZkDistributedSequenceUnitTests
    {
        private Mock<ICuratorFramework> _clientMock;
        private ZkDistributedSequence _zkSequence;

        public ZkDistributedSequenceUnitTests()
        {
            _clientMock = new Mock<ICuratorFramework>();
            _zkSequence = new ZkDistributedSequence("localhost");
            typeof(ZkDistributedSequence).GetField("client", BindingFlags.NonPublic | BindingFlags.Instance)
                ?.SetValue(_zkSequence, _clientMock.Object);
        }

        [Fact]
        public void TestGetSetMaxRetries()
        {
            Assert.Equal(3, _zkSequence.MaxRetries);
            _zkSequence.MaxRetries = 9;
            Assert.Equal(9, _zkSequence.MaxRetries);
        }

        [Fact]
        public void TestGetBaseSleepTimeMs()
        {
            Assert.Equal(1000, _zkSequence.BaseSleepTimeMs);
        }

        [Fact]
        public void TestSequenceReturnsValue()
        {
            var setDataBuilder = new Mock<ISetDataBuilder>();
            var setDataBuilderWithVersion = new Mock<ISetDataBuilder>();
            _clientMock.Setup(c => c.SetData()).Returns(setDataBuilder.Object);
            setDataBuilder.Setup(b => b.WithVersion(-1)).Returns(setDataBuilderWithVersion.Object);
            var fakeStat = new StatFake() { Version = 17 };
            setDataBuilderWithVersion.Setup(b => b.ForPath(It.IsAny<string>(), It.IsAny<byte[]>())).Returns(fakeStat);
            long? result = _zkSequence.Sequence("abc");
            Assert.NotNull(result);
            Assert.Equal(17, result.Value);
        }

        [Fact]
        public void TestSequenceHandlesException()
        {
            var setDataBuilder = new Mock<ISetDataBuilder>();
            var setDataBuilderWithVersion = new Mock<ISetDataBuilder>();
            _clientMock.Setup(c => c.SetData()).Returns(setDataBuilder.Object);
            setDataBuilder.Setup(b => b.WithVersion(-1)).Returns(setDataBuilderWithVersion.Object);
            setDataBuilderWithVersion.Setup(b => b.ForPath(It.IsAny<string>(), It.IsAny<byte[]>())).Throws(new Exception("fail!"));
            long? result = _zkSequence.Sequence("failcase");
            Assert.Null(result);
        }
    }
}

/* Fake interfaces and classes for this translation: in real code, these would be the real Curator/ZooKeeper .NET equivalents */

public interface ICuratorFramework
{
    ISetDataBuilder SetData();
}

public interface ISetDataBuilder
{
    ISetDataBuilder WithVersion(int version);
    object ForPath(string path, byte[] data);
}

// Fake stat used for getting version result
public class StatFake
{
    public int Version { get; set; }
}