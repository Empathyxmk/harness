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

def test_basic_output():
    pid = PID(1.0, 0.5, 0.1, 0.0, 10.0, -10.0)
    output = pid.update(5.0, 3.0, 0.1)
    assert output > 0.0

def test_integral_windup():
    pid = PID(0.1, 0.8, 0.05, 1.0, 1.0, -1.0)
    output = 0.0
    for _ in range(20):
        output = pid.update(10.0, 0.0, 0.2)
    assert output <= 1.0

def test_negative_output():
    pid = PID(1.2, 0.3, 0.2, 0.0, 5.0, -5.0)
    output = pid.update(0.0, 2.0, 0.2)
    assert output < 0.0