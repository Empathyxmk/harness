use claude_to_chatgpt::logger::{get_logger, DummyLogger};
use log::LevelFilter;

#[test]
fn test_public_get_logger_level() {
    let logger = get_logger("publicLoggerTest");
    logger.set_level(LevelFilter::Error);
    assert_eq!(logger.get_level(), LevelFilter::Error);
}

#[test]
fn test_public_get_logger_name() {
    let logger_name = "unique_logger_name";
    let logger = get_logger(logger_name);
    assert_eq!(logger.name(), logger_name);
}