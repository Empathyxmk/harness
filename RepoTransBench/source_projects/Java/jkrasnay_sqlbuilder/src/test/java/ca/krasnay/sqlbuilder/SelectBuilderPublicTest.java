package ca.krasnay.sqlbuilder;

import junit.framework.TestCase;

public class SelectBuilderPublicTest extends TestCase {

    public void testBasicsPublic() {

        //
        // Simple tables with different table names and columns
        //

        SelectBuilder sb = new SelectBuilder("Department");
        assertEquals("select * from Department", sb.toString());

        sb = new SelectBuilder("Department d");
        assertEquals("select * from Department d", sb.toString());

        sb = new SelectBuilder("Department d").column("floor");
        assertEquals("select floor from Department d", sb.toString());

        sb = new SelectBuilder("Department d").column("floor").column("budget");
        assertEquals("select floor, budget from Department d", sb.toString());

        sb = new SelectBuilder("Department d").column("floor as f").column("budget");
        assertEquals("select floor as f, budget from Department d", sb.toString());

        //
        // Where clauses (different values)
        //

        sb = new SelectBuilder("Department d").where("floor > 2");
        assertEquals("select * from Department d where floor > 2", sb.toString());

        sb = new SelectBuilder("Department d").where("budget >= 1000").where("floor < 5");
        assertEquals("select * from Department d where budget >= 1000 and floor < 5", sb.toString());

        //
        // Join clauses (different tables)
        //

        sb = new SelectBuilder("Department d").join("Building b on d.building_id = b.id");
        assertEquals("select * from Department d join Building b on d.building_id = b.id", sb.toString());

        sb = new SelectBuilder("Department d").join("Building b on d.building_id = b.id").where("budget > 500");
        assertEquals("select * from Department d join Building b on d.building_id = b.id where budget > 500", sb.toString());

        //
        // Order by clauses (different column)
        //

        sb = new SelectBuilder("Department d").orderBy("budget desc");
        assertEquals("select * from Department d order by budget desc", sb.toString());

        sb = new SelectBuilder("Department d").orderBy("floor").orderBy("budget");
        assertEquals("select * from Department d order by floor, budget", sb.toString());

        sb = new SelectBuilder("Department").where("budget < 2000").orderBy("floor desc");
        assertEquals("select * from Department where budget < 2000 order by floor desc", sb.toString());

        //
        // For Update (different id)
        //

        sb = new SelectBuilder("Department").where("id = 7").forUpdate();
        assertEquals("select * from Department where id = 7 for update", sb.toString());

    }

    public void testLimitsPublic() {

        SelectBuilder sb = new SelectBuilder()
                .from("public_table")
                .column("x")
                .column("y")
                .limit(5);

        assertEquals("select x, y from public_table limit 5", sb.toString());

        sb = sb.limit(2, 15);

        assertEquals("select x, y from public_table limit 2, 15", sb.toString());
    }

    public void testUnionsPublic() {

        SelectBuilder sb = new SelectBuilder()
        .column("x")
        .column("y")
        .from("Alpha")
        .where("x < 100")
        .orderBy("2");

        sb.union(new SelectBuilder()
        .column("z")
        .column("w")
        .from("Beta"));

        assertEquals("select x, y from Alpha where x < 100 union select z, w from Beta order by 2", sb.toString());

    }
}