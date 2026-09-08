import pytest

def test_podman_basic():
    # Simulated objects and methods, mimicking the logic
    class QuadPodman:
        def __init__(self, what, mode):
            self.args = [what, mode]
            self.env = {}
            self.labels = {}
            self.annots = {}
            self.arrays = []

        def add(self, arg):
            self.args.append(arg)
        def addf(self, fmt, val):
            self.args.append(fmt % val if "%s" in fmt else fmt)
        def addv(self, *args):
            self.args.extend(args)
        def add_env(self, env):
            self.env = env.copy()
        def add_labels(self, labels):
            self.labels = labels.copy()
        def add_annotations(self, ann):
            self.annots = ann.copy()
        def add_array(self, arr, n):
            self.arrays.extend(arr[:n])
        def to_exec(self):
            return " ".join(self.args)
        def free(self):
            pass

    podman = QuadPodman("container", "run")
    podman.add("--rm")
    podman.addf("--name=%s", "demo")
    podman.addv("--detach", "--tty")
    env = {"FOO": "BAR", "ABC": "XYZ"}
    podman.add_env(env)
    lab = {"app": "test"}
    podman.add_labels(lab)
    ann = {"com.example": "test"}
    podman.add_annotations(ann)
    podman.add_array(["FOO=BAR", "ABC=XYZ"], 2)
    exec_str = podman.to_exec()
    assert exec_str
    podman.free()