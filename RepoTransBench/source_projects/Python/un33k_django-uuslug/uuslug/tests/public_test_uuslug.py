import uuslug.uuslug as uuslug_mod

def test_slugify_all_ascii_public():
    # Different phrase than in original test for variety
    input_str = "Hello World: Testing Slugify!"
    slug = uuslug_mod.slugify(input_str)
    assert slug == "hello-world-testing-slugify"

def test_slugify_allowed_chars_public():
    # Testing a string with different allowed chars and digits
    input_str = "Python_3! Test #Slug"
    slug = uuslug_mod.slugify(input_str, allowed_chars="-_")
    assert slug == "python_3-test-slug"

def test_slugify_stopwords_public():
    # Using different stopwords and input
    input_str = "Skip the quick brown fox"
    slug = uuslug_mod.slugify(input_str, stopwords=["skip", "the"])
    assert slug == "quick-brown-fox"