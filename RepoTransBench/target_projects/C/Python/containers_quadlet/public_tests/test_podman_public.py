import pytest

def test_podman_basic_public():
    # Simulated podman object for the "public" mode test
    class QuadPodman:
        def __init__(self, what, mode):
            self.args = [what, mode]
            self.env = {}
            self.labels = {}

        def add(self, arg):
            self.args.append(arg)
        def addf(self, fmt, val):
            self.args.append(fmt.replace("%s", val))
        def addv(self, *args):
            self.args.extend(args)
        def add_env(self, env):
            self.env = env.copy()
        def add_labels(self, labels):
            self.labels = labels.copy()
        def free(self):
            pass

    podman = QuadPodman("container", "exec")
    podman.add("--interactive")
    podman.addf("--name=%s", "public")
    podman.addv("--user", "--privileged")
    env = {"HELLO": "WORLD", "SAMPLE": "VALUE"}
    podman.add_env(env)
    lab = {"env": "prod"}
    podman.add_labels(lab)
    podman.free()