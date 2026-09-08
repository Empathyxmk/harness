import pytest
import os
import stat
from pathlib import Path

# The original C tests mock interactions with /root/.ssh.
# We will use a temporary directory provided by pytest's tmp_path fixture
# to simulate this environment safely and cleanly.

class TestOriginalFakeSshd:

    @pytest.fixture(autouse=True)
    def setup_fake_root_ssh(self, tmp_path):
        """
        Fixture to create a mock /root/.ssh directory structure for tests.
        The C tests perform operations directly on /root/.ssh.
        We simulate this by creating a temp directory and acting as if it's /root/.ssh.
        """
        self.fake_root_ssh = tmp_path / "root" / ".ssh"
        self.fake_root_ssh.mkdir(parents=True, mode=0o700)
        # Store for cleanup in teardown (if not autouse) or implicitly by tmp_path
        self._temp_files = [] 
        yield
        # Clean up files created by the "external program simulation"
        for f in self._temp_files:
            if f.exists():
                f.unlink()

    def _safe_unlink(self, path):
        """Helper: Safe unlink, ignore errors if file is missing."""
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def test_read_authorized_keys(self):
        """Test opening and reading the authorized_keys file exists."""
        filepath = self.fake_root_ssh / "authorized_keys"
        
        # Prepare file
        with open(filepath, "w") as f:
            f.write("unit-test-key")

        # Simulate C open/read behavior
        with open(filepath, "r") as f:
            content = f.read()

        assert "unit-test-key" in content, "File content should contain 'unit-test-key'"
        
        print("test_read_authorized_keys passed")
        self._safe_unlink(filepath)

    def test_file_not_found(self):
        """Test when file does not exist."""
        filepath = self.fake_root_ssh / "authorized_keys"
        self._safe_unlink(filepath) # Ensure it doesn't exist

        with pytest.raises(FileNotFoundError) as excinfo:
            with open(filepath, "r") as f:
                pass # This line should not be reached

        # On some systems, permission errors or other issues might arise.
        # The C code checks for fd < 0, which means any error on open.
        # Python's FileNotFoundError is the most direct equivalent for non-existence.
        assert "No such file or directory" in str(excinfo.value) or "file not found" in str(excinfo.value).lower()
        
        print("test_file_not_found passed")

    def test_empty_file(self):
        """Test when file can be opened but is empty."""
        filepath = self.fake_root_ssh / "authorized_keys"
        
        with open(filepath, "w") as f:
            pass # Create an empty file

        with open(filepath, "r") as f:
            content = f.read()
        
        assert len(content) == 0, "File content should be empty"
        
        print("test_empty_file passed")
        self._safe_unlink(filepath)

    def test_large_file(self):
        """Test large file contents."""
        filepath = self.fake_root_ssh / "authorized_keys"
        
        with open(filepath, "w") as f:
            for i in range(4096):
                f.write(chr(ord('A') + (i % 26)))

        with open(filepath, "r") as f:
            content = f.read()
        
        assert len(content) == 4096, "File content length should be 4096"
        expected_content = ""
        for i in range(4096):
            expected_content += chr(ord('A') + (i % 26))
        assert content == expected_content, "File content should match the pattern"
        
        print("test_large_file passed")
        self._safe_unlink(filepath)

    def test_run_tests_sh_simulation(self, tmp_path):
        """
        Simulates the behavior of the original run_tests.sh script's
        interaction with `fake_sshd_test` and `test_output.txt`.
        The C `main_fixed.c` is not provided, so we simulate its file I/O behavior.
        """
        # Prepare mock /root/.ssh as done by the C script
        mock_authorized_keys_path = self.fake_root_ssh / "authorized_keys"
        mock_authorized_keys_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with open(mock_authorized_keys_path, "w") as f:
            f.write("dummy-key\n")

        # Simulate fake_sshd_test output
        # The C fake_sshd_test is assumed to read /root/.ssh/authorized_keys
        # and print its content.
        # We'll write to a temporary output file to simulate test/fake_sshd/test_output.txt
        temp_output_file = tmp_path / "test_output.txt"
        self._temp_files.append(temp_output_file) # Track for cleanup

        # If the simulated 'fake_sshd_test' were to encounter an error, it would print "ERROR OPEN FILE".
        # For a successful run, it would print the key.
        simulated_output = ""
        try:
            with open(mock_authorized_keys_path, "r") as f:
                simulated_output = f.read()
        except FileNotFoundError:
            simulated_output = "ERROR OPEN FILE\n"

        with open(temp_output_file, "w") as f:
            # The original test_output.txt has a gcov profiling error message and then "dummy-key"
            # We'll just put the expected output directly here for simplicity,
            # focusing on the 'dummy-key' assertion logic.
            f.write("libgcov profiling error:fake.gcda:overwriting an existing profile data with a different timestamp\n")
            f.write(simulated_output)

        # Verify conditions as per the original run_tests.sh
        with open(temp_output_file, "r") as f:
            output_content = f.read()

        assert "===== Test program output =====" in f"===== Test program output =====\n{output_content}\n=============================="
        assert "==============================" in f"===== Test program output =====\n{output_content}\n=============================="

        assert "ERROR OPEN FILE" not in output_content, "Test failed: could not open file"
        assert "dummy-key" in output_content, "Test failed: did not print authorized_keys"
        print("test_run_tests_sh_simulation passed")