using System.Collections.Generic;
using Xunit;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    public class PreferenceComponent_AppComponent
    {
        private static PreferenceComponent_AppComponent _instance;
        public static PreferenceComponent_AppComponent GetInstance()
        {
            return _instance ??= new PreferenceComponent_AppComponent();
        }

        public object UserProfile() => new object();
        public object UserDevice() => new object();
        public List<string> GetEntityNameList() => new List<string> { "UserProfile", "UserDevice" };
    }

    public class AppComponentTests
    {
        private PreferenceComponent_AppComponent appComponent;

        public AppComponentTests()
        {
            appComponent = PreferenceComponent_AppComponent.GetInstance();
        }

        [Fact]
        public void ComponentInitializeTest()
        {
            Assert.NotNull(PreferenceComponent_AppComponent.GetInstance());
        }

        [Fact]
        public void EntityInitializeTest()
        {
            Assert.NotNull(appComponent.UserProfile());
            Assert.NotNull(appComponent.UserDevice());
        }

        [Fact]
        public void EntityListTest()
        {
            Assert.Equal("UserProfile", appComponent.GetEntityNameList()[0]);
            Assert.Equal("UserDevice", appComponent.GetEntityNameList()[1]);
        }
    }
}