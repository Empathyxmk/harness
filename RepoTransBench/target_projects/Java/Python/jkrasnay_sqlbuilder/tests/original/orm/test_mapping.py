import pytest

class RowNotFoundException(Exception):
    pass
class OptimisticLockException(Exception):
    pass

class Employee:
    def __init__(self):
        self.id = 0
        self.version = 0
        self.name = ""

class Mapping:
    def __init__(self, orm_config=None, cls=None, table=None):
        self.cls = cls or Employee
        self.table = table or "Employee"
        self.storage = {}
        self.last_id = 0

    def setIdColumn(self, col):
        self.id_col = col
        return self

    def setVersionColumn(self, version_col):
        self.version_col = version_col
        return self

    def addColumn(self, col):
        return self

    def findById(self, id_):
        if id_ not in self.storage:
            raise RowNotFoundException()
        return self.storage[id_]

    def insert(self, emp):
        if getattr(emp, "id") == 0:
            raise Exception("Primary key unset")
        emp.version = 0
        self.storage[emp.id] = emp

    def update(self, emp):
        if getattr(emp, "version", None) != self.storage[emp.id].version:
            raise OptimisticLockException()
        emp.version += 1
        self.storage[emp.id] = emp

    def deleteById(self, id_):
        if id_ not in self.storage:
            raise RowNotFoundException()
        del self.storage[id_]

def test_all():
    mapping = Mapping(None, Employee, "Employee")
    mapping.setIdColumn("id").setVersionColumn("version").addColumn("name")
    with pytest.raises(RowNotFoundException):
        mapping.findById(42)
    emp = Employee()
    emp.name = "Bobo"
    assert emp.id == 0 and emp.version == 0 and emp.name == "Bobo"

    # Insert failure
    with pytest.raises(Exception):
        mapping.insert(emp)
    emp.id = 1
    mapping.insert(emp)
    assert emp.id == 1 and emp.version == 0
    emp_found = mapping.findById(1)
    assert emp_found.id == 1 and emp_found.name == "Bobo" and emp_found.version == 0

    # Update success
    emp.name = "Bezu"
    mapping.update(emp)
    assert emp.id == 1 and emp.name == "Bezu" and emp.version == 1

    # Update fail (sim optimistic lock)
    emp.name = "Boffo"
    emp.version = 0
    with pytest.raises(OptimisticLockException):
        mapping.update(emp)

    # Delete fail/success
    with pytest.raises(RowNotFoundException):
        mapping.deleteById(2)
    mapping.deleteById(1)
    with pytest.raises(RowNotFoundException):
        mapping.findById(1)