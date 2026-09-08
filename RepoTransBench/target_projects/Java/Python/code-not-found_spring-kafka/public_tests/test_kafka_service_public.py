import pytest

from src.kafkaservice.kafka_service import KafkaService

class TestKafkaServicePublic:
    def test_process_message_valid_diff(self):
        service = KafkaService()
        result = service.process_message("Kafka Rocks")
        assert result is not None
        assert result == "Processed: KAFKA ROCKS"

    def test_process_message_null_public(self):
        service = KafkaService()
        result = service.process_message(None)
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_empty_public(self):
        service = KafkaService()
        result = service.process_message("")
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_whitespace_public(self):
        service = KafkaService()
        result = service.process_message("\t\n")
        assert result is not None
        assert result == "Error: Message cannot be empty."

    def test_process_message_too_long_public(self):
        service = KafkaService()
        long_message = "Short messages are nice, but this one is way too long!!!"
        result = service.process_message(long_message)
        assert result is not None
        assert result == "Warning: Message too long."

    def test_process_message_boundary_length_fifty_public(self):
        service = KafkaService()
        msg = "12345678901234567890123456789012345678901234567890"  # 50 chars
        result = service.process_message(msg)
        assert result is not None
        assert result == "Processed: 12345678901234567890123456789012345678901234567890"

    def test_process_message_boundary_length_fifty_one_public(self):
        service = KafkaService()
        msg = "123456789012345678901234567890123456789012345678901"  # 51 chars
        result = service.process_message(msg)
        assert result is not None
        assert result == "Warning: Message too long."

    def test_get_message_length_valid_public(self):
        service = KafkaService()
        length = service.get_message_length("Kafka")
        assert length == 5

    def test_get_message_length_null_public(self):
        service = KafkaService()
        length = service.get_message_length(None)
        assert length == 0

    def test_get_message_length_empty_public(self):
        service = KafkaService()
        length = service.get_message_length("   ".strip())
        assert length == 0