use homu_rust::parse_issue_comment::*;
static COMMIT: &str = "5ffafdb1e94fa87334d4851a57564425e11a569e";
static OTHER_COMMIT: &str = "4e4c9ddd781729173df2720d83e0f4d1b0102a94";

fn find_action(commands: &[Command], action: &str) -> Vec<&Command> {
    commands.iter().filter(|c| c.action == action).collect()
}

#[test]
fn test_r_plus() {
    let author = "jack";
    let body = "@bors r+";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jack");
}

#[test]
fn test_r_plus_with_colon() {
    let author = "jack";
    let body = "@bors: r+";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jack");
    assert_eq!(command.commit, COMMIT);
}

#[test]
fn test_r_plus_with_sha() {
    let author = "jack";
    let body = format!("@bors r+ {}", OTHER_COMMIT);
    let commands = parse_issue_comment(author, &body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jack");
    assert_eq!(command.commit, OTHER_COMMIT);
}

#[test]
fn test_r_equals() {
    let author = "jack";
    let body = "@bors r=jill";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jill");
}

#[test]
fn test_r_equals_at_user() {
    let author = "jack";
    let body = "@bors r=@jill";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jill");
}

#[test]
fn test_hidden_r_equals() {
    let author = "bors";
    let body = format!(
        ":pushpin: Commit {} has been approved by `jack`\nIt is now in the [queue]({}) for this repository.\n\n<!-- @bors r=jack {} -->",
        COMMIT, "rust", COMMIT
    );
    let commands = parse_issue_comment(author, &body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "approve");
    assert_eq!(command.actor, "jack");
    assert_eq!(command.commit, COMMIT);
}

#[test]
fn test_r_me() {
    let author = "jack";
    let body = "@bors r=me";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 0);
}

#[test]
fn test_r_minus() {
    let author = "jack";
    let body = "@bors r-";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "unapprove");
}

#[test]
fn test_priority() {
    let author = "jack";
    let body = "@bors p=5";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "prioritize");
    assert_eq!(command.priority, Some(5));
}

#[test]
fn test_approve_and_priority() {
    let author = "jack";
    let body = "@bors r+ p=5";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    let approve_commands = find_action(&commands, "approve");
    let prioritize_commands = find_action(&commands, "prioritize");
    assert_eq!(approve_commands.len(), 1);
    assert_eq!(prioritize_commands.len(), 1);
    assert_eq!(approve_commands[0].actor, "jack");
    assert_eq!(prioritize_commands[0].priority, Some(5));
}

#[test]
fn test_approve_specific_and_priority() {
    let author = "jack";
    let body = format!("@bors r+ {} p=5", OTHER_COMMIT);
    let commands = parse_issue_comment(author, &body, COMMIT, "bors");
    let approve_commands = find_action(&commands, "approve");
    let prioritize_commands = find_action(&commands, "prioritize");
    assert_eq!(approve_commands.len(), 1);
    assert_eq!(prioritize_commands.len(), 1);
    assert_eq!(approve_commands[0].actor, "jack");
    assert_eq!(approve_commands[0].commit, OTHER_COMMIT);
    assert_eq!(prioritize_commands[0].priority, Some(5));
}

#[test]
fn test_delegate_plus() {
    let author = "jack";
    let body = "@bors delegate+";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "delegate-author");
}

#[test]
fn test_delegate_equals() {
    let author = "jack";
    let body = "@bors delegate=jill";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "delegate");
    assert_eq!(command.delegate_to, Some("jill".to_string()));
}

#[test]
fn test_delegate_equals_at_user() {
    let author = "jack";
    let body = "@bors delegate=@jill";
    let commands = parse_issue_comment(author, body, COMMIT, "bors");
    assert_eq!(commands.len(), 1);
    let command = &commands[0];
    assert_eq!(command.action, "delegate");
    assert_eq!(command.delegate_to, Some("jill".to_string()));
}