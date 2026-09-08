import pytest
from src.ball import Ball

def test_constructor_sets_members():
    b = Ball(15.0, 25.0, 8.0, -2.5, 7.0)
    assert b.x == pytest.approx(15.0)
    assert b.y == pytest.approx(25.0)
    assert b.radius == pytest.approx(8.0)
    assert b.speedX == pytest.approx(-2.5)
    assert b.speedY == pytest.approx(7.0)

def test_update_bounces_off_left_wall():
    b = Ball(2.0, 40.0, 7.0, -8.0, 0.0)
    b.Update(130.0, 120.0)
    assert b.x == pytest.approx(7.0) # at radius
    assert b.speedX == pytest.approx(8.0) # inverted

def test_update_bounces_off_right_wall():
    b = Ball(128.0, 35.0, 7.0, 5.0, 0.0)
    b.Update(135.0, 120.0)
    assert b.x == pytest.approx(128.0) # at screenWidth-radius (135-7)
    assert b.speedX == pytest.approx(-5.0) # inverted

def test_update_bounces_off_top_wall():
    b = Ball(65.0, 3.0, 6.0, 0.0, -6.0)
    b.Update(110.0, 110.0)
    assert b.y == pytest.approx(6.0) # at radius
    assert b.speedY == pytest.approx(6.0) # inverted

def test_update_bounces_off_bottom_wall():
    b = Ball(60.0, 108.0, 6.0, 0.0, 6.0)
    b.Update(110.0, 110.0)
    assert b.y == pytest.approx(104.0) # at screenHeight-radius (110-6)
    assert b.speedY == pytest.approx(-6.0) # inverted

def test_update_no_bounce():
    b = Ball(70.0, 70.0, 7.0, -2.0, 3.0)
    b.Update(140.0, 140.0)
    assert b.x == pytest.approx(68.0)
    assert b.y == pytest.approx(73.0)
    assert b.speedX == pytest.approx(-2.0)
    assert b.speedY == pytest.approx(3.0)

def test_draw_does_not_throw():
    b = Ball(14.0, 19.0, 9.0, 0.0, 0.0)
    b.Draw()