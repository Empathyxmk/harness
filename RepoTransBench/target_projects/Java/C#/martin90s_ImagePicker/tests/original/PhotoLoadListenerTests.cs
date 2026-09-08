using System;
using System.Collections.Generic;
using Xunit;

namespace martin90s_ImagePicker.OriginalTests
{
    public interface IPhotoLoadListener
    {
        void OnLoadComplete(List<string> photoUris);
        void OnLoadError();
    }

    public class PhotoLoadListenerTests
    {
        private bool onLoadCompleteCalled = false;
        private bool onLoadErrorCalled = false;

        private class DummyListener : IPhotoLoadListener
        {
            private PhotoLoadListenerTests parent;
            public DummyListener(PhotoLoadListenerTests p) { parent = p; }
            public void OnLoadComplete(List<string> photoUris)
            {
                parent.onLoadCompleteCalled = true;
                Assert.NotNull(photoUris);
            }
            public void OnLoadError()
            {
                parent.onLoadErrorCalled = true;
            }
        }

        [Fact]
        public void TestListener()
        {
            var listener = new DummyListener(this);
            listener.OnLoadComplete(new List<string>());
            listener.OnLoadError();
            Assert.True(onLoadCompleteCalled);
            Assert.True(onLoadErrorCalled);
        }
    }
}