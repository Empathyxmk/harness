def test_MainPublic():
    class Main:
        @staticmethod
        def main(args):
            pass
    Main.main(["public"])