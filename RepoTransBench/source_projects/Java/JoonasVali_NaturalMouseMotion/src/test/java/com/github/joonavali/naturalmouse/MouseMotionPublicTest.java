package com.github.joonavali.naturalmouse;

import com.github.joonasvali.naturalmouse.support.DefaultOvershootManager;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.awt.*;
import java.util.ArrayList;

/**
 * Public version of MouseMotionTest with different input/output data but same logic.
 */
public class MouseMotionPublicTest extends MouseMotionTestBase {

  @Test
  public void linearMotionNoOvershoots_public() throws InterruptedException {
    assertMousePosition(10, 10);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(0);
    factory.move(30, 80);
    assertMousePosition(30, 80);

    ArrayList<Point> points = mouse.getMouseMovements();
    Assertions.assertTrue(points.size() > 5, "Path too short; should be more movement points.");
    Point lastPoint = new Point(10, 10);
    for (Point p : points) {
      // check the motion is along a linear diagonal (x - 10) * 7 == (y - 10) * 2, with integer steps
      Assertions.assertEquals( (p.x - 10) * 7, (p.y - 10) * 2, "Not on expected line: " + p );
      Assertions.assertTrue(p.x >= lastPoint.x, "p.x  = " + p.x + " lastPoint.x = " + lastPoint.x);
      Assertions.assertTrue(p.y >= lastPoint.y, "p.y  = " + p.y + " lastPoint.y = " + lastPoint.y);
      lastPoint = p;
    }
  }

  @Test
  public void cantMoveOutOfScreenToNegative_noOverShoots_public() throws InterruptedException {
    assertMousePosition(2, 2);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(0);
    factory.move(-150, -250);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getX() >= 0 && p.getY() >= 0, "Moved out of screen negatives");
    }
    assertMousePosition(0, 0);
  }

  @Test
  public void cantMoveUpToScreenWidth_noOvershoots_public() throws InterruptedException {
    Assertions.assertNotEquals(SCREEN_WIDTH, SCREEN_HEIGHT);
    assertMousePosition(0, 0);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(0);
    // Go to max X and some safe Y within range
    factory.move(SCREEN_WIDTH + 120, SCREEN_HEIGHT / 2);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getX() < SCREEN_WIDTH, "Crossed width limit");
    }
    assertMousePosition(SCREEN_WIDTH - 1, SCREEN_HEIGHT / 2);
  }

  @Test
  public void cantMoveUpToScreenWidth_withOvershoots_public() throws InterruptedException {
    Assertions.assertNotEquals(SCREEN_WIDTH, SCREEN_HEIGHT);

    assertMousePosition(2, 2);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(14);
    factory.move(SCREEN_WIDTH - 2, SCREEN_HEIGHT / 4);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getX() < SCREEN_WIDTH);
    }
    assertMousePosition(SCREEN_WIDTH - 2, SCREEN_HEIGHT / 4);
  }

  @Test
  public void cantMoveUpToScreenHeight_noOvershoots_public() throws InterruptedException {
    Assertions.assertNotEquals(SCREEN_WIDTH, SCREEN_HEIGHT);

    assertMousePosition(3, 3);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(0);
    factory.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT + 73);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getY() < SCREEN_HEIGHT);
    }
    assertMousePosition(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 1);
  }

  @Test
  public void cantMoveUpToScreenHeight_withOvershoots_public() throws InterruptedException {
    Assertions.assertNotEquals(SCREEN_WIDTH, SCREEN_HEIGHT);

    assertMousePosition(7, 7);
    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(13);
    factory.move(SCREEN_WIDTH / 3, SCREEN_HEIGHT - 2);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getY() < SCREEN_HEIGHT);
    }
    assertMousePosition(SCREEN_WIDTH / 3, SCREEN_HEIGHT - 2);
  }

  @Test
  public void cantMoveOutOfScreenToNegative_withOverShoots_public() throws InterruptedException {
    mouse.mouseMove(70, 15);
    assertMousePosition(70, 15);

    ((DefaultOvershootManager)factory.getOvershootManager()).setOvershoots(17);
    factory.move(0, 0);

    ArrayList<Point> points = mouse.getMouseMovements();
    for (Point p : points) {
      Assertions.assertTrue(p.getX() >= 0 && p.getY() >= 0);
    }
    assertMousePosition(0, 0);
  }
}