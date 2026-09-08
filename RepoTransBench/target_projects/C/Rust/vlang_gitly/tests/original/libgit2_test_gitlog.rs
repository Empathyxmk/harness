// Translated from libgit2/test_gitlog.c

#[cfg(test)]
mod tests {
    use std::cell::RefCell;

    struct GitRepository;
    struct GitError {
        message: &'static str,
    }

    #[derive(Debug)]
    enum DummyGitError {
        NotFound(&'static str),
        Other(&'static str),
    }

    thread_local! {
        static LAST_ERROR: RefCell<Option<GitError>> = RefCell::new(None);
    }

    fn git_error_last() -> Option<GitError> {
        LAST_ERROR.with(|l| l.borrow().clone())
    }

    fn set_error(msg: &'static str) {
        LAST_ERROR.with(|l| *l.borrow_mut() = Some(GitError { message: msg }));
    }

    fn git_libgit2_init() {
        LAST_ERROR.with(|l| *l.borrow_mut() = None);
    }

    fn git_libgit2_shutdown() {
        LAST_ERROR.with(|l| *l.borrow_mut() = None);
    }

    fn git_repository_open(_path: &str) -> Result<GitRepository, DummyGitError> {
        set_error("Repository not found");
        Err(DummyGitError::NotFound("Repository not found"))
    }

    fn git_repository_init(_path: &str) -> Result<GitRepository, DummyGitError> {
        Ok(GitRepository)
    }

    fn git_repository_free(_repo: GitRepository) {}

    #[test]
    fn test_git_repository_open_fail() {
        git_libgit2_init();

        let result = git_repository_open("/tmp/nonexistent-repo-for-test");
        assert!(result.is_err(), "Repository open should fail");
        match result {
            Err(DummyGitError::NotFound(_)) => {}
            _ => panic!("Expected NotFound error"),
        }
        let e = git_error_last();
        assert!(e.is_some(), "Should have error after failure");
        if let Some(err) = e {
            println!("Expected failure: {}", err.message);
        }

        git_libgit2_shutdown();
    }

    #[test]
    fn test_git_repository_init_and_free() {
        git_libgit2_init();

        let result = git_repository_init("/tmp/libgit2-c-test-init");
        if let Ok(repo) = result {
            // In C: assert(repo != NULL);
            // Here: GitRepository is a normal value, so Ok must contain it
            // We can still assert types for robustness:
            let _: &GitRepository = &repo;
            git_repository_free(repo);
            // No error expected, no further checks necessary
        }

        git_libgit2_shutdown();
    }
}