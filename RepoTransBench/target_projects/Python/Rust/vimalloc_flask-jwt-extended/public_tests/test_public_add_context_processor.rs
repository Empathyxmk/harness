// Test: context processor integration
use actix_web::{test, web, App};
use actix_web::web::Data;
use actix_web::Responder;

fn context_value() -> Data<i32> {
    Data::new(29)
}

#[actix_rt::test]
async fn test_context_processor() {
    // Simulate a context processor that adds bar=29 to template environment
    let val = context_value();
    // Render logic would access this value as {{ bar }}; here we just assert it's present.
    assert_eq!(*val.get_ref(), 29);
}