use nickjj_ansible_docker::host_mock::*;
use regex::Regex;

// To simulate pytest's fixture
fn setup_host() -> DummyHost {
    DummyHost::new()
}

#[test]
fn test_docker_version() {
    let host = setup_host();
    assert_eq!(0, host.run("docker --version").rc);
}

#[test]
fn test_pinned_docker_version() {
    let host = setup_host();
    let existing_docker_version = host.check_output("docker --version");
    host.run("sudo apt-get update");
    host.run("sudo apt-get upgrade");
    let docker_version_after_apt_update = host.check_output("docker --version");
    assert_eq!(existing_docker_version, docker_version_after_apt_update);
}

#[test]
fn test_docker_compose_v2_version() {
    let host = setup_host();
    assert_eq!(0, host.run("docker compose version").rc);
}

#[test]
fn test_pinned_docker_compose_v2_version() {
    let host = setup_host();
    let existing_docker_compose_version = host.check_output("docker compose version");
    host.run("sudo apt-get update");
    host.run("sudo apt-get upgrade");
    let docker_compose_version_after_apt_update = host.check_output("docker compose version");
    assert_eq!(existing_docker_compose_version, docker_compose_version_after_apt_update);
}

#[test]
fn test_able_to_access_docker_without_root() {
    let host = setup_host();
    assert!(host.user("test").groups.contains(&"docker".to_string()));
}

#[test]
fn test_daemon_json_is_configured() {
    let host = setup_host();
    let daemon_json = host.file("/etc/docker/daemon.json");
    assert!(daemon_json.contains("journald"));
    assert!(daemon_json.contains("8.8.8.8"));
}

#[test]
fn test_customized_environment_systemd_unit_file() {
    let host = setup_host();
    let unit_file = "/etc/systemd/system/docker.service.d/environment.conf";
    let file_contents = host.file(unit_file).content_string;
    let re_http = Regex::new(r#"Environment="HTTP_PROXY=.*""#).unwrap();
    let re_https = Regex::new(r#"Environment="HTTPS_PROXY=.*""#).unwrap();
    assert!(re_http.is_match(&file_contents));
    assert!(re_https.is_match(&file_contents));
}

#[test]
fn test_customized_daemon_flags_systemd_unit_file() {
    let host = setup_host();
    let unit_file = "/etc/systemd/system/docker.service.d/options.conf";
    let file_contents = host.file(unit_file).content_string;
    assert!(file_contents.contains("-H fd://"));
    assert!(file_contents.contains("--debug"));
}

#[test]
fn test_customized_systemd_override() {
    let host = setup_host();
    let unit_file = "/etc/systemd/system/docker.service.d/custom.conf";
    let file_contents = host.file(unit_file).content_string;
    assert!(file_contents.contains("ATest"));
}

#[test]
fn test_docker_clean_up_cron_job() {
    let host = setup_host();
    let cron_conf = host.file("/etc/cron.d/docker-disk-clean-up").content_string;
    assert!(cron_conf.contains("test docker system prune -af"));
}

#[test]
fn test_python_docker_module() {
    let host = setup_host();
    assert_eq!(0, host.run("python3-docker -c 'import docker'").rc);
}

#[test]
fn test_daemon_json_missing_keys() {
    let host = setup_host();
    let f = host.file("/wrong/path");
    assert!(!f.contains("journald"));
    assert!(!f.contains("8.8.8.8"));
}

#[test]
fn test_customized_environment_systemd_unit_file_missing_keys() {
    let host = setup_host();
    let file_contents = host.file("/wrong/path").content_string;
    let re_http = Regex::new(r#"Environment="HTTP_PROXY=.*""#).unwrap();
    let re_https = Regex::new(r#"Environment="HTTPS_PROXY=.*""#).unwrap();
    assert!(!re_http.is_match(&file_contents));
    assert!(!re_https.is_match(&file_contents));
}

#[test]
fn test_file_object_empty() {
    let host = setup_host();
    assert_eq!("", host.file("/nonexistent/path").content_string);
}

#[test]
fn test_user_without_docker_group() {
    struct NoDockerUser;
    impl NoDockerUser {
        fn groups(&self) -> Vec<String> {
            vec!["test".to_string()]
        }
    }
    struct NoDockerHost;
    impl NoDockerHost {
        fn user(&self, _name: &str) -> NoDockerUser {
            NoDockerUser
        }
    }
    let h = NoDockerHost;
    assert!(!h.user("test").groups().contains(&"docker".to_string()));
}