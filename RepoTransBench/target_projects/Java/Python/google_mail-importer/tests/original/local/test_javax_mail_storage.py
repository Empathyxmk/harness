def test_iterator_simple():
    class JavaxMailStorage:
        def __init__(self, folder):
            self.folder = folder

        def __len__(self):
            return len(self.folder["messages"])

        def __iter__(self):
            return iter(self.folder["messages"])

    folder = {"messages": [object() for _ in range(5)]}
    javax_mail_storage = JavaxMailStorage(folder)
    assert len(javax_mail_storage) == 5


def test_iterator_with_subfolders():
    # Simulate subfolders as nested dicts
    def make_folder_with_messages(num_messages, *folders):
        messages = [object() for _ in range(num_messages)]
        subfolders = folders
        return {"messages": messages, "subfolders": list(subfolders)}

    def count_messages(folder):
        count = len(folder["messages"])
        for sub in folder["subfolders"]:
            count += count_messages(sub)
        return count

    # build a folder tree with known total messages
    f1 = make_folder_with_messages(10)
    f2 = make_folder_with_messages(6, make_folder_with_messages(9), make_folder_with_messages(3))
    f3 = make_folder_with_messages(
        15, f2, make_folder_with_messages(0, make_folder_with_messages(0, make_folder_with_messages(5)))
    )
    f0 = make_folder_with_messages(
        5, f1, f3, make_folder_with_messages(7)
    )

    total_expected = count_messages(f0)

    class JavaxMailStorage:
        def __init__(self, folder):
            self.folder = folder

        def __len__(self):
            return count_messages(self.folder)

    javax_mail_storage = JavaxMailStorage(f0)
    assert len(javax_mail_storage) == total_expected


def test_iterator_pathological_no_messages():
    def make_folder_with_messages(num_messages, *folders):
        messages = [object() for _ in range(num_messages)]
        subfolders = folders
        return {"messages": messages, "subfolders": list(subfolders)}

    def count_messages(folder):
        count = len(folder["messages"])
        for sub in folder["subfolders"]:
            count += count_messages(sub)
        return count

    # Tree with all zero messages
    f1 = make_folder_with_messages(0)
    f2 = make_folder_with_messages(
        0, make_folder_with_messages(0), make_folder_with_messages(
            0,
            make_folder_with_messages(0), make_folder_with_messages(0)),
        make_folder_with_messages(0,
            make_folder_with_messages(0, make_folder_with_messages(0, make_folder_with_messages(0)))))
    f0 = make_folder_with_messages(
        0, f1, f2, make_folder_with_messages(0)
    )

    class JavaxMailStorage:
        def __init__(self, folder):
            self.folder = folder

        def __len__(self):
            return count_messages(self.folder)

    javax_mail_storage = JavaxMailStorage(f0)
    assert len(javax_mail_storage) == 0


def test_iterator_get_without_looking():
    # Single message in nested subfolder
    def make_folder_with_messages(num_messages, *folders):
        messages = [object() for _ in range(num_messages)]
        subfolders = folders
        return {"messages": messages, "subfolders": list(subfolders)}

    nested = make_folder_with_messages(
        0, make_folder_with_messages(0),
        make_folder_with_messages(0, make_folder_with_messages(0), make_folder_with_messages(1))
    )

    class JavaxMailStorage:
        def __init__(self, folder):
            self.folder = folder

        def __iter__(self):
            # Flatten all messages recursively
            def gather(folder):
                for msg in folder["messages"]:
                    yield msg
                for sub in folder["subfolders"]:
                    yield from gather(sub)
            return gather(self.folder)

    javax_mail_storage = JavaxMailStorage(nested)
    first = next(iter(javax_mail_storage))
    assert first is not None