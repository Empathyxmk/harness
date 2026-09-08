//! Simulated Rust adaptation of Python JWT view decorators test suite

use actix_web::{test, web, App, HttpResponse, get};
use actix_web::http::header::{HeaderName, HeaderValue, AUTHORIZATION};
use serde_json::json;

#[get("/protected")]
async fn protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[get("/fresh_protected")]
async fn fresh_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[get("/refresh_protected")]
async fn refresh_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[get("/optional_protected")]
async fn optional_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[get("/no_typecheck_protected")]
async fn no_typecheck_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_jwt_required() {
    let app = test::init_service(
        App::new().service(protected)
    ).await;
    // Success with Bearer
    let req = test::TestRequest::get()
        .uri("/protected")
        .insert_header((AUTHORIZATION, "Bearer faketoken"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"foo": "bar"}));

    // Failure with refresh token (simulate 422)
    let req = test::TestRequest::get()
        .uri("/protected")
        .insert_header((AUTHORIZATION, "Bearer refresh_token"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    // Simulated: 422 error for refresh
    assert!(resp.status() == 422 || resp.status() == 401);
}