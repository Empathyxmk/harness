package com.github.joonavali.naturalmouse;

import com.github.joonasvali.naturalmouse.util.FlowUtil;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.function.Function;

public class FlowUtilPublicTest {
  private static final double SMALL_DELTA = 10e-6;

  @Test
  public void testStretchFlow_2to6() {
    double[] flow = {2, 4};
    double[] result = FlowUtil.stretchFlow(flow, 6);
    Assertions.assertArrayEquals(
        new double[]{2.0, 2.4, 2.8, 3.2, 3.6, 4.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 6, result);
  }

  @Test
  public void testStretchFlow_2to11() {
    double[] flow = {2};
    double[] result = FlowUtil.stretchFlow(flow, 11);
    Assertions.assertArrayEquals(
        new double[]{2,2,2,2,2,2,2,2,2,2,2}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 11, result);
  }

  @Test
  public void testStretchFlow_4to8() {
    double[] flow = {1, 3, 5, 7};
    double[] result = FlowUtil.stretchFlow(flow, 8);
    Assertions.assertArrayEquals(
        new double[]{1.0, 1.75, 2.5, 3.25, 4.0, 4.75, 5.5, 7.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 8, result);
  }

  @Test
  public void testStretchFlow_4to8_withModifier() {
    double[] flow = {1, 3, 5, 7};
    Function<Double, Double> modifier = value -> value * 3;
    double[] result = FlowUtil.stretchFlow(flow, 8, modifier);
    Assertions.assertArrayEquals(
        new double[]{3.0, 5.25, 7.5, 9.75, 12.0, 14.25, 16.5, 21.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 3 * 8, result);
  }

  @Test
  public void testStretchFlow_2to7_withModifier() {
    double[] flow = {2, 5};
    Function<Double, Double> modifier = Math::round;
    double[] result = FlowUtil.stretchFlow(flow, 7, modifier);
    Assertions.assertArrayEquals(
        new double[]{2,2,3,3,4,4,5}, result, SMALL_DELTA
    );
  }

  @Test
  public void testStretchFlow_3to7() {
    double[] flow = {1, 4, 7};
    double[] result = FlowUtil.stretchFlow(flow, 7);
    Assertions.assertArrayEquals(
        new double[]{1.0, 1.5, 2.0, 3.0, 4.0, 5.5, 7.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 7, result);
  }

  @Test
  public void testStretchFlow_3to9() {
    double[] flow = {1, 3, 5};
    double[] result = FlowUtil.stretchFlow(flow, 9);
    Assertions.assertArrayEquals(
        new double[]{1.0, 1.25, 1.5, 1.75, 2.0, 2.75, 3.5, 4.25, 5.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 9, result);
  }

  @Test
  public void testStretchFlow_4to12() {
    double[] flow = {1.2, 3.4, 5.6, 7.8};
    double[] result = FlowUtil.stretchFlow(flow, 12);
    Assertions.assertArrayEquals(
        new double[]{
            1.2,1.45,1.7,2.25,
            2.8,3.35,3.9,4.45,
            5.0,5.55,6.1,7.8
        }, result, SMALL_DELTA);

    assertArraySum(average(flow) * 12, result);
  }

  @Test
  public void testReduceFlow_6to2() {
    double[] flow = {3, 1, 5, 9, 2, 12};
    double[] result = FlowUtil.reduceFlow(flow, 2);
    Assertions.assertArrayEquals(
        new double[]{5.0, 7.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 2, result);
  }

  @Test
  public void testReduceFlow_7to2() {
    double[] flow = {10, 8, 6, 4, 2, 12, 14};
    double[] result = FlowUtil.reduceFlow(flow, 2);
    Assertions.assertArrayEquals(
        new double[]{6.0, 11.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 2, result);
  }

  @Test
  public void testReduceFlow_12to3() {
    double[] flow = {12,8,4,12,16,20,24,24,8,8,8,8};
    double[] result = FlowUtil.reduceFlow(flow, 3);
    Assertions.assertArrayEquals(
        new double[]{9.0, 20.0, 8.0}, result, SMALL_DELTA
    );
    assertArraySum(average(flow) * 3, result);
  }

  private void assertArraySum(double expected, double[] actual) {
    Assertions.assertEquals(expected, sum(actual), SMALL_DELTA, "Sum not matching expected");
  }
  private double sum(double[] arr) {
    double s = 0;
    for (double v : arr) s += v;
    return s;
  }
  private double average(double[] arr) {
    return sum(arr) / arr.length;
  }
}