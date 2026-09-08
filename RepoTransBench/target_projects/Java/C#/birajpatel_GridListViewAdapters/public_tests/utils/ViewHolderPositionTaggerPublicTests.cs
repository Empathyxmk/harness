using Xunit;

namespace GridListViewAdapters.PublicTests.Utils
{
    public class ViewHolderPositionTaggerPublicTests
    {
        [Fact]
        public void SetAndGetPositionTagsPublic()
        {
            var tagger = new ViewHolderPositionTagger();
            tagger.SetRowPosition(5);
            tagger.SetColumnPosition(7);
            Assert.Equal(5, tagger.GetRowPosition());
            Assert.Equal(7, tagger.GetColumnPosition());
        }
    }
}