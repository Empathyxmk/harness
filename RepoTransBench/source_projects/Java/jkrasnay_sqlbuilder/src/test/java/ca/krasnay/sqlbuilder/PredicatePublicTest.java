package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class PredicatePublicTest extends TestCase {

    public void testPredicatePublic() {
        Predicate pred = new Predicate() {
            String sql;
            public void init(AbstractSqlCreator creator) {
                String p = creator.allocateParameter();
                sql = p + " > 10";
            }
            public String toSql() {
                return sql;
            }
        };
        SelectCreator sc = new SelectCreator();
        pred.init(sc);
        assertEquals("param0 > 10", pred.toSql());
    }
}