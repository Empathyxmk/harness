use actix_web::{test, web, App, HttpResponse, Responder, post, guard};

async fn opt() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({"answer": "options!"}))
}

#[actix_rt::test]
async fn test_options_allowed() {
    let app = test::init_service(
        App::new().route(
            "/endpoint",
            web::route()
                .guard(guard::Options())
                .to(|| HttpResponse::Ok().finish())
        ).route("/endpoint", web::post().to(opt))
    ).await;
    let req = test::TestRequest::options().uri("/endpoint").to_request();
    let resp = test::call_service(&app, req).await;
    // actix-web returns 200 for OPTIONS; allow both 200/204 for Flask parity
    assert!(resp.status() == 200 || resp.status() == 204);
}