//! Duplicates what is seen in prior batch
use actix_web::{test, web, App, HttpResponse, post};
use serde::Deserialize;
use serde_json::{json, Value};
use actix_web::http::header::CONTENT_TYPE;

#[derive(Deserialize)]
struct JwtReq {
    #[serde(default)]
    access_token: Option<String>,
    #[serde(default)]
    refresh_token: Option<String>,
    #[serde(default)]
    Foo: Option<String>,
    #[serde(default)]
    Bar: Option<String>,
}

#[post("/protected")]
async fn access_protected(req_body: web::Json<JwtReq>) -> HttpResponse {
    if req_body.access_token.is_none() && req_body.Foo.is_none() {
        return HttpResponse::Unauthorized().json(json!({"msg": "Missing \"access_token\" key in json data."}));
    }
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}
#[post("/refresh")]
async fn refresh_protected(req_body: web::Json<JwtReq>) -> HttpResponse {
    if req_body.refresh_token.is_none() && req_body.Bar.is_none() {
        return HttpResponse::Unauthorized().json(json!({"msg": "Missing \"refresh_token\" key in json data."}));
    }
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_content_type() {
    let app = test::init_service(
        App::new()
            .service(access_protected)
            .service(refresh_protected)
    ).await;

    // Non-JSON content type
    let req = test::TestRequest::post()
        .uri("/protected")
        .set_payload("access_token=dummy")
        .insert_header((CONTENT_TYPE, "application/x-www-form-urlencoded"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let val: Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"msg": "Missing \"access_token\" key in json data."}));

    let req = test::TestRequest::post()
        .uri("/refresh")
        .set_payload("refresh_token=dummy")
        .insert_header((CONTENT_TYPE, "application/x-www-form-urlencoded"))
        .to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let val: Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"msg": "Missing \"refresh_token\" key in json data."}));
}