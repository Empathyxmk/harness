from src.ajpfuzzer.ajpfuzzer import AJPFuzzer

def test_main_handles_args():
    AJPFuzzer.main(["test", "case"])