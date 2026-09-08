use claude_to_chatgpt::logger::{get_logger, DummyLogger};
use log::LevelFilter;

#[test]
fn test_logger_importable() {
    let logger = get_logger("claude_to_chatgpt");
    assert_eq!(logger.name(), "claude_to_chatgpt");
    logger.set_level(LevelFilter::Info);
    assert_eq!(logger.get_level(), LevelFilter::Info);
}