def test_issue69_public(db):
    db.query("CREATE table animals (species text)")
    db.query("SELECT * FROM animals WHERE species = :sp", sp="CanisLupus")