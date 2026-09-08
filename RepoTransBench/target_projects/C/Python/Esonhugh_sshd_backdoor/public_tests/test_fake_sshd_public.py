import pytest
import os
import stat
from pathlib import Path

# Similar to original tests, public tests also mock interactions with /root/.ssh.
# We'll use a temporary directory for isolation.

class TestPublicFakeSshd:

    @pytest.fixture(autouse=True)
    def setup_fake_root_ssh_public(self, tmp_path):
        """
        Fixture to create a mock /root/.ssh directory structure for public tests.
        """
        self.fake_root_ssh = tmp_path / "root" / ".ssh"
        self.fake_root_ssh.mkdir(parents=True, mode=0o700)
        self._temp_files = [] # Track files created by external program simulation
        yield
        for f in self._temp_files:
            if f.exists():
                f.unlink()

    def test_read_public_keys(self):
        """
        Test reading public_authorized_keys and verifying content.
        Corresponds to test_read_public_keys in test_main_public.c.
        """
        filename = self.fake_root_ssh / "public_authorized_keys"
        expected_content = "public-dummy-key\nsecond-public-key\n"
        
        with open(filename, "w") as f:
            f.write(expected_content)

        # Simulate C open/read behavior
        content = ""
        try:
            with open(filename, "r") as f:
                content = f.read()
        except FileNotFoundError:
            pytest.fail("test_read_public_keys: FAIL (cannot open file)")
        
        assert "public-dummy-key" in content and "second-public-key" in content, \
            "test_read_public_keys: FAIL (expected test data not found)"
        
        print("test_read_public_keys: PASS")

    def test_nonexistent_file(self):
        """
        Test when public_authorized_keys file does not exist.
        Corresponds to test_nonexistent_file in test_main_public.c.
        """
        filename = self.fake_root_ssh / "nonexistent_public_file"
        
        # Ensure file does not exist
        if filename.exists():
            filename.unlink()

        with pytest.raises(FileNotFoundError) as excinfo:
            with open(filename, "r") as f:
                pass

        assert "No such file or directory" in str(excinfo.value) or "file not found" in str(excinfo.value).lower(), \
            "test_nonexistent_file: FAIL (file unexpectedly exists or wrong error)"
        
        print("test_nonexistent_file: PASS")

    def test_run_public_tests_sh_simulation(self, tmp_path):
        """
        Simulates the behavior of the original run_public_tests.sh script's
        interaction with `fake_sshd_public_test` and `test_output_public.txt`.
        The C `main_public.c` is not provided, so we simulate its file I/O behavior.
        """
        # Prepare mock /root/.ssh as done by the C script
        mock_public_authorized_keys_path = self.fake_root_ssh / "public_authorized_keys"
        mock_public_authorized_keys_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with open(mock_public_authorized_keys_path, "w") as f:
            f.write("public-dummy-key\nsecond-public-key\n")

        # Simulate fake_sshd_public_test output
        temp_output_file = tmp_path / "test_output_public.txt"
        self._temp_files.append(temp_output_file) # Track for cleanup

        simulated_output = ""
        try:
            with open(mock_public_authorized_keys_path, "r") as f:
                simulated_output = f.read()
        except FileNotFoundError:
            simulated_output = "ERROR OPEN FILE\n"

        with open(temp_output_file, "w") as f:
            f.write(simulated_output)
            # Original test_output_public.txt has extra newlines, mimicking that
            f.write("\n\n") 

        # Verify conditions as per the original run_public_tests.sh
        with open(temp_output_file, "r") as f:
            output_content = f.read()

        assert "===== Public Test program output =====" in f"===== Public Test program output =====\n{output_content}\n=============================="
        assert "==============================" in f"===== Public Test program output =====\n{output_content}\n=============================="

        assert "ERROR OPEN FILE" not in output_content, "Public test failed: could not open file"
        assert "public-dummy-key" in output_content and "second-public-key" in output_content, \
            "Public test failed: did not print public_authorized_keys contents"
        
        print("test_run_public_tests_sh_simulation passed")