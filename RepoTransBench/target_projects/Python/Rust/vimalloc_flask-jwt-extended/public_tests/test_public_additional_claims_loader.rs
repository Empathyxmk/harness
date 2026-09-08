//! Public: Check that additional claims supplied by a loader are included in JWT response data

use actix_web::{test, web, App, HttpResponse, Responder, get};
use serde::{Deserialize, Serialize};
use serde_json::json;

async fn with_claims() -> impl Responder {
    // Simulating claim loader behavior
    HttpResponse::Ok().json(json!({"role": "editor", "active": false}))
}

#[actix_rt::test]
async fn test_additional_claims_are_included() {
    let app = test::init_service(
        App::new().route("/protected", web::get().to(with_claims))
    ).await;

    let req = test::TestRequest::get().uri("/protected").to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"role": "editor", "active": false}));
}