package com.spotify.docker;

import org.junit.Test;
import static org.junit.Assert.*;

public class AbstractDockerMojoPublicTest {

    @Test
    public void testRegistryUrlReplacePublic() {
        AbstractDockerMojo mojo = new AbstractDockerMojo() {};
        String url = mojo.replaceRegistryUrl("index.docker.io", "my.other.io");
        assertEquals("my.other.io", url);
    }

    // The method is protected; additional more complex logic would need subclassing as needed
}