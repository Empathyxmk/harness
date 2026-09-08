package com.spotify.docker;

import com.spotify.docker.client.exceptions.DockerException;
import org.apache.maven.plugin.MojoExecutionException;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.io.IOException;

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.mockito.Mockito.when;

public class GitPublicTest {

  @Mock private org.eclipse.jgit.lib.Repository repository;
  @Mock private org.eclipse.jgit.lib.RefDatabase refDb;

  @Before
  public void setUp() {
    MockitoAnnotations.initMocks(this);
  }

  @Test(expected = MojoExecutionException.class)
  public void testGetCommitId_WhenRepoStillNull_ThrowsException()
      throws IOException, DockerException, GitAPIException, MojoExecutionException {
    final Git git = new Git();
    git.setRepo(null); // Explicitly null
    git.getCommitId();
  }

  @Test
  public void testGetCommitId_WhenHeadIsMissing_ReturnsNull()
      throws IOException, DockerException, GitAPIException, MojoExecutionException {
    when(repository.resolve("HEAD")).thenReturn(null); // Mock HEAD not set
    final Git git = new Git();
    git.setRepo(repository);
    String commitId = git.getCommitId();
    assertThat(commitId, is(equalTo(null)));
  }
}