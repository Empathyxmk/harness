using Xunit;
using Moq;
using System;
using System.Reflection;

namespace NetEaseArrowTests.Public
{
    public interface ITestAnnotation
    {
        object GetRetryAnalyzer();
        void SetRetryAnalyzer(Type type);
    }

    public class AnotherDummyTest { }

    public class RetryListener
    {
        public void Transform(ITestAnnotation annotation, Type testClass, ConstructorInfo ctor, MethodInfo method)
        {
            if (annotation.GetRetryAnalyzer() == null)
            {
                annotation.SetRetryAnalyzer(typeof(TestngRetry));
            }
        }
    }

    public class TestngRetry { }

    public class RetryListenerPublicTests
    {
        [Fact]
        public void TestTransformSetsRetryAnalyzerWhenNull()
        {
            var listener = new RetryListener();
            var mockAnnotation = new Mock<ITestAnnotation>();
            mockAnnotation.Setup(x => x.GetRetryAnalyzer()).Returns((object)null);

            listener.Transform(mockAnnotation.Object, typeof(AnotherDummyTest), null, null);
            mockAnnotation.Verify(x => x.SetRetryAnalyzer(typeof(TestngRetry)), Times.Once());
        }

        [Fact]
        public void TestTransformDoesNotOverrideIfAlreadySet()
        {
            var listener = new RetryListener();
            var mockAnnotation = new Mock<ITestAnnotation>();
            var mockedRetry = new object();
            mockAnnotation.Setup(x => x.GetRetryAnalyzer()).Returns(mockedRetry);

            listener.Transform(mockAnnotation.Object, typeof(AnotherDummyTest), null, null);
            mockAnnotation.Verify(x => x.SetRetryAnalyzer(It.IsAny<Type>()), Times.Never());
        }
    }
}