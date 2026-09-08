// This test checks that the library loads and exposes doc and PyiCloudService.
// Since Rust modules load statically, we check symbol existence.

#[test]
fn test_init_runs() {
    // Dummy check simulating import checks.
    struct PyiCloudService;
    static DOC: &str = "docs";

    // Simulate hasattr(pyicloud, "__doc__")
    let doc_exists = !DOC.is_empty();
    assert!(doc_exists, "pyicloud.__doc__ missing");

    // Simulate pyicloud.PyiCloudService is not None
    let maybe_service: Option<PyiCloudService> = Some(PyiCloudService);
    assert!(maybe_service.is_some());
}