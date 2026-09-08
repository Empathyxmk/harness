import pytest
from unittest.mock import Mock, call

class ChatNotification:
    pass

class ChatMessage:
    def __init__(self, sender_id, recipient_id, content):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.id = None

    @staticmethod
    def builder():
        class Builder:
            def __init__(self):
                self._sender_id = None
                self._recipient_id = None
                self._content = None

            def senderId(self, sender_id):
                self._sender_id = sender_id
                return self

            def recipientId(self, recipient_id):
                self._recipient_id = recipient_id
                return self

            def content(self, content):
                self._content = content
                return self

            def build(self):
                return ChatMessage(self._sender_id, self._recipient_id, self._content)
        return Builder()

class ChatMessageService:
    def save(self, message):
        pass

    def find_chat_messages(self, sender_id, recipient_id):
        pass

class SimpMessagingTemplate:
    def convert_and_send_to_user(self, username, dest, notification):
        pass

class ChatController:
    def __init__(self, messaging_template, message_service):
        self.messaging_template = messaging_template
        self.message_service = message_service

    def process_message(self, chat_message):
        msg_to_save = chat_message
        saved_msg = self.message_service.save(msg_to_save)
        notification = ChatNotification()
        self.messaging_template.convert_and_send_to_user(
            chat_message.recipient_id,
            "/queue/messages",
            notification
        )
        # No return (void)

    def find_chat_messages(self, sender_id, recipient_id):
        messages = self.message_service.find_chat_messages(sender_id, recipient_id)
        return (200, messages)

def test_process_message_sends_and_saves_message():
    # Arrange
    messaging_template = Mock(spec=SimpMessagingTemplate)
    chat_message_service = Mock(spec=ChatMessageService)

    chat_message = ChatMessage.builder()\
        .senderId("user1")\
        .recipientId("user2")\
        .content("Hello")\
        .build()
    chat_message.id = "msg1"

    chat_message_service.save.return_value = chat_message

    controller = ChatController(messaging_template, chat_message_service)

    # Act
    controller.process_message(chat_message)

    # Assert
    chat_message_service.save.assert_called_once_with(chat_message)
    messaging_template.convert_and_send_to_user.assert_called_once()
    args = messaging_template.convert_and_send_to_user.call_args[0]
    assert args[0] == "user2"
    assert args[1] == "/queue/messages"
    # args[2] is a ChatNotification

def test_find_chat_messages_returns_messages():
    messaging_template = Mock(spec=SimpMessagingTemplate)
    chat_message_service = Mock(spec=ChatMessageService)

    sender_id = "user1"
    recipient_id = "user2"
    mock_messages = [
        ChatMessage.builder().senderId(sender_id).recipientId(recipient_id).content("Hi").build(),
        ChatMessage.builder().senderId(recipient_id).recipientId(sender_id).content("Hello").build()
    ]

    chat_message_service.find_chat_messages.return_value = mock_messages

    controller = ChatController(messaging_template, chat_message_service)
    status, body = controller.find_chat_messages(sender_id, recipient_id)

    assert status == 200
    assert body == mock_messages
    chat_message_service.find_chat_messages.assert_called_once_with(sender_id, recipient_id)