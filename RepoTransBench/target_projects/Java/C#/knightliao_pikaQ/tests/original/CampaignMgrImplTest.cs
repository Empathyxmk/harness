using Xunit;
using Moq;
using System;
using System.Collections.Generic;
using System.Numerics;

namespace KnightliaoPikaQ.Tests.Original
{
    // Stub and minimal domain classes/interfaces for test
    public class Campaign
    {
        public BigDecimal Price { get; set; }
        public string Name { get; set; }
    }
    public class BigDecimal
    {
        public decimal Value { get; }
        public BigDecimal(decimal v) { Value = v; }
        public static BigDecimal ValueOf(long l) => new BigDecimal(l);
        public static readonly BigDecimal ONE = new BigDecimal(1);
        public static readonly BigDecimal TEN = new BigDecimal(10);
        public static readonly BigDecimal ZERO = new BigDecimal(0);
        public override bool Equals(object obj) => obj is BigDecimal d && Value == d.Value;
        public override int GetHashCode() => Value.GetHashCode();
        public override string ToString() => $"{Value}";
    }
    public static class MessageConstants
    {
        public const string DEFAULT_EXCHANGE = "defaultExchange";
        public const string DEFAULT_ROUTE_KEY = "defaultRouteKey";
        public const string ROUTE_KEY_CONSUMER_ERROR = "routeKeyConsumerError";
        public const string ROUTE_KEY2 = "routeKey2";
    }
    public interface IPikaQGateway
    {
        void Send(string exchange, string routeKey, object msg = null);
        void SendSimple(string exchange, string routeKey, object msg = null);
    }
    public interface IRabbitQGateway
    {
        void Send(string exchange, string routeKey, object msg = null);
        void SendSimple(string exchange, string routeKey, object msg = null);
    }
    public interface ICampaignDao
    {
        Campaign GetByName(string name);
        List<Campaign> FindAll();
        Campaign Create(string name, BigDecimal val);
        Campaign Get(long id);
        void UpdatePriceById(long id, BigDecimal price);
    }
    public class CampaignMgrImpl
    {
        public IPikaQGateway pikaQGateway;
        public IRabbitQGateway rabbitQGateway;
        public ICampaignDao campaignDao;

        public Campaign GetByName(string name) => campaignDao.GetByName(name);
        public List<Campaign> FindAll() => campaignDao.FindAll();
        public Campaign Create(string name, BigDecimal v)
        {
            var c = campaignDao.Create(name, v);
            pikaQGateway.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.DEFAULT_ROUTE_KEY, null);
            return c;
        }
        public Campaign CreateWithConsumerErrorPikaQStrong(string name, BigDecimal v)
        {
            campaignDao.Create(name, v);
            pikaQGateway.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null);
            throw new Exception("something wrong with pikaQ strong");
        }
        public Campaign CreateWithConsumerErrorPikaQNormal(string name, BigDecimal v)
        {
            campaignDao.Create(name, v);
            pikaQGateway.SendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null);
            throw new Exception("something wrong with pikaQ normal");
        }
        public Campaign CreateWithConsumerError(string name, BigDecimal v)
        {
            campaignDao.Create(name, v);
            rabbitQGateway.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null);
            throw new Exception("something wrong with rabbitQ");
        }
        public void Update(long id, BigDecimal price)
        {
            var c = campaignDao.Get(id);
            if (c == null) { return; }
            campaignDao.UpdatePriceById(id, price);
            c.Price = price;
            pikaQGateway.SendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY2, null);
        }
    }

    public class CampaignMgrImplTest
    {
        private CampaignMgrImpl mgr;
        private Mock<IPikaQGateway> pikaQGateway;
        private Mock<IRabbitQGateway> rabbitQGateway;
        private Mock<ICampaignDao> campaignDao;

        public CampaignMgrImplTest()
        {
            pikaQGateway = new Mock<IPikaQGateway>();
            rabbitQGateway = new Mock<IRabbitQGateway>();
            campaignDao = new Mock<ICampaignDao>();
            mgr = new CampaignMgrImpl
            {
                pikaQGateway = pikaQGateway.Object,
                rabbitQGateway = rabbitQGateway.Object,
                campaignDao = campaignDao.Object
            };
        }

        [Fact]
        public void TestGetByName()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.GetByName("x")).Returns(c);
            Assert.Same(c, mgr.GetByName("x"));
            campaignDao.Verify(d => d.GetByName("x"), Times.Once());
        }

        [Fact]
        public void TestFindAll()
        {
            var cs = new List<Campaign> { new Campaign(), new Campaign() };
            campaignDao.Setup(d => d.FindAll()).Returns(cs);
            Assert.Same(cs, mgr.FindAll());
            campaignDao.Verify(d => d.FindAll(), Times.Once());
        }

        [Fact]
        public void TestCreate()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.Create(It.IsAny<string>(), It.IsAny<BigDecimal>())).Returns(c);

            var result = mgr.Create("foo", BigDecimal.ValueOf(19));
            Assert.Same(c, result);

            campaignDao.Verify(d => d.Create("foo", BigDecimal.ValueOf(19)), Times.Once());
            pikaQGateway.Verify(q => q.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.DEFAULT_ROUTE_KEY, null), Times.Once());
        }

        [Fact]
        public void TestCreateWithConsumerErrorPikaQStrong()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.Create(It.IsAny<string>(), It.IsAny<BigDecimal>())).Returns(c);

            var ex = Assert.Throws<Exception>(() =>
                mgr.CreateWithConsumerErrorPikaQStrong("foo", BigDecimal.TEN)
            );
            Assert.Contains("something wrong", ex.Message);

            pikaQGateway.Verify(q => q.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null), Times.Once());
        }

        [Fact]
        public void TestCreateWithConsumerErrorPikaQNormal()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.Create(It.IsAny<string>(), It.IsAny<BigDecimal>())).Returns(c);

            var ex = Assert.Throws<Exception>(() =>
                mgr.CreateWithConsumerErrorPikaQNormal("f", BigDecimal.ONE)
            );
            Assert.Contains("something wrong", ex.Message);

            pikaQGateway.Verify(q => q.SendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null), Times.Once());
        }

        [Fact]
        public void TestCreateWithConsumerError()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.Create(It.IsAny<string>(), It.IsAny<BigDecimal>())).Returns(c);

            var ex = Assert.Throws<Exception>(() =>
                mgr.CreateWithConsumerError("abc", BigDecimal.ZERO)
            );
            Assert.Contains("something wrong", ex.Message);

            rabbitQGateway.Verify(q => q.Send(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY_CONSUMER_ERROR, null), Times.Once());
        }

        [Fact]
        public void TestUpdate_Found()
        {
            var c = new Campaign();
            campaignDao.Setup(d => d.Get(It.IsAny<long>())).Returns(c);

            mgr.Update(22L, BigDecimal.ValueOf(33));
            campaignDao.Verify(d => d.UpdatePriceById(22L, BigDecimal.ValueOf(33)), Times.Once());
            Assert.Equal(BigDecimal.ValueOf(33), c.Price);
            pikaQGateway.Verify(q => q.SendSimple(MessageConstants.DEFAULT_EXCHANGE, MessageConstants.ROUTE_KEY2, null), Times.Once());
        }

        [Fact]
        public void TestUpdate_NotFound()
        {
            campaignDao.Setup(d => d.Get(It.IsAny<long>())).Returns((Campaign)null);

            mgr.Update(33L, BigDecimal.ValueOf(12));
            campaignDao.Verify(d => d.Get(33L), Times.Once());
            campaignDao.Verify(d => d.UpdatePriceById(It.IsAny<long>(), It.IsAny<BigDecimal>()), Times.Never());
            pikaQGateway.Verify(q => q.SendSimple(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<object>()), Times.Never());
        }
    }
}