import io

# Event types
class JustAfterLaunch: pass
class BeforeTheEnd: pass
class ReadingManga:
    def __init__(self, title):
        self.title = title

# Handler types
class CoutWhisperer:
    @staticmethod
    def handle(event):
        if isinstance(event, JustAfterLaunch):
            print("Welcome!")
        elif isinstance(event, BeforeTheEnd):
            print("Farewell!")
        elif isinstance(event, ReadingManga):
            print("Manga!")

class SilentPerson:
    pass

class MangaFan:
    @staticmethod
    def handle(event):
        if isinstance(event, ReadingManga):
            print(f"I enjoy {event.title}!")

# Meta-programming helpers
class type_list:
    def __init__(self, *types): self.types = types

def has_tail(typelist): return len(typelist.types) > 0

class Dispatcher:
    def __init__(self, listeners): self.listeners = listeners
    def post(self, evt):
        for listener in self.listeners.types:
            handler = getattr(listener, 'handle', None)
            if callable(handler):
                handler(evt)

class different_count:
    def __init__(self, typelist):
        self.value = len(set(typelist.types))

def test_public_case_study_2_public(capsys):
    listeners_A = type_list(SilentPerson)
    repr_A = "type_list<SilentPerson>"
    listeners_B = type_list(CoutWhisperer, SilentPerson, MangaFan)
    repr_B = "type_list<CoutWhisperer, SilentPerson, MangaFan>"
    dispatcher_A = Dispatcher(listeners_A)
    dispatcher_B = Dispatcher(listeners_B)

    dispatcher_A.post(JustAfterLaunch())
    dispatcher_B.post(JustAfterLaunch())
    print()
    print(f"{repr_A} has tail: {'true' if has_tail(listeners_A) else 'false'}")
    print(f"{repr_B} has tail: {'true' if has_tail(listeners_B) else 'false'}")
    print()
    naruto = ReadingManga("Naruto")
    dispatcher_A.post(naruto)
    dispatcher_B.post(naruto)
    print()
    print(f"{repr_A} has count: {different_count(listeners_A).value}")
    print(f"{repr_B} has count: {different_count(listeners_B).value}")
    print(f"type_list<> has count: {different_count(type_list()).value}")
    print()
    dispatcher_A.post(BeforeTheEnd())
    dispatcher_B.post(BeforeTheEnd())

    out = capsys.readouterr().out.strip().split('\n')
    expected = [
        "Welcome!",
        "",
        "type_list<SilentPerson> has tail: true",
        "type_list<CoutWhisperer, SilentPerson, MangaFan> has tail: true",
        "",
        "Manga!",
        "I enjoy Naruto!",
        "",
        "type_list<SilentPerson> has count: 1",
        "type_list<CoutWhisperer, SilentPerson, MangaFan> has count: 3",
        "type_list<> has count: 0",
        "",
        "Farewell!"
    ]
    # blank lines must be kept, so above matches the C++ test printout order
    assert out == expected