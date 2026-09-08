package com.zaxxer.sansorm;

import org.h2.jdbcx.JdbcDataSource;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.sansorm.TestUtils;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@RunWith(Parameterized.class)
public class SqlClosurePublicTest {
   @Parameterized.Parameters(name = "autocommit={0}, ut={1}")
   public static Collection<Object[]> data() {
      return Arrays.asList(new Object[][] {
         { true, true }, { true, false }, { false, true }, { false, false }
      });
   }

   @Parameterized.Parameter(0)
   public boolean withAutoCommit;

   @Parameterized.Parameter(1)
   public boolean withUserTx;

   @Before
   public void setUp() throws IOException {
      final JdbcDataSource dataSource = TestUtils.makeH2DataSource(/*autoCommit=*/withAutoCommit);
      if (withUserTx) {
         SansOrm.initializeTxSimple(dataSource);
      } else {
         SansOrm.initializeTxNone(dataSource);
      }
      SqlClosureElf.executeUpdate("CREATE TABLE tx_test_pub (pubstring VARCHAR(128))");
   }

   @After
   public void tearDown() {
      SqlClosureElf.executeUpdate("DROP TABLE tx_test_pub");
      SansOrm.deinitialize();
   }

   @Test
   public void shouldSupportNestedCalls_Public() {
      final Set<String> insertedValues = SqlClosure.sqlExecute(c -> {
         SqlClosureElf.executeUpdate(c, "INSERT INTO tx_test_pub VALUES (?)", "A");

         // here goes nested SqlClosure
         SqlClosure.sqlExecute(cNested -> SqlClosureElf.executeUpdate(cNested, "INSERT INTO tx_test_pub VALUES (?)", "B"));

         return getStrings(c);
      });
      assertThat(insertedValues).containsOnly("A", "B");
   }

   @Test
   public void shouldRollbackHighestTx_Public() {
      assertThatThrownBy(() -> SqlClosure.sqlExecute(c -> {
         SqlClosureElf.executeUpdate(c, "INSERT INTO tx_test_pub VALUES (?)", "C");

         // here goes nested SqlClosure
         SqlClosure.sqlExecute(cNested -> {
            SqlClosureElf.executeUpdate(cNested, "INSERT INTO tx_test_pub VALUES (?)", "D");
            throw new RuntimeException("public_boom!");
         });

         return SqlClosureElf.executeUpdate(c, "INSERT INTO tx_test_pub VALUES (?)", "E");
      })).isInstanceOf(RuntimeException.class).hasMessage("public_boom!");

      final Set<String> insertedValues = SqlClosure.sqlExecute(SqlClosurePublicTest::getStrings);
      assertThat(insertedValues).isEmpty();
   }

   @Test
   public void shouldRollbackNestedClosuresWithUserTransaction_Public() {
      assertThatThrownBy(() -> SqlClosure.sqlExecute(c -> {
         SqlClosureElf.executeUpdate(c, "INSERT INTO tx_test_pub VALUES (?)", "F");

         // here goes nested SqlClosure
         SqlClosure.sqlExecute(cNested -> SqlClosureElf.executeUpdate(cNested, "INSERT INTO tx_test_pub VALUES (?)", "G"));

         SqlClosureElf.executeUpdate(c, "INSERT INTO tx_test_pub VALUES (?)", "H");
         throw new Error("public_boom!"); // ie something not or type SQLException or RuntimeException
      })).isInstanceOf(Error.class).hasMessage("public_boom!");

      final Set<String> insertedValues = SqlClosure.sqlExecute(SqlClosurePublicTest::getStrings);
      if (withUserTx) {
         assertThat(insertedValues).containsOnly().as("With UserTransaction nested closures share same tx scope");
      } else {
         assertThat(insertedValues).containsOnly("G").as("Without UserTransaction every closure defines it's own tx scope");
      }
   }

   static Set<String> getStrings(Connection c) throws SQLException {
      ResultSet rs = SqlClosureElf.executeQuery(c, "SELECT pubstring FROM tx_test_pub;");
      Set<String> result = new HashSet<>();
      while (rs.next()) {
         result.add(rs.getString(1));
      }
      return result;
   }
}