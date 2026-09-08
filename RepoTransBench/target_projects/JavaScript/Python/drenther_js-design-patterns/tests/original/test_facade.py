def import_facade():
    from src.Structural.Facade import ComplaintRegistry, ServiceComplaints, ProductComplaints
    return ComplaintRegistry, ServiceComplaints, ProductComplaints

def test_register_product_complaint():
    ComplaintRegistry, _, _ = import_facade()
    registry = ComplaintRegistry()
    report = registry.register_complaint('John', 'product', 'manufacturing defect')
    assert report == (
        'Complaint No. 1 reported by John regarding manufacturing defect have been filed with the Products Complaint Department. Replacement/Repairment of the product as per terms and conditions will be carried out soon.'
    )

def test_register_service_complaint():
    ComplaintRegistry, _, _ = import_facade()
    registry = ComplaintRegistry()
    report = registry.register_complaint('John', 'service', 'flaky service')
    assert report == (
        'Complaint No. 2 reported by John regarding flaky service have been filed with the Service Complaint Department. The issue will be resolved or the purchase will be refunded as per terms and conditions.'
    )

def test_singleton_behavior():
    ComplaintRegistry, ServiceComplaints, ProductComplaints = import_facade()
    registry = ComplaintRegistry()
    report_service = registry.register_complaint('Martha', 'service', 'availability')
    report_product = registry.register_complaint('Jane', 'product', 'faded color')
    assert report_product == (
        'Complaint No. 4 reported by Jane regarding faded color have been filed with the Products Complaint Department. Replacement/Repairment of the product as per terms and conditions will be carried out soon.'
    )
    assert ProductComplaints().complaints == [
        {'id': 1, 'customer': 'John', 'details': 'manufacturing defect'},
        {'id': 4, 'customer': 'Jane', 'details': 'faded color'},
    ]
    assert report_service == (
        'Complaint No. 3 reported by Martha regarding availability have been filed with the Service Complaint Department. The issue will be resolved or the purchase will be refunded as per terms and conditions.'
    )
    assert ServiceComplaints().complaints == [
        {'id': 2, 'customer': 'John', 'details': 'flaky service'},
        {'id': 3, 'customer': 'Martha', 'details': 'availability'},
    ]