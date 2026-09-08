/// Test: User lookup callback and current user context handling
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::{json, Value};
use serde::{Deserialize, Serialize};

#[get("/get_user1")]
async fn get_user1() -> HttpResponse {
    // Simulate error if no user_lookup_loader is set
    HttpResponse::Ok().json(json!({"error": "@jwt.user_lookup_loader must be implemented"}))
}

#[get("/get_user2")]
async fn get_user2() -> HttpResponse {
    // Simulate error if no user_lookup_loader is set
    HttpResponse::Ok().json(json!({"error": "@jwt.user_lookup_loader must be implemented"}))
}

#[actix_rt::test]
async fn test_no_user_lookup_loader_specified() {
    let app = test::init_service(
        App::new()
            .service(get_user1)
            .service(get_user2)
    ).await;

    let req = test::TestRequest::get().uri("/get_user1").to_request();
    let resp = test::call_service(&app, req).await;
    let v: Value = test::read_body_json(resp).await;
    assert!(v["error"].as_str().unwrap().contains("@jwt.user_lookup_loader"));

    let req = test::TestRequest::get().uri("/get_user2").to_request();
    let resp = test::call_service(&app, req).await;
    let v: Value = test::read_body_json(resp).await;
    assert!(v["error"].as_str().unwrap().contains("@jwt.user_lookup_loader"));
}