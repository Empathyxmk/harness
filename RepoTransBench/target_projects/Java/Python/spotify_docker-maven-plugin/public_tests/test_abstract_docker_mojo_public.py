class AbstractDockerMojo:
    def replaceRegistryUrl(self, old, new):
        return new

def test_registry_url_replace_public():
    mojo = AbstractDockerMojo()
    url = mojo.replaceRegistryUrl("index.docker.io", "my.other.io")
    assert url == "my.other.io"