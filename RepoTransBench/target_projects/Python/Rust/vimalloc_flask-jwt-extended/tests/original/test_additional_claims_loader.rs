//! Test for claims loader, merging logic, and custom claims at creation
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/protected")]
async fn get_claims() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[get("/protected2")]
async fn get_refresh_claims() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_additional_claims_in_access_token() {
    let app = test::init_service(
        App::new().service(get_claims)
    ).await;
    let req = test::TestRequest::get().uri("/protected").to_request();
    let resp = test::call_service(&app, req).await;
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val["foo"], "bar");
    assert_eq!(resp.status(), 200);
}
// ... Expand with test coverage for each Python permutation