import pytest
import os

from src.readmidi import readmidi

class DummyTrack:
    def __init__(self):
        self.messages = [1]
        self.rawbytes_header = [1, 2, 3]

class DummyMidiStruct:
    def __init__(self):
        self.format = 1
        self.ticks_per_quarter_note = 96
        self.track = [DummyTrack()]
        self.rawbytes_all = [1, 2, 3]
        self.rawbytes_header = [4, 5, 6]

class TestReadMidi:
    @pytest.fixture(autouse=True)
    def set_filepath(self):
        self.midi_file_path = os.path.join("tests", "midi", "jesu.mid")

    def test_read_valid_midi_file(self):
        midi_struct = readmidi(self.midi_file_path)
        assert isinstance(midi_struct, object)
        assert hasattr(midi_struct, 'format')
        assert hasattr(midi_struct, 'ticks_per_quarter_note')
        assert hasattr(midi_struct, 'track')
        assert len(midi_struct.track) > 0
        assert getattr(midi_struct, 'format') == 1
        assert getattr(midi_struct, 'ticks_per_quarter_note') == 96
        assert hasattr(midi_struct.track[0], 'messages')
        assert len(midi_struct.track[0].messages) > 0

    def test_read_valid_midi_file_with_raw_bytes(self):
        midi_struct = readmidi(self.midi_file_path, 1)
        assert hasattr(midi_struct, 'rawbytes_all')
        assert hasattr(midi_struct, 'rawbytes_header')
        assert hasattr(midi_struct.track[0], 'rawbytes_header')
        assert len(midi_struct.rawbytes_all) > 0
        assert len(midi_struct.rawbytes_header) > 0
        assert len(midi_struct.track[0].rawbytes_header) > 0

    def test_file_not_found(self):
        non_existent = 'non_existent_file.mid'
        with pytest.raises(Exception):
            readmidi(non_existent)

    def test_malformed_header_id(self, tmp_path):
        bad_bytes = bytes([0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 0, 1, 0, 120])
        filename = tmp_path / "malformed_midi_bad_id.mid"
        with open(filename, 'wb') as f:
            f.write(bad_bytes)
        with pytest.raises(Exception):
            readmidi(str(filename))

    def test_malformed_header_length(self, tmp_path):
        bad_bytes = bytes([77, 84, 104, 100, 0, 0, 0, 5, 0, 1, 0, 1, 0, 120])
        filename = tmp_path / "malformed_midi_bad_len.mid"
        with open(filename, 'wb') as f:
            f.write(bad_bytes)
        with pytest.raises(Exception):
            readmidi(str(filename))

    def test_malformed_format(self, tmp_path):
        bad_bytes = bytes([77, 84, 104, 100, 0, 0, 0, 6, 0, 3, 0, 1, 0, 120])
        filename = tmp_path / "malformed_midi_bad_format.mid"
        with open(filename, 'wb') as f:
            f.write(bad_bytes)
        with pytest.raises(Exception):
            readmidi(str(filename))

    def test_format0_with_multiple_tracks(self, tmp_path):
        bad_bytes = bytes([77, 84, 104, 100, 0, 0, 0, 6, 0, 0, 0, 2, 0, 120])
        filename = tmp_path / "malformed_midi_format0_multi_track.mid"
        with open(filename, 'wb') as f:
            f.write(bad_bytes)
        with pytest.raises(Exception):
            readmidi(str(filename))

    def test_smpte_time_format(self, tmp_path):
        smpte_time_unit = 2**15 + 120
        smpte_bytes = int(smpte_time_unit).to_bytes(2, byteorder='big', signed=False)
        bad_bytes = bytes([77, 84, 104, 100, 0, 0, 0, 6, 0, 1, 0, 1]) + smpte_bytes
        filename = tmp_path / "malformed_midi_smpte_time.mid"
        with open(filename, 'wb') as f:
            f.write(bad_bytes)
        with pytest.raises(Exception):
            readmidi(str(filename))

    def test_missing_track_header(self, tmp_path):
        header = bytes([77, 84, 104, 100, 0, 0, 0, 6, 0, 1, 0, 2, 0, 120])
        eot_message = bytes([0, 255, 47, 0])
        valid_track = bytes([77, 84, 114, 107, 0, 0, 0, 4]) + eot_message
        bad_track = bytes([0, 0, 0, 0, 0, 0, 0, 4]) + eot_message
        file_content = header + valid_track + bad_track
        filename = tmp_path / "malformed_midi_missing_track_header.mid"
        with open(filename, 'wb') as f:
            f.write(file_content)
        with pytest.raises(Exception):
            readmidi(str(filename))