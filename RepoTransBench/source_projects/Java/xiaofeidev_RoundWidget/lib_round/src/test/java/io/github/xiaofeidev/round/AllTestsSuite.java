package io.github.xiaofeidev.round;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import io.github.xiaofeidev.round.round.RoundStatusImplTest;
import io.github.xiaofeidev.round.round.RoundStatusTest;
import io.github.xiaofeidev.round.round.RoundStatusImplBuilderTest;
import io.github.xiaofeidev.round.utils.SizeUtilsTest;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        RoundStatusImplTest.class,
        RoundStatusTest.class,
        RoundStatusImplBuilderTest.class,
        SizeUtilsTest.class,
        RoundFrameLayoutTest.class,
        RoundImageViewTest.class,
})
public class AllTestsSuite {
}