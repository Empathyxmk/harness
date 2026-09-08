package com.spotify.docker;

import com.spotify.docker.client.DockerClient;
import org.apache.maven.plugin.testing.AbstractMojoTestCase;

import java.io.File;

import static com.spotify.docker.TestUtils.getPom;
import static org.mockito.Mockito.*;

public class RemoveImageMojoPublicTest extends AbstractMojoTestCase {

  public void testRemoveImageBasicPublic() throws Exception {
    final File pom = getPom("/pom-removeImage.xml");
    final RemoveImageMojo mojo = (RemoveImageMojo) lookupMojo("removeImage", pom);
    assertNotNull(mojo);

    DockerClient docker = mock(DockerClient.class);
    when(docker.inspectImage("imageToRemove")).thenReturn(null);
    mojo.execute(docker); // Expect no exception even if image is missing
    verify(docker, atLeast(0)).removeImage(anyString(), anyBoolean(), anyBoolean());
  }

  public void testRemoveMultipleImagesPublic() throws Exception {
    final File pom = getPom("/pom-removeMultipleImages.xml");
    final RemoveImageMojo mojo = (RemoveImageMojo) lookupMojo("removeImage", pom);
    assertNotNull(mojo);

    DockerClient docker = mock(DockerClient.class);
    when(docker.inspectImage(anyString())).thenReturn(null);
    mojo.execute(docker); // No exception on missing images
    verify(docker, atLeast(0)).removeImage(anyString(), anyBoolean(), anyBoolean());
  }
}