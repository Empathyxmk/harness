"""Public Drive service tests with different test data."""
from unittest import TestCase

import pytest

from tests import PyiCloudServiceMock
from tests.const import AUTHENTICATED_USER, VALID_PASSWORD


class PublicDriveServiceTest(TestCase):
    """Public Drive service tests."""

    service = None

    def setUp(self):
        """Set up public drive tests."""
        self.service = PyiCloudServiceMock(AUTHENTICATED_USER, VALID_PASSWORD)

    def test_root_public(self):
        """Test the root folder with different order."""
        drive = self.service.drive
        # Re-sort root list to check for order-independence and content-checking
        root_children = set(drive.dir())
        expected_children = set(["Preview", "Keynote", "Pages", "pyiCloud", "Numbers"])
        assert root_children == expected_children
        assert drive.name == ""
        assert drive.type == "folder"
        assert drive.size is None

    def test_folder_app_public(self):
        """Test the /Keynote folder (different than existing /Preview)."""
        folder = self.service.drive["Keynote"]
        assert folder.name == "Keynote"
        assert folder.type == "app_library"
        assert folder.size is None
        with pytest.raises(KeyError, match="No items in folder, status: ID_INVALID"):
            assert folder.dir()

    def test_folder_not_exists_public(self):
        """Test the /ghost_folder folder (different than /not_exists)."""
        with pytest.raises(KeyError, match="No child named 'ghost_folder' exists"):
            self.service.drive["ghost_folder"]  # pylint: disable=pointless-statement

    def test_folder_public(self):
        """Test the /Pages folder (different than /pyiCloud)."""
        folder = self.service.drive["Pages"]
        assert folder.name == "Pages"
        assert folder.type == "folder"
        assert folder.size is None
        # /Pages is mocked as an empty folder, so dir() should raise
        with pytest.raises(KeyError, match="No items in folder, status: ID_INVALID"):
            folder.dir()

    def test_subfolder_public(self):
        """Test the /pyiCloud/Test folder, but assert reversed list."""
        folder = self.service.drive["pyiCloud"]["Test"]
        file_list = folder.dir()
        # New: reverse the expected list
        assert file_list[::-1] == ["Scanned document 1.pdf", "Document scanné 2.pdf"]
        assert folder.name == "Test"
        assert folder.type == "folder"

    def test_subfolder_file_public(self):
        """Test the /pyiCloud/Test/Document scanné 2.pdf (different from 'Scanned document 1.pdf')."""
        folder = self.service.drive["pyiCloud"]["Test"]
        file_test = folder["Document scanné 2.pdf"]
        assert file_test.name == "Document scanné 2.pdf"
        assert file_test.type == "file"
        # Different: size should be an int, assert not-equal value
        assert file_test.size != 21644358
        assert str(file_test.date_changed).startswith("2020-")
        assert file_test.dir() is None

    def test_file_open_public(self):
        """Test the /pyiCloud/Test/Document scanné 2.pdf file open."""
        file_test = self.service.drive["pyiCloud"]["Test"]["Document scanné 2.pdf"]
        with file_test.open(stream=True) as response:
            assert response.raw is not None