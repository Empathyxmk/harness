def test_issue105_public(db):
    db.query("CREATE TABLE plants (species varchar(32))")
    db.query("INSERT INTO plants (species) VALUES (:species)", species="Ficus")
    data = db.query("SELECT * FROM plants")
    assert data.first()['species'] == "Ficus"