using Xunit;

namespace martin90s_ImagePicker.PublicTests
{
    public interface IPhotoLoadListenerPublic
    {
        void OnPhotoLoaded(int count);
    }

    public class PhotoLoadListenerPublicTests
    {
        private class DummyListener : IPhotoLoadListenerPublic
        {
            public int LastCount = -2;
            public bool Called = false;
            public void OnPhotoLoaded(int count)
            {
                LastCount = count;
                Called = true;
            }
        }

        [Fact]
        public void TestPhotoLoadListenerWithDifferentCount()
        {
            var listener = new DummyListener();
            listener.OnPhotoLoaded(7); // different count
            Assert.True(listener.Called);
            Assert.Equal(7, listener.LastCount);
        }

        [Fact]
        public void TestPhotoLoadListenerMultipleCalls()
        {
            var listener = new DummyListener();
            listener.OnPhotoLoaded(2);
            Assert.True(listener.Called);
            Assert.Equal(2, listener.LastCount);
            listener.OnPhotoLoaded(12);
            Assert.Equal(12, listener.LastCount);
        }
    }
}