def test_HelloWorldStateContext():
    class HelloWorldStateContext:
        def __init__(self):
            self.words = []
            self.finalized = False

        def appendWord(self, word):
            if not self.finalized:
                self.words.append(word)
                if len(self.words) >= 2:
                    self.finalized = True

        def helloWorld(self):
            if len(self.words) == 1:
                return self.words[0] + " "
            if len(self.words) >= 2:
                return self.words[0] + " " + self.words[1] + "!"
            return ""

    ctx = HelloWorldStateContext()
    ctx.appendWord("Hello")
    assert ctx.helloWorld() == "Hello "
    ctx.appendWord("State")
    assert ctx.helloWorld() == "Hello State!"
    ctx.appendWord("Whatever")
    assert ctx.helloWorld() == "Hello State!"