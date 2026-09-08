using Xunit;
using Moq;

namespace GridListViewAdapters.Tests.Utils
{
    public class ViewHolderPositionTaggerTests
    {
        [Fact]
        public void TagAndRetrievePosition_SetsTagAndGetsIt()
        {
            var view = new Mock<IView>();
            ViewHolderPositionTagger.TagPosition(view.Object, 5);
            view.Verify(v => v.SetTag(ViewHolderPositionTagger.PositionTagKey, 5), Times.Once);

            view.Setup(v => v.GetTag(ViewHolderPositionTagger.PositionTagKey)).Returns(5);
            int result = ViewHolderPositionTagger.GetPosition(view.Object);
            Assert.Equal(5, result);
        }
    }
}