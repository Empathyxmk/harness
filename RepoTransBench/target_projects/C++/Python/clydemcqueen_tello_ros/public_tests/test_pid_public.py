import pytest
import math

class PID:
    def __init__(self, kp, ki, kd, integral_limit, output_max, output_min):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit = integral_limit
        self.output_max = output_max
        self.output_min = output_min
        self.integral = 0.0
        self.prev_error = None

    def update(self, setpoint, pv, dt):
        error = setpoint - pv

        # Proportional
        p = self.kp * error

        # Integral
        self.integral += error * dt
        if self.integral_limit != 0.0:
            if self.integral > self.integral_limit:
                self.integral = self.integral_limit
            elif self.integral < -self.integral_limit:
                self.integral = -self.integral_limit
        i = self.ki * self.integral

        # Derivative
        if self.prev_error is None or dt == 0.0:
            d = 0.0
        else:
            d = self.kd * (error - self.prev_error) / dt

        self.prev_error = error

        output = p + i + d

        if output > self.output_max:
            output = self.output_max
        elif output < self.output_min:
            output = self.output_min

        return output

def test_output_increased_setpoint():
    pid = PID(1.5, 0.4, 0.2, 0.0, 8.0, -8.0)
    output = pid.update(8.0, 2.0, 0.05)
    assert output > 0.0

def test_integral_windup_different_limits():
    pid = PID(0.15, 0.6, 0.04, 0.5, 0.8, -0.8)
    output = 0.0
    for _ in range(25):
        output = pid.update(12.0, 2.0, 0.15)
    assert output <= 0.8

def test_negative_output_reversed():
    pid = PID(1.3, 0.25, 0.1, 0.0, 6.0, -6.0)
    output = pid.update(1.0, 5.0, 0.1)
    assert output < 0.0