package com.github.joonavali.naturalmouse;

import com.github.joonasvali.naturalmouse.support.Flow;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.util.Arrays;

public class FlowPublicTest {

  private static final double SMALL_DELTA = 10e-6;

  @Test
  public void constantCharacteristicsGetNormalizedTo150() {
    double[] characteristics = new double[50];
    Arrays.fill(characteristics, 300d);
    Flow flow = new Flow(characteristics);

    double[] result = flow.getFlowCharacteristics();
    double sum = 0;
    for (int i = 0; i < result.length; i++) {
      Assertions.assertEquals(100, result[i], SMALL_DELTA);
      sum += result[i];
    }

    Assertions.assertEquals(100 * characteristics.length, sum, SMALL_DELTA);
  }

  @Test
  public void constantCharacteristicsGetNormalizedTo100withVeryLargeArray() {
    double[] characteristics = new double[2000];
    Arrays.fill(characteristics, 999d);
    Flow flow = new Flow(characteristics);

    double[] result = flow.getFlowCharacteristics();
    double sum = 0;
    for (int i = 0; i < result.length; i++) {
      Assertions.assertEquals(100, result[i], SMALL_DELTA);
      sum += result[i];
    }

    Assertions.assertEquals(100 * characteristics.length, sum, SMALL_DELTA);
  }

  @Test
  public void constantCharacteristicsGetNormalizedTo100fromMidValues() {
    double[] characteristics = new double[10];
    Arrays.fill(characteristics, 31);
    Flow flow = new Flow(characteristics);

    double[] result = flow.getFlowCharacteristics();
    double sum = 0;
    for (int i = 0; i < result.length; i++) {
      Assertions.assertEquals(100, result[i], SMALL_DELTA);
      sum += result[i];
    }

    Assertions.assertEquals(100 * characteristics.length, sum, SMALL_DELTA);
  }

  @Test
  public void characteristicsGetNormalizedToAverage100_Public() {
    double[] characteristics = {10, 20, 40};

    Flow flow = new Flow(characteristics);

    double[] result = flow.getFlowCharacteristics();
    double sum = 0;
    for (int i = 0; i < result.length; i++) {
      sum += result[i];
    }
    Assertions.assertEquals(50.0, result[0], SMALL_DELTA);
    Assertions.assertEquals(100.0, result[1], SMALL_DELTA);
    Assertions.assertEquals(200.0, result[2], SMALL_DELTA);

    Assertions.assertEquals(100 * characteristics.length, sum, SMALL_DELTA);
  }

  @Test
  public void stepsAddUpToDistance_accelerating_public() {
    double[] characteristics = {2, 3, 5, 7};
    Flow flow = new Flow(characteristics);
    double step1 = flow.getStepSize(80, 4, 0);
    double step2 = flow.getStepSize(80, 4, 0.25);
    double step3 = flow.getStepSize(80, 4, 0.5);
    double step4 = flow.getStepSize(80, 4, 0.75);
    double sum = step1 + step2 + step3 + step4;
    Assertions.assertEquals(80d, sum, SMALL_DELTA);
  }

  @Test
  public void stepsAddUpToDistance_decelerating_public() {
    double[] characteristics = {7, 5, 3, 2};
    Flow flow = new Flow(characteristics);
    double step1 = flow.getStepSize(80, 4, 0);
    double step2 = flow.getStepSize(80, 4, 0.25);
    double step3 = flow.getStepSize(80, 4, 0.5);
    double step4 = flow.getStepSize(80, 4, 0.75);
    double sum = step1 + step2 + step3 + step4;
    Assertions.assertEquals(80d, sum, SMALL_DELTA);
  }

  @Test
  public void stepsAddUpToDistance_characteristics_not_dividable_by_steps_pub1() {
    double[] characteristics = {2, 2, 4, 4, 6, 6, 8};
    Flow flow = new Flow(characteristics);
    double step1 = flow.getStepSize(84, 3, 0);
    double step2 = flow.getStepSize(84, 3, 1d/3);
    double step3 = flow.getStepSize(84, 3, 2d/3);
    double sum = step1 + step2 + step3;
    Assertions.assertEquals(84d, sum, SMALL_DELTA);
  }

  @Test
  public void stepsAddUpToDistance_characteristics_not_dividable_by_steps_pub2() {
    double[] characteristics = {2,4,6,8,10,12,14,16,18};
    Flow flow = new Flow(characteristics);
    double step1 = flow.getStepSize(180, 6, 0);
    double step2 = flow.getStepSize(180, 6, 1d/6);
    double step3 = flow.getStepSize(180, 6, 2d/6);
    double step4 = flow.getStepSize(180, 6, 3d/6);
    double step5 = flow.getStepSize(180, 6, 4d/6);
    double step6 = flow.getStepSize(180, 6, 5d/6);
    double sum = step1 + step2 + step3 + step4 + step5 + step6;
    Assertions.assertEquals(180d, sum, SMALL_DELTA);
  }

  @Test
  public void stepsAddUpToDistance_characteristics_not_dividable_by_steps_pub3() {
    double[] characteristics = {2,2,4,4,6,6,8,8};
    Flow flow = new Flow(characteristics);
    double step1 = flow.getStepSize(160, 4, 0);
    double step2 = flow.getStepSize(160, 4, 0.25);
    double step3 = flow.getStepSize(160, 4, 0.5);
    double step4 = flow.getStepSize(160, 4, 0.75);
    double sum = step1 + step2 + step3 + step4;
    Assertions.assertEquals(160d, sum, SMALL_DELTA);
  }
}