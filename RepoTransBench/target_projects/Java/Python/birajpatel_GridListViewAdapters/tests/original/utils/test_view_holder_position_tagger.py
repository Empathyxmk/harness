def test_tag_and_retrieve_position(mocker):
    class ViewHolderPositionTagger:
        POSITION_TAG_KEY = "KEY"
        @staticmethod
        def tagPosition(view, pos):
            view.setTag(ViewHolderPositionTagger.POSITION_TAG_KEY, pos)
        @staticmethod
        def getPosition(view):
            return view.getTag(ViewHolderPositionTagger.POSITION_TAG_KEY)

    view = mocker.Mock()
    ViewHolderPositionTagger.tagPosition(view, 5)
    view.setTag.assert_called_with(ViewHolderPositionTagger.POSITION_TAG_KEY, 5)
    view.getTag.return_value = 5
    result = ViewHolderPositionTagger.getPosition(view)
    assert result == 5