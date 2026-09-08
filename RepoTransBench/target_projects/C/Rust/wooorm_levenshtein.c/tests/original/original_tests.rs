use levenshtein::{levenshtein, levenshtein_n};

fn assert_distance(input: &str, alternative: &str, expected: usize) {
    let res = levenshtein(input, alternative);
    let res_n = levenshtein_n(input, input.len(), alternative, alternative.len());
    
    assert_eq!(res, expected, 
        "For `{}` and `{}`. Expected `{}`, got `{}`", 
        input, alternative, expected, res);
        
    assert_eq!(res_n, expected, 
        "For `{}` and `{}`. Expected `{}`, got `{}`", 
        input, alternative, expected, res_n);
}

fn assert_distance_n(input: &str, input_n: usize, alternative: &str, alt_n: usize, expected: usize) {
    let res = levenshtein_n(input, input_n, alternative, alt_n);
    
    assert_eq!(res, expected, 
        "For `{}` and `{}`. Expected `{}`, got `{}`", 
        input, alternative, expected, res);
}

#[test]
fn test_original_cases() {
    // Existing tests
    assert_distance("", "a", 1);
    assert_distance("a", "", 1);
    assert_distance("", "", 0);
    assert_distance("levenshtein", "levenshtein", 0);
    assert_distance("sitting", "kitten", 3);
    assert_distance("gumbo", "gambol", 2);
    assert_distance("saturday", "sunday", 3);
    assert_distance("DwAyNE", "DUANE", 2);
    assert_distance("dwayne", "DuAnE", 5);
    assert_distance("aarrgh", "aargh", 1);
    assert_distance("aargh", "aarrgh", 1);
    assert_distance("a", "b", 1);
    assert_distance("ab", "ac", 1);
    assert_distance("ac", "bc", 1);
    assert_distance("abc", "axc", 1);
    assert_distance("xabxcdxxefxgx", "1ab2cd34ef5g6", 6);
    assert_distance("xabxcdxxefxgx", "abcdefg", 6);
    assert_distance("javawasneat", "scalaisgreat", 7);
    assert_distance("example", "samples", 3);
    assert_distance("sturgeon", "urgently", 6);
    assert_distance("levenshtein", "frankenstein", 6);
    assert_distance("distance", "difference", 5);

    // ------------------------------------------------------------------------
    // Coverage-specific edge cases:
    // 1. a and b are the same pointer (test a == b shortcut, even if non-empty)
    let ptr = "same";
    assert_distance_n(ptr, ptr.len(), ptr, ptr.len(), 0);

    // 2. Explicit coverage if only one arg is empty
    assert_distance_n("", 0, "abc", 3, 3);
    assert_distance_n("abc", 3, "", 0, 3);

    // 3. Test allocation failure edge - not applicable in Rust version

    // 4. Zero-length input, both ways, distinct pointers
    let e1 = "";
    let e2 = "";
    assert_distance_n(e1, 0, e2, 0, 0);

    // 5. Single character, mismatch
    assert_distance_n("a", 1, "b", 1, 1);

    // 6. Large length (length > 1), but no overlap
    assert_distance_n("abc", 3, "def", 3, 3);

    // 7. Check upper/lower branch in main edit distance loop (via substitutions, insertions, deletions)
    assert_distance_n("kitten", 6, "sitting", 7, 3);
}