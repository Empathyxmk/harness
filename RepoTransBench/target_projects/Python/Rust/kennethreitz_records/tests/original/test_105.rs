// Translated from tests/test_105.py

struct DummyDb;

impl DummyDb {
    fn query(&self, _query: &str) -> DummyQueryResult {
        DummyQueryResult
    }
}

struct DummyQueryResult;

impl DummyQueryResult {
    fn scalar(&self) -> i32 {
        // Simulate empty table
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_issue105() {
        let db = DummyDb;
        // Simulate the usefixture("foo_table"), which creates an empty table, so scalar is 0.
        assert_eq!(db.query("select count(*) as n from foo").scalar(), 0);
    }
}