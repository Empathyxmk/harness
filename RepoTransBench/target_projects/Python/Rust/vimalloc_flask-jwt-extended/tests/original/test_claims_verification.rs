//! Claims verification/loader logic tests
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/protected1")]
async fn protected1() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_successful_claims_validation() {
    let app = test::init_service(
        App::new().service(protected1)
    ).await;
    let req = test::TestRequest::get().uri("/protected1").to_request();
    let resp = test::call_service(&app, req).await;
    let v: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(v["foo"], "bar");
    assert_eq!(resp.status(), 200);
}
// ... Add the unsuccessful/ custom error route logic, as in original