//! JWTs in query string handling/coverage
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/protected")]
async fn access_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_default_query_paramater() {
    let app = test::init_service(App::new().service(access_protected)).await;
    let req = test::TestRequest::get().uri("/protected?jwt=token").to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"foo": "bar"}));
}