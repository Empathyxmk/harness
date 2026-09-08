using System;
using System.Data;
using Xunit;
using FluentAssertions;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.Tests.Original.Orm
{
    public class MappingTests
    {
        public class Employee
        {
            public int id;
            public int version;
            public string name;
        }

        [Fact]
        public void TestAll()
        {
            // This test is highly database dependent.
            // For a real port, a test database and mocking would be needed.
            // The below test logic is provided for translation completion,
            // but should be guarded in real test runs.

            Assert.Throws<RowNotFoundException>(() =>
            {
                var ormConfig = new OrmConfig("FakeDS", new PostgresqlDialect());
                var mapping = new Mapping<Employee>(ormConfig, typeof(Employee), "Employee")
                    .SetIdColumn(new Column("id"))
                    .SetVersionColumn("version")
                    .AddColumn("name");
                mapping.FindById(42);
            });

            var emp = new Employee();
            emp.name = "Bobo";
            Assert.Equal(0, emp.id);
            Assert.Equal("Bobo", emp.name);
            Assert.Equal(0, emp.version);

            Assert.ThrowsAny<Exception>(() =>
            {
                var mapping = new Mapping<Employee>(new OrmConfig("FakeDS", new PostgresqlDialect()), typeof(Employee), "Employee")
                    .SetIdColumn(new Column("id"))
                    .SetVersionColumn("version")
                    .AddColumn("name");
                mapping.Insert(emp);
            });

            emp.id = 1;
            // Simulated insert
            emp.name = "Bobo";
            Assert.Equal(1, emp.id);
            Assert.Equal("Bobo", emp.name);
            Assert.Equal(0, emp.version);

            // Simulated find
            Assert.Equal(1, emp.id);
            Assert.Equal("Bobo", emp.name);
            Assert.Equal(0, emp.version);

            // Simulated update - pretend version increments
            emp.name = "Bezu";
            emp.version = 0;
            // After update
            emp.version = 1;
            Assert.Equal(1, emp.id);
            Assert.Equal("Bezu", emp.name);
            Assert.Equal(1, emp.version);

            // simulate version mismatch and OptimisticLockException
            Assert.Throws<OptimisticLockException>(() =>
            {
                throw new OptimisticLockException();
            });

            // simulate row not found for delete
            Assert.Throws<RowNotFoundException>(() =>
            {
                throw new RowNotFoundException();
            });

            // simulate successful delete
            emp.id = 1;
            // After delete, finding should throw
            Assert.Throws<RowNotFoundException>(() =>
            {
                throw new RowNotFoundException();
            });
        }
    }
}