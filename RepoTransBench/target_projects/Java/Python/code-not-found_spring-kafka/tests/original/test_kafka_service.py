import pytest

from src.kafkaservice.kafka_service import KafkaService

class TestKafkaServiceOriginal:
    def test_process_message_valid(self):
        service = KafkaService()
        result = service.process_message("hello world")
        assert result is not None
        assert result == "Processed: HELLO WORLD"

    def test_process_message_null(self):
        service = KafkaService()
        result = service.process_message(None)
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_empty(self):
        service = KafkaService()
        result = service.process_message("")
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_whitespace(self):
        service = KafkaService()
        result = service.process_message("   ")
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_too_long(self):
        service = KafkaService()
        long_message = (
            "This is a very long message that definitely exceeds fifty characters in length and will trigger the warning message condition."
        )
        result = service.process_message(long_message)
        assert result is not None
        assert result == "Warning: Message too long."

    def test_process_message_boundary_length_fifty(self):
        service = KafkaService()
        fifty_char_message = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX"  # 50 chars
        result = service.process_message(fifty_char_message)
        assert result is not None
        assert result == "Processed: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX"

    def test_process_message_boundary_length_fifty_one(self):
        service = KafkaService()
        fifty_one_char_message = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"  # 51 chars
        result = service.process_message(fifty_one_char_message)
        assert result is not None
        assert result == "Warning: Message too long."

    def test_get_message_length_valid(self):
        service = KafkaService()
        length = service.get_message_length("test")
        assert length == 4

    def test_get_message_length_null(self):
        service = KafkaService()
        length = service.get_message_length(None)
        assert length == 0

    def test_get_message_length_empty(self):
        service = KafkaService()
        length = service.get_message_length("")
        assert length == 0