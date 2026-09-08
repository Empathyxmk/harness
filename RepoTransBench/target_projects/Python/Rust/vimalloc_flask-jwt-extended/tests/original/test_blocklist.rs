//! Blocklist integration/config/logic tests (partial)
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/protected")]
async fn access_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_non_blocklisted_access_token() {
    let app = test::init_service(App::new().service(access_protected)).await;
    let req = test::TestRequest::get().uri("/protected").to_request();
    let resp = test::call_service(&app, req).await;
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"foo": "bar"}));
    assert_eq!(resp.status(), 200);
}