package com.baidu.pikaq.demo.service;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.List;
import java.io.Serializable;
import java.math.BigDecimal;

import com.baidu.ub.common.commons.BaseObject;
import com.baidu.unbiz.common.genericdao.operator.Match;
import com.baidu.unbiz.common.genericdao.operator.Modify;
import com.baidu.unbiz.common.genericdao.operator.Order;
import com.baidu.ub.common.db.DaoPage;
import com.baidu.ub.common.db.DaoPageResult;

public class AbstractDaoPublicTest {

    static class SimpleEntity extends BaseObject<Long> {
        private static final long serialVersionUID = 1L;
        Long id;
        public SimpleEntity(Long id) { this.id = id; }
        @Override public Long getId() { return id; }
        @Override public void setId(Long id) { this.id = id; }
    }

    static class SimpleDao extends AbstractDao<Long, SimpleEntity> {
        @Override
        public SimpleEntity get(Long id) { return new SimpleEntity(id); }
        @Override
        public List<SimpleEntity> find(List<Match> matchList, List<Order> orderList) { 
            return Arrays.asList(new SimpleEntity(3L), new SimpleEntity(4L));
        }
        @Override
        public List<SimpleEntity> find(List<Match> matchList, List<Order> orderList, int offset, int limit) {
            return Arrays.asList(new SimpleEntity(3L), new SimpleEntity(4L));
        }
        @Override
        public int count(List<Match> matchList) { return 77; }
    }

    @Test
    public void testOrderMatchModify() {
        SimpleDao dao = new SimpleDao();
        Order order = dao.order("otherCol", false);
        assertEquals("otherCol", order.getColumn());
        assertFalse(order.isAsc());

        Match match = dao.match("bar", 5);
        assertEquals("bar", match.getColumn());
        assertEquals(5, match.getValue());

        Modify modify = dao.modify("baz", 8);
        assertEquals("baz", modify.getColumn());
        assertEquals(8, modify.getValue());
    }

    @Test
    public void testToList() {
        SimpleDao dao = new SimpleDao();
        List<Object> empty = dao.toList();
        assertEquals(0, empty.size());
        List<Object> vals = dao.toList("test", 42, 7.8, false);
        assertEquals(4, vals.size());
        assertEquals(42, vals.get(1));
        assertEquals(false, vals.get(3));
    }

    @Test
    public void testPage2() {
        SimpleDao dao = new SimpleDao();
        DaoPage page = new DaoPage();
        page.setPageNo(2);
        page.setPageSize(10);
        DaoPageResult<SimpleEntity> result = dao.page2(Arrays.asList(dao.match("bar", 456)), page);
        assertNotNull(result.getResult());
        assertEquals(77, result.getTotalCount());
    }

    @Test
    public void testLikeBetweenGreaterLessExpressNotIncr() {
        SimpleDao dao = new SimpleDao();
        assertNotNull(dao.like("otherStr"));
        assertNotNull(dao.between(2, 8));
        assertNotNull(dao.greaterThan(15));
        assertNotNull(dao.lessThan(1));
        assertNotNull(dao.express());
        assertNotNull(dao.not("anotherVal"));
        assertNotNull(dao.incr(10));
    }
}