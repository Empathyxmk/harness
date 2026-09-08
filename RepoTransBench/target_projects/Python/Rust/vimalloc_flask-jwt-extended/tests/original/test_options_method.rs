//! OPTIONS requests to endpoints with jwt_required/fresh_jwt_required/refresh_jwt_required
use actix_web::{test, web, App, HttpResponse};
use actix_web::dev::ServiceResponse;

#[actix_rt::test]
async fn test_access_jwt_required_enpoint() {
    async fn jwt_required_endpoint() -> HttpResponse {
        HttpResponse::Ok().body("ok")
    }
    let app = test::init_service(
        App::new().route("/jwt_required", web::route().to(jwt_required_endpoint))
    ).await;
    let req = test::TestRequest::options().uri("/jwt_required").to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
}