using Xunit;
using Moq;
using easygcm;

namespace public_tests
{
    public class GcmRegistrationServicePublicTests
    {
        private Mock<object> mockContext;

        public GcmRegistrationServicePublicTests()
        {
            mockContext = new Mock<object>();
        }

        [Fact]
        public void TestCreateGcmRegistrationIntentWithWakeLockPublic()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object, false);
            Assert.NotNull(intent);
        }

        [Fact]
        public void TestCreateGcmRegistrationIntentWithWakeLockPublicDifferent()
        {
            var intent = GcmRegistrationService.CreateGcmRegistrationIntent(mockContext.Object, true);
            Assert.NotNull(intent);
        }
    }
}