import pytest
from unittest.mock import Mock

class ChatRoom:
    def __init__(self, chat_id, sender_id, recipient_id):
        self.chat_id = chat_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id

    @staticmethod
    def builder():
        class Builder:
            def __init__(self):
                self._chat_id = None
                self._sender_id = None
                self._recipient_id = None

            def chatId(self, chat_id):
                self._chat_id = chat_id
                return self

            def senderId(self, sender_id):
                self._sender_id = sender_id
                return self

            def recipientId(self, recipient_id):
                self._recipient_id = recipient_id
                return self

            def build(self):
                return ChatRoom(self._chat_id, self._sender_id, self._recipient_id)
        return Builder()

class ChatRoomRepository:
    def find_by_sender_id_and_recipient_id(self, sender_id, recipient_id):
        pass

    def save(self, chat_room):
        pass

class ChatRoomService:
    def __init__(self, chat_room_repository: ChatRoomRepository):
        self.chat_room_repository = chat_room_repository

    def get_chat_room_id(self, sender_id, recipient_id, create_if_not_exists):
        chat_room_opt = self.chat_room_repository.find_by_sender_id_and_recipient_id(sender_id, recipient_id)
        if chat_room_opt is not None:
            return chat_room_opt
        elif create_if_not_exists:
            chat_id = f"{sender_id}_{recipient_id}"
            room1 = ChatRoom(chat_id, sender_id, recipient_id)
            room2 = ChatRoom(chat_id, recipient_id, sender_id)
            self.chat_room_repository.save(room1)
            self.chat_room_repository.save(room2)
            return chat_id
        else:
            return None

def test_get_chat_room_id_existing_room_public():
    sender_id = "alice"
    recipient_id = "bob"
    expected_chat_id = "alice_bob"
    existing_chat_room = ChatRoom.builder()\
        .chatId(expected_chat_id)\
        .senderId(sender_id)\
        .recipientId(recipient_id)\
        .build()

    repo = Mock(spec=ChatRoomRepository)
    repo.find_by_sender_id_and_recipient_id.return_value = expected_chat_id

    service = ChatRoomService(repo)

    result = service.get_chat_room_id(sender_id, recipient_id, False)

    assert result == expected_chat_id
    repo.save.assert_not_called()

def test_get_chat_room_id_new_room_create_if_not_exists_true_public():
    sender_id = "charlie"
    recipient_id = "dan"
    expected_chat_id = f"{sender_id}_{recipient_id}"

    repo = Mock(spec=ChatRoomRepository)
    repo.find_by_sender_id_and_recipient_id.return_value = None
    repo.save.side_effect = lambda room: room

    service = ChatRoomService(repo)

    result = service.get_chat_room_id(sender_id, recipient_id, True)

    assert result == expected_chat_id
    assert repo.save.call_count == 2

def test_get_chat_room_id_new_room_create_if_not_exists_false_public():
    sender_id = "eve"
    recipient_id = "frank"

    repo = Mock(spec=ChatRoomRepository)
    repo.find_by_sender_id_and_recipient_id.return_value = None

    service = ChatRoomService(repo)

    result = service.get_chat_room_id(sender_id, recipient_id, False)

    assert result is None
    repo.save.assert_not_called()