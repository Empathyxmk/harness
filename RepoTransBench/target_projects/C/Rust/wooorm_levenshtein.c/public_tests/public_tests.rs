use levenshtein::levenshtein;

#[test]
fn test_public_cases() {
    // PUBLIC TEST CASES - different strings/values from private test.c
    assert_eq!(levenshtein("cat", "cut"), 1, "For `cat` and `cut`. Expected `1`, got `{}`", levenshtein("cat", "cut"));
    assert_eq!(levenshtein("kitten", "sitting"), 3, "For `kitten` and `sitting`. Expected `3`, got `{}`", levenshtein("kitten", "sitting"));
    assert_eq!(levenshtein("book", "back"), 2, "For `book` and `back`. Expected `2`, got `{}`", levenshtein("book", "back"));
    assert_eq!(levenshtein("intention", "execution"), 5, "For `intention` and `execution`. Expected `5`, got `{}`", levenshtein("intention", "execution"));
    assert_eq!(levenshtein("", "a"), 1, "For `\"\"` and `a`. Expected `1`, got `{}`", levenshtein("", "a"));
    assert_eq!(levenshtein("a", ""), 1, "For `a` and `\"\"`. Expected `1`, got `{}`", levenshtein("a", ""));
    assert_eq!(levenshtein("", ""), 0, "For empty strings. Expected `0`, got `{}`", levenshtein("", ""));
    assert_eq!(levenshtein("sunday", "saturday"), 3, "For `sunday` and `saturday`. Expected `3`, got `{}`", levenshtein("sunday", "saturday"));
    assert_eq!(levenshtein("abcdef", "azced"), 3, "For `abcdef` and `azced`. Expected `3`, got `{}`", levenshtein("abcdef", "azced"));
    assert_eq!(levenshtein("gumbo", "gambol"), 2, "For `gumbo` and `gambol`. Expected `2`, got `{}`", levenshtein("gumbo", "gambol"));
    assert_eq!(levenshtein("flaw", "lawn"), 2, "For `flaw` and `lawn`. Expected `2`, got `{}`", levenshtein("flaw", "lawn"));
    assert_eq!(levenshtein("night", "nacht"), 2, "For `night` and `nacht`. Expected `2`, got `{}`", levenshtein("night", "nacht"));
    assert_eq!(levenshtein("drive", "dives"), 2, "For `drive` and `dives`. Expected `2`, got `{}`", levenshtein("drive", "dives"));
    assert_eq!(levenshtein("apple", "apples"), 1, "For `apple` and `apples`. Expected `1`, got `{}`", levenshtein("apple", "apples"));
    assert_eq!(levenshtein("plane", "plan"), 1, "For `plane` and `plan`. Expected `1`, got `{}`", levenshtein("plane", "plan"));
    assert_eq!(levenshtein("mist", "must"), 1, "For `mist` and `must`. Expected `1`, got `{}`", levenshtein("mist", "must"));
    assert_eq!(levenshtein("rose", "rows"), 2, "For `rose` and `rows`. Expected `2`, got `{}`", levenshtein("rose", "rows"));
    assert_eq!(levenshtein("seat", "seats"), 1, "For `seat` and `seats`. Expected `1`, got `{}`", levenshtein("seat", "seats"));
    assert_eq!(levenshtein("music", "mosaic"), 3, "For `music` and `mosaic`. Expected `3`, got `{}`", levenshtein("music", "mosaic"));
    assert_eq!(levenshtein("draw", "drew"), 1, "For `draw` and `drew`. Expected `1`, got `{}`", levenshtein("draw", "drew"));
    assert_eq!(levenshtein("rat", "tar"), 2, "For `rat` and `tar`. Expected `2`, got `{}`", levenshtein("rat", "tar"));
    assert_eq!(levenshtein("pale", "bake"), 2, "For `pale` and `bake`. Expected `2`, got `{}`", levenshtein("pale", "bake"));
    assert_eq!(levenshtein("cheese", "chase"), 2, "For `cheese` and `chase`. Expected `2`, got `{}`", levenshtein("cheese", "chase"));
    assert_eq!(levenshtein("tale", "table"), 1, "For `tale` and `table`. Expected `1`, got `{}`", levenshtein("tale", "table"));
    assert_eq!(levenshtein("host", "ghosts"), 2, "For `host` and `ghosts`. Expected `2`, got `{}`", levenshtein("host", "ghosts"));
    assert_eq!(levenshtein("random", "rand"), 2, "For `random` and `rand`. Expected `2`, got `{}`", levenshtein("random", "rand"));
    assert_eq!(levenshtein("find", "found"), 1, "For `find` and `found`. Expected `1`, got `{}`", levenshtein("find", "found"));
    assert_eq!(levenshtein("lead", "load"), 1, "For `lead` and `load`. Expected `1`, got `{}`", levenshtein("lead", "load"));
    assert_eq!(levenshtein("digit", "digit"), 0, "For `digit` and `digit`. Expected `0`, got `{}`", levenshtein("digit", "digit"));
    assert_eq!(levenshtein("abc", "cba"), 2, "For `abc` and `cba`. Expected `2`, got `{}`", levenshtein("abc", "cba"));
}