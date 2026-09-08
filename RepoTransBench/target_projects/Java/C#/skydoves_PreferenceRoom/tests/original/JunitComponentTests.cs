using System.Collections.Generic;
using Xunit;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    // Dummy for inject preference
    public class PreferenceComponent_JunitComponent
    {
        private static PreferenceComponent_JunitComponent _instance;
        public static PreferenceComponent_JunitComponent GetInstance()
            => _instance ??= new PreferenceComponent_JunitComponent();

        public void Inject(object target) { /* Simulated injection */ }
        public object TestProfile() => new object();
        public List<string> GetEntityNameList() => new List<string> { "TestProfile" };
    }

    public class JunitComponentTests
    {
        private PreferenceComponent_JunitComponent junitComponent;

        public JunitComponentTests()
        {
            PreferenceComponent_JunitComponent.GetInstance().Inject(this);
            junitComponent = PreferenceComponent_JunitComponent.GetInstance();
        }

        [Fact]
        public void InjectionTest()
        {
            Assert.NotNull(junitComponent);
            Assert.NotNull(junitComponent.TestProfile());
        }

        [Fact]
        public void EntityListTest()
        {
            Assert.Equal("TestProfile", junitComponent.GetEntityNameList()[0]);
        }
    }
}