using System;
using Xunit;
using System.Collections.Generic;
using System.Linq;

namespace KnightliaoPikaQ.PublicTests
{
    public abstract class BaseObject<T>
    {
        public abstract T GetId();
        public abstract void SetId(T id);
    }

    public class Match
    {
        public string Column { get; set; }
        public object Value { get; set; }
        public Match(string column, object value) { Column = column; Value = value; }
    }

    public class Modify
    {
        public string Column { get; set; }
        public object Value { get; set; }
        public Modify(string column, object value) { Column = column; Value = value; }
    }

    public class Order
    {
        public string Column { get; }
        public bool IsAsc { get; }
        public Order(string column, bool asc) { Column = column; IsAsc = asc; }
    }

    public class DaoPage
    {
        public int PageNo { get; set; }
        public int PageSize { get; set; }
    }

    public class DaoPageResult<T>
    {
        public List<T> Result { get; set; }
        public int TotalCount { get; set; }
        public DaoPageResult(List<T> result, int total) { Result = result; TotalCount = total; }
        public List<T> GetResult() => Result;
        public int GetTotalCount() => TotalCount;
    }

    public abstract class AbstractDao<TKey, TEntity>
    {
        public virtual Order Order(string col, bool asc) => new Order(col, asc);
        public virtual Match Match(string col, object val) => new Match(col, val);
        public virtual Modify Modify(string col, object val) => new Modify(col, val);

        public virtual List<object> ToList(params object[] items)
        {
            return items == null ? new List<object>() : new List<object>(items);
        }

        public abstract TEntity Get(TKey id);
        public abstract List<TEntity> Find(List<Match> matchList, List<Order> orderList);
        public abstract List<TEntity> Find(List<Match> matchList, List<Order> orderList, int offset, int limit);
        public abstract int Count(List<Match> matchList);

        public virtual object Like(object value) => value;
        public virtual object Between(object left, object right) => new[] { left, right };
        public virtual object GreaterThan(object val) => val;
        public virtual object LessThan(object val) => val;
        public virtual object Express() => new object();
        public virtual object Not(object val) => val;
        public virtual object Incr(object val) => val;
        public DaoPageResult<TEntity> Page2(List<Match> matchList, DaoPage page)
        {
            return new DaoPageResult<TEntity>(Find(matchList, new List<Order>()), Count(matchList));
        }
    }

    public class AbstractDaoPublicTest
    {
        class SimpleEntity : BaseObject<long>
        {
            public long id;
            public SimpleEntity(long id) { this.id = id; }
            public override long GetId() => id;
            public override void SetId(long id) { this.id = id; }
        }

        class SimpleDao : AbstractDao<long, SimpleEntity>
        {
            public override SimpleEntity Get(long id) => new SimpleEntity(id);
            public override List<SimpleEntity> Find(List<Match> matchList, List<Order> orderList)
                => new List<SimpleEntity> { new SimpleEntity(3L), new SimpleEntity(4L) };
            public override List<SimpleEntity> Find(List<Match> matchList, List<Order> orderList, int offset, int limit)
                => new List<SimpleEntity> { new SimpleEntity(3L), new SimpleEntity(4L) };
            public override int Count(List<Match> matchList) => 77;
        }

        [Fact]
        public void TestOrderMatchModify()
        {
            var dao = new SimpleDao();
            var order = dao.Order("otherCol", false);
            Assert.Equal("otherCol", order.Column);
            Assert.False(order.IsAsc);

            var match = dao.Match("bar", 5);
            Assert.Equal("bar", match.Column);
            Assert.Equal(5, match.Value);

            var modify = dao.Modify("baz", 8);
            Assert.Equal("baz", modify.Column);
            Assert.Equal(8, modify.Value);
        }

        [Fact]
        public void TestToList()
        {
            var dao = new SimpleDao();
            var empty = dao.ToList();
            Assert.Equal(0, empty.Count);
            var vals = dao.ToList("test", 42, 7.8, false);
            Assert.Equal(4, vals.Count);
            Assert.Equal(42, vals[1]);
            Assert.Equal(false, vals[3]);
        }

        [Fact]
        public void TestPage2()
        {
            var dao = new SimpleDao();
            var page = new DaoPage { PageNo = 2, PageSize = 10 };
            var result = dao.Page2(new List<Match> { dao.Match("bar", 456) }, page);
            Assert.NotNull(result.GetResult());
            Assert.Equal(77, result.GetTotalCount());
        }

        [Fact]
        public void TestLikeBetweenGreaterLessExpressNotIncr()
        {
            var dao = new SimpleDao();
            Assert.NotNull(dao.Like("otherStr"));
            Assert.NotNull(dao.Between(2, 8));
            Assert.NotNull(dao.GreaterThan(15));
            Assert.NotNull(dao.LessThan(1));
            Assert.NotNull(dao.Express());
            Assert.NotNull(dao.Not("anotherVal"));
            Assert.NotNull(dao.Incr(10));
        }
    }
}