//! Test Authorization header variants and errors
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/protected")]
async fn protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_default_headers() {
    let app = test::init_service(
        App::new().service(protected)
    ).await;
    // Non-bearer
    let req = test::TestRequest::get()
        .uri("/protected")
        .insert_header((header::AUTHORIZATION, "Basic basiccreds"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let ebody: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(ebody, json!({"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"}));
    // Bearer (success path simulation):
    let req = test::TestRequest::get()
        .uri("/protected")
        .insert_header((header::AUTHORIZATION, "Bearer faketoken"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let body: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(body, json!({"foo": "bar"}));
}