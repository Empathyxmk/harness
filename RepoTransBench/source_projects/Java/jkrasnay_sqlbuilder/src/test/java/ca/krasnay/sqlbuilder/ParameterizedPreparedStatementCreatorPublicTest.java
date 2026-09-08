package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class ParameterizedPreparedStatementCreatorPublicTest extends TestCase {

    public void testNamedParametersToSqlPublic() {
        ParameterizedPreparedStatementCreator creator =
            new ParameterizedPreparedStatementCreator("select * from item where id=:id and price=:price");
        creator.setParameter("id", 111);
        creator.setParameter("price", 15.50);

        assertEquals("select * from item where id=? and price=?", creator.toString());
    }
}