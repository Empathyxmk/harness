import pytest
import io

def solve_mandelbrot(real, imag, iterations, result):
    for i in range(len(real)):
        x = real[i]
        y = imag[i]
        n = 0
        while (x * x + y * y <= 4.0) and n < iterations:
            xtemp = x * x - y * y + real[i]
            y = 2 * x * y + imag[i]
            x = xtemp
            n += 1
        result[i] = -1 if x * x + y * y <= 4.0 else n

def test_mandelbrot_basic():
    real = [0.0, 0.5]
    imag = [0.0, 0.5]
    res = [0, 0]
    solve_mandelbrot(real, imag, 10, res)
    assert res[0] == -1
    assert res[1] > 0

def test_mandelbrot_edge():
    real = [2.0, -2.0]
    imag = [0.0, 0.0]
    res = [0, 0]
    solve_mandelbrot(real, imag, 5, res)
    # 2+0i is outside, escapes fast
    assert res[0] == 1 or res[0] == 2
    # -2+0i should not escape, likely -1 for low iter
    assert res[1] == -1

def ppm_draw(os, grid):
    iterations = 50
    os.write(f"P6 {len(grid[0])} {len(grid)} 255\n".encode())
    for row in grid:
        for j in row:
            if j == -1:
                r = 0
                g = 0
                b = 0
            else:
                r = int(j * 255 / iterations)
                g = r
                b = 255
            os.write(bytes([r, g, b]))

def test_ppm_draw_basic():
    grid = [[-1, 5], [8, -1]]
    ss = io.BytesIO()
    ppm_draw(ss, grid)
    s = ss.getvalue()
    assert s.startswith(b"P6")
    assert len(s) > 10