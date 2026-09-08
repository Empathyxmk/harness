package com.spotify.docker;

import com.spotify.docker.client.DockerClient;
import org.apache.maven.plugin.testing.AbstractMojoTestCase;

import java.io.File;

import static com.spotify.docker.TestUtils.getPom;
import static org.mockito.Mockito.*;

public class PushMojoPublicTest extends AbstractMojoTestCase {
  public void testPushMojoSkippedDockerPublic() throws Exception {
    final File pom = getPom("/pom-push-skip-docker.xml");
    final PushMojo mojo = (PushMojo) lookupMojo("push", pom);
    assertNotNull(mojo);
    // Should skip execution altogether, so spy to check
    PushMojo mocha = spy(mojo);
    mocha.execute();
    verify(mocha, never()).execute(any(DockerClient.class));
  }

  public void testPushMojoSkippedPushPublic() throws Exception {
    final File pom = getPom("/pom-push-skip-push.xml");
    final PushMojo mojo = (PushMojo) lookupMojo("push", pom);
    assertNotNull(mojo);
    final DockerClient docker = mock(DockerClient.class);
    mojo.execute(docker);
    // Should not push
    verify(docker, never()).push(anyString());
  }
}