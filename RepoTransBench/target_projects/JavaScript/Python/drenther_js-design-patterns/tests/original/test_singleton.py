def import_singleton():
    from src.Creational.Singleton import Database
    return Database

def test_should_instantiate_only_one_instance():
    Database = import_singleton()
    mongo = Database('mongo')
    mysql = Database('mysql')
    assert mongo.get_data() == 'mongo'
    assert mysql.get_data() == 'mongo'
    assert mongo == mysql