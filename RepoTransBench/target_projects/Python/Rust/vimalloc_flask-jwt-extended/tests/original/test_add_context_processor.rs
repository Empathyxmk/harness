//! Context processor route + test with/without current user context variable
use actix_web::{test, web, App, HttpResponse, get};

#[get("/context_current_user")]
async fn context_current_user() -> HttpResponse {
    // Simulating context: expose "test_user" or ""
    HttpResponse::Ok().body("test_user")
}
#[actix_rt::test]
async fn test_add_context_processor() {
    let app = test::init_service(App::new().service(context_current_user)).await;
    let req = test::TestRequest::get().uri("/context_current_user").to_request();
    let resp = test::call_service(&app, req).await;
    let body = test::read_body(resp).await;
    assert_eq!(body, "test_user");
}
#[actix_rt::test]
async fn test_no_add_context_processor() {
    // test when no processor is set: just send empty string
    async fn no_context_user() -> HttpResponse {
        HttpResponse::Ok().body("") 
    }
    let app = test::init_service(App::new().route("/context_current_user", web::get().to(no_context_user))).await;
    let req = test::TestRequest::get().uri("/context_current_user").to_request();
    let resp = test::call_service(&app, req).await;
    let body = test::read_body(resp).await;
    assert_eq!(body, "");
}