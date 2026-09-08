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
    NewAccess: Option<String>,
    #[serde(default)]
    NewRefresh: Option<String>,
}

#[post("/protected")]
async fn protected(req: web::Json<JwtReq>) -> actix_web::Result<HttpResponse> {
    if req.access_token.is_none() && req.NewAccess.is_none() {
        return Ok(
            HttpResponse::Unauthorized().json(json!({"msg": "Missing \"NewAccess\" key in json data."}))
        );
    }
    Ok(HttpResponse::Ok().json(json!({"bar": "baz"})))
}
#[post("/refresh")]
async fn refresh(req: web::Json<JwtReq>) -> actix_web::Result<HttpResponse> {
    if req.refresh_token.is_none() && req.NewRefresh.is_none() {
        return Ok(
            HttpResponse::Unauthorized().json(json!({"msg": "Missing \"NewRefresh\" key in json data."}))
        );
    }
    Ok(HttpResponse::Ok().json(json!({"bar": "baz"})))
}
#[actix_rt::test]
async fn test_content_type() {
    let app = test::init_service(App::new().service(protected).service(refresh)).await;
    // Not json encoded
    let req = test::TestRequest::post().uri("/protected")
        .set_payload("access_token=foo").insert_header((CONTENT_TYPE, "application/x-www-form-urlencoded")).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let val: Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"msg": "Missing \"NewAccess\" key in json data."}));
    let req = test::TestRequest::post().uri("/refresh")
        .set_payload("refresh_token=foo").insert_header((CONTENT_TYPE, "application/x-www-form-urlencoded")).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let val: Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"msg": "Missing \"NewRefresh\" key in json data."}));
}

#[actix_rt::test]
async fn test_custom_body_key() {
    let app = test::init_service(App::new().service(protected).service(refresh)).await;

    // Default keys won't work
    let json = json!({"access_token": "foo"});
    let req = test::TestRequest::post().uri("/protected").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"msg": "Missing \"NewAccess\" key in json data."}));

    let json = json!({"refresh_token": "bar"});
    let req = test::TestRequest::post().uri("/refresh").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 401);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"msg": "Missing \"NewRefresh\" key in json data."}));

    // New keys work
    let json = json!({"NewAccess": "foo"});
    let req = test::TestRequest::post().uri("/protected").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"bar": "baz"}));

    let json = json!({"NewRefresh": "bar"});
    let req = test::TestRequest::post().uri("/refresh").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"bar": "baz"}));
}

#[actix_rt::test]
async fn test_defaults() {
    let app = test::init_service(App::new().service(protected).service(refresh)).await;

    let json = json!({"NewAccess": "foo"});
    let req = test::TestRequest::post().uri("/protected").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"bar": "baz"}));

    let json = json!({"NewRefresh": "bar"});
    let req = test::TestRequest::post().uri("/refresh").set_json(&json).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"bar": "baz"}));
}

#[actix_rt::test]
async fn test_custom_content_type() {
    // Variant content-type accepted
    let app = test::init_service(App::new().service(protected).service(refresh)).await;
    let json = json!({"NewAccess": "foo"});
    let req = test::TestRequest::post().uri("/protected").set_json(&json)
        .insert_header(("content-type", "application/json; charset=utf-8")).to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let v: Value = test::read_body_json(resp).await;
    assert_eq!(v, json!({"bar": "baz"}));
}