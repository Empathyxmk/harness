package guru.springframework.spring5webapp;

import org.junit.Test;

public class Spring5webappApplicationMainMethodPublicTest {

    @Test
    public void mainMethodRunsWithoutExceptionWithArgs() {
        Spring5webappApplication.main(new String[]{"publicTestArg"});
    }
}