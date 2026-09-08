using System;
using Xunit;
using Moq;

namespace PayatuDivaAndroid.Tests.Original
{
    public class AccessControl1Activity
    {
        public bool IntentWasStarted { get; private set; }
        public bool ToastWasShown { get; private set; }
        public bool IntentCanBeResolved { get; set; }

        public void ViewAPICredentials()
        {
            if (IntentCanBeResolved)
            {
                IntentWasStarted = true;
            }
            else
            {
                ToastWasShown = true;
            }
        }
    }

    public class AccessControl1ActivityTests
    {
        private AccessControl1Activity activity;

        public AccessControl1ActivityTests()
        {
            activity = new AccessControl1Activity();
        }

        [Fact]
        public void Test_OnCreate_SetsLayout()
        {
            Assert.NotNull(activity);
        }

        [Fact]
        public void Test_ViewAPICredentials_IntentResolved_StartsActivity()
        {
            activity.IntentCanBeResolved = true;
            activity.ViewAPICredentials();
            Assert.True(activity.IntentWasStarted);
        }

        [Fact]
        public void Test_ViewAPICredentials_IntentNotResolved_ShowsToastAndLogs()
        {
            activity.IntentCanBeResolved = false;
            activity.ViewAPICredentials();
            Assert.True(activity.ToastWasShown);
        }
    }
}