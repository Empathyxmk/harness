package com.spotify.docker;

import com.spotify.docker.client.AnsiProgressHandler;
import com.spotify.docker.client.DockerClient;
import org.apache.maven.plugin.testing.AbstractMojoTestCase;
import org.mockito.ArgumentCaptor;

import java.io.File;

import static com.spotify.docker.TestUtils.getPom;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;

public class TagMojoPublicTest extends AbstractMojoTestCase {

  public void testTagAlpha() throws Exception {
    final File pom = getPom("/pom-tag2.xml"); // Use different logic, will do different asserts

    final TagMojo mojo = (TagMojo) lookupMojo("tag", pom);
    assertNotNull(mojo);
    final DockerClient docker = mock(DockerClient.class);
    final ArgumentCaptor<String> image = ArgumentCaptor.forClass(String.class);
    final ArgumentCaptor<String> name = ArgumentCaptor.forClass(String.class);
    mojo.execute(docker);
    verify(docker).tag(image.capture(), name.capture(), eq(false));
    assertEquals("imageToTag", image.getValue());
    // Instead of checking length like Tag2, check format
    final String[] split = name.getValue().split(":");
    assertEquals("newRepo", split[0]);
    assertTrue(split[1].matches("[a-f0-9]{7,}.*"));
  }

  public void testTagBeta() throws Exception {
    final File pom = getPom("/pom-tag3.xml");

    final TagMojo mojo = (TagMojo) lookupMojo("tag", pom);
    assertNotNull(mojo);
    final DockerClient docker = mock(DockerClient.class);
    mojo.execute(docker);
    verify(docker).tag("imageToTag", "newRepo:newTag", false);
  }

  public void testTagSkipTagPublic() throws Exception {
    final TagMojo mojo = (TagMojo) lookupMojo("tag",
        getPom("/pom-tag-skip-tag.xml"));
    assertThat(mojo).isNotNull();
    assertThat(mojo.isSkipDockerTag()).isTrue();

    final DockerClient docker = mock(DockerClient.class);
    mojo.execute(docker);

    verify(docker, never())
        .tag(anyString(), anyString(), anyBoolean());
  }

  public void testTagSkipDockerPublic() throws Exception {
    final TagMojo mojo = (TagMojo) lookupMojo("tag",
        getPom("/pom-tag-skip-docker.xml"));
    assertThat(mojo.isSkipDocker()).isTrue();

    final TagMojo mojoSpy = spy(mojo); // spy on it to verify method not called
    mojo.execute();

    verify(mojoSpy, never()).execute(any(DockerClient.class));
  }
}