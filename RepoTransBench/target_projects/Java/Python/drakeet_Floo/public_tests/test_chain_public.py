def test_chain_proceed_returns_data_public():
    class Chain:
        def proceed(self, input_):
            return input_ + "_public"
    chain = Chain()
    result = chain.proceed("hello")
    assert result == "hello_public"

def test_chain_proceed_with_different_data_public():
    class Chain:
        def proceed(self, input_):
            return input_ + 42
    chain = Chain()
    result = chain.proceed(8)
    assert result == 50