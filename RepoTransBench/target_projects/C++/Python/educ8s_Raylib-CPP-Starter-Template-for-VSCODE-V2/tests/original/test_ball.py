import pytest
from src.ball import Ball

def test_constructor_sets_members():
    b = Ball(10.0, 20.0, 5.0, 3.0, -4.0)
    assert b.x == pytest.approx(10.0)
    assert b.y == pytest.approx(20.0)
    assert b.radius == pytest.approx(5.0)
    assert b.speedX == pytest.approx(3.0)
    assert b.speedY == pytest.approx(-4.0)

def test_update_bounces_off_left_wall():
    b = Ball(1.0, 20.0, 5.0, -3.0, 0.0)
    b.Update(100.0, 100.0)
    assert b.x == pytest.approx(5.0) # at radius
    assert b.speedX == pytest.approx(3.0) # inverted

def test_update_bounces_off_right_wall():
    b = Ball(99.0, 20.0, 5.0, 3.0, 0.0)
    b.Update(100.0, 100.0)
    assert b.x == pytest.approx(95.0) # at screenWidth-radius
    assert b.speedX == pytest.approx(-3.0) # inverted

def test_update_bounces_off_top_wall():
    b = Ball(50.0, 1.0, 5.0, 0.0, -2.0)
    b.Update(100.0, 100.0)
    assert b.y == pytest.approx(5.0) # at radius
    assert b.speedY == pytest.approx(2.0) # inverted

def test_update_bounces_off_bottom_wall():
    b = Ball(50.0, 99.0, 5.0, 0.0, 2.0)
    b.Update(100.0, 100.0)
    assert b.y == pytest.approx(95.0) # at screenHeight-radius
    assert b.speedY == pytest.approx(-2.0) # inverted

def test_update_no_bounce():
    b = Ball(50.0, 50.0, 5.0, 1.0, 1.0)
    b.Update(100.0, 100.0)
    assert b.x == pytest.approx(51.0)
    assert b.y == pytest.approx(51.0)
    assert b.speedX == pytest.approx(1.0)
    assert b.speedY == pytest.approx(1.0)

def test_draw_does_not_throw():
    b = Ball(10.0, 10.0, 5.0, 0.0, 0.0)
    # Should not raise anything
    b.Draw()