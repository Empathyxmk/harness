def import_decorator():
    from src.Structural.Decorator import Book, gift_wrap, hardbind_book
    return Book, gift_wrap, hardbind_book

def test_gift_wrapped():
    Book, gift_wrap, _ = import_decorator()
    alchemist = gift_wrap(Book('The Alchemist', 'Paulo Coelho', 10))
    assert alchemist.is_gift_wrapped
    assert alchemist.unwrap() == 'Unwrapped The Alchemist by Paulo Coelho'

def test_hard_bound():
    Book, _, hardbind_book = import_decorator()
    inferno = hardbind_book(Book('Inferno', 'Dan Brown', 15))
    assert inferno.is_hardbound
    assert inferno.price == 20