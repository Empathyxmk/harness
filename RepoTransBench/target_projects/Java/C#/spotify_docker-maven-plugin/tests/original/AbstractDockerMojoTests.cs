using System;
using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class AbstractDockerMojoTests
    {
        private const string DOCKER_HOST = "testhost";
        private const string DOCKER_CERT_PATH = "test_resources/certs";
        private const string SERVER_ID = "testId";
        private const string REGISTRY_URL = "my.docker.reg";
        private const string USERNAME = "username";
        private const string PASSWORD = "password";
        private const string EMAIL = "user@host.domain";

        private Mock<ISettings> _settings;
        private Mock<IDockerClientBuilder> _builder;

        private AbstractDockerMojo _sut;

        public AbstractDockerMojoTests()
        {
            _settings = new Mock<ISettings>();
            _builder = new Mock<IDockerClientBuilder>();
            _sut = new ConcreteDockerMojo(_settings.Object, _builder.Object);
        }

        [Fact]
        public void TestDockerHostSet()
        {
            _sut.DockerHost = DOCKER_HOST;
            _sut.DockerCertPath = DOCKER_CERT_PATH;
            _sut.Execute();
            _builder.Verify(b => b.Uri(DOCKER_HOST), Times.Once());
            _builder.Verify(b => b.DockerCertificates(It.IsAny<IDockerCertificates>()), Times.Once());
        }

        // ...other tests, e.g., authentication...
    }
}