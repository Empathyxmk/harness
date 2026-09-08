use betterprompt::meta::__all__;

#[test]
fn test_public_all_exports() {
    for &name in __all__ {
        // Just check it's referenced in meta (simulate public __dict__ access)
        match name {
            "get_from_dict_or_env" | "calculate_perplexity" | "call_openai" | "DummyOpenAICompletion" | "openai" => { /* exists */ }
            _ => panic!("Unexpected export: {}", name),
        }
    }
}