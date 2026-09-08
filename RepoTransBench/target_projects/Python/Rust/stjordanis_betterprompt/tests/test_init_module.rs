use betterprompt::meta::__all__;
use std::collections::HashMap;

#[test]
fn test_all_exports() {
    for &name in __all__ {
        // Try to check that top-level module symbols exist (simulate hasattr)
        // We'll just check they compile/access by name in this context
        match name {
            "get_from_dict_or_env" => {
                let mut d = HashMap::new();
                d.insert("SOMEKEY".to_string(), "someval".to_string());
                let _ = betterprompt::get_from_dict_or_env("SOMEKEY", Some(&d));
            }
            "calculate_perplexity" => {
                let _ = betterprompt::calculate_perplexity(&[0.0f64, 1.0]);
            }
            "call_openai" => {
                // (This will call dummy just fine)
                let _ = betterprompt::call_openai("hello", None, None);
            }
            "DummyOpenAICompletion" => {
                let _ = betterprompt::DummyOpenAICompletion::create();
            }
            "openai" => {
                // Not strictly available, but OPENAI global exists
                let _ = &betterprompt::OPENAI;
            }
            _ => panic!("Missing export: {}", name),
        }
    }
}