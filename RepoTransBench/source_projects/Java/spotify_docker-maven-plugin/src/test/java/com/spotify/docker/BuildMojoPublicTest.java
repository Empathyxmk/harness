package com.spotify.docker;

import com.spotify.docker.client.DockerClient;
import org.apache.maven.plugin.testing.AbstractMojoTestCase;

import java.io.File;

import static com.spotify.docker.TestUtils.getPom;
import static org.mockito.Mockito.*;

public class BuildMojoPublicTest extends AbstractMojoTestCase {

  public void testBuildMojoWithNoPushPublic() throws Exception {
    File pom = getPom("/pom-build-skip-push.xml");
    BuildMojo mojo = (BuildMojo) lookupMojo("build", pom);
    assertNotNull(mojo);

    DockerClient docker = mock(DockerClient.class);
    mojo.execute(docker);

    // No push call should be made
    verify(docker, never()).push(anyString());
  }

  public void testBuildMojoSkipBuildPublic() throws Exception {
    File pom = getPom("/pom-build-skip-build.xml");
    BuildMojo mojo = (BuildMojo) lookupMojo("build", pom);
    assertNotNull(mojo);

    DockerClient docker = mock(DockerClient.class);
    mojo.execute(docker);

    // Should not attempt to build if skipped
    verify(docker, never()).build(any(File.class), anyString());
  }
}