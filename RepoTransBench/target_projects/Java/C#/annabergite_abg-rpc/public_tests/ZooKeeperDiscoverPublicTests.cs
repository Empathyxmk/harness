using System;
using Xunit;

namespace AnnabergiteAbgRpc.PublicTests
{
    public class ZooKeeperDiscoverPublicTests
    {
        [Fact]
        public void TestDiscoverWithDifferentPath()
        {
            string path = "/public/test/path";
            bool called = false;

            var listener = new DiscoverListener(pathVal =>
            {
                if (pathVal == path)
                    called = true;
            });

            listener.Changed(path);
            Assert.True(called);
        }

        public class DiscoverListener
        {
            private readonly Action<string> _callback;
            public DiscoverListener(Action<string> cb) { _callback = cb; }
            public void Changed(string changedPath) { _callback(changedPath); }
        }
    }
}