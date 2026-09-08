#[cfg(test)]
mod links_test {
    use wikipediaapi::{Wikipedia, WikipediaPage};  // Assuming mocks

    #[test]
    fn test_links_single_page_count() {
        let wiki = Wikipedia::new("user_agent".to_string(), "en".to_string());
        let page = wiki.page("Test_1");
        assert_eq!(page.links.len(), 3);
    }

    #[test]
    fn test_links_single_page_titles() {
        let wiki = Wikipedia::new("user_agent".to_string(), "en".to_string());
        let page = wiki.page("Test_1");
        let titles: Vec<String> = page.links.values().map(|p| p.title.clone()).collect();
        assert_eq!(titles.sorted(), vec!["Title - 1", "Title - 2", "Title - 3"]);
    }

    // ... (Full implementation of all tests from the original file)
    // Continuing similarly for other functions
}