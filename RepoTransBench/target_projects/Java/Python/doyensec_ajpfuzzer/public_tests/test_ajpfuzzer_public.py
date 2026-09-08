from src.ajpfuzzer.ajpfuzzer import AJPFuzzer

def test_main_no_crash():
    AJPFuzzer.main(["--version"])
    AJPFuzzer.main([])