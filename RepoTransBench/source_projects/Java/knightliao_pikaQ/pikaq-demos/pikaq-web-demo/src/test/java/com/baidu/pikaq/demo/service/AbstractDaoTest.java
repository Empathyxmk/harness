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

public class AbstractDaoTest {

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
            return Arrays.asList(new SimpleEntity(1L), new SimpleEntity(2L));
        }
        @Override
        public List<SimpleEntity> find(List<Match> matchList, List<Order> orderList, int offset, int limit) {
            return Arrays.asList(new SimpleEntity(1L), new SimpleEntity(2L));
        }
        @Override
        public int count(List<Match> matchList) { return 42; }
    }

    @Test
    public void testOrderMatchModify() {
        SimpleDao dao = new SimpleDao();
        Order order = dao.order("col", true);
        assertEquals("col", order.getColumn());
        assertTrue(order.isAsc());

        Match match = dao.match("foo", 1);
        assertEquals("foo", match.getColumn());
        assertEquals(1, match.getValue());

        Modify modify = dao.modify("bar", 2);
        assertEquals("bar", modify.getColumn());
        assertEquals(2, modify.getValue());
    }

    @Test
    public void testToList() {
        SimpleDao dao = new SimpleDao();
        List<Object> empty = dao.toList();
        assertEquals(0, empty.size());
        List<Object> vals = dao.toList(1, "abc", 3.4);
        assertEquals(3, vals.size());
        assertEquals("abc", vals.get(1));
    }

    @Test
    public void testPage2() {
        SimpleDao dao = new SimpleDao();
        DaoPage page = new DaoPage();
        page.setPageNo(1);
        page.setPageSize(20);
        DaoPageResult<SimpleEntity> result = dao.page2(Arrays.asList(dao.match("foo", 123)), page);
        assertNotNull(result.getResult());
        assertEquals(42, result.getTotalCount());
    }

    @Test
    public void testLikeBetweenGreaterLessExpressNotIncr() {
        SimpleDao dao = new SimpleDao();
        assertNotNull(dao.like("str"));
        assertNotNull(dao.between(1, 5));
        assertNotNull(dao.greaterThan(9));
        assertNotNull(dao.lessThan(5));
        assertNotNull(dao.express());
        assertNotNull(dao.not("notVal"));
        assertNotNull(dao.incr(3));
    }
}