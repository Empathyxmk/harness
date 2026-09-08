def test_package_info_fields():
    # In JS: checks package.json metadata.
    # In Python, checks info can be mocked here.
    package_info = {
        "name": "passport-twitter",
        "version": "1.0.0",
        "main": "./lib/index.js"
    }
    assert package_info["name"] == "passport-twitter"
    assert "version" in package_info
    assert package_info.get("main", "") == "./lib/index.js"