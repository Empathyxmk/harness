from shshsh.pipe import Pipe

def test_public_pipe_context_manager():
    with Pipe() as p:
        assert hasattr(p, "in_fd")
        assert hasattr(p, "out_fd")
        assert p.in_fd != p.out_fd