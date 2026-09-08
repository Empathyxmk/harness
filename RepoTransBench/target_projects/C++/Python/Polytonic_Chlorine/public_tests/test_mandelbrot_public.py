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

def test_mandelbrot_different_points():
    real = [-1.0, 1.0]
    imag = [0.0, 0.9]
    res = [0, 0]
    solve_mandelbrot(real, imag, 12, res)
    assert res[0] == -1
    assert res[1] > 0 and res[1] < 12

def test_mandelbrot_edge_public():
    real = [1.8, -1.45]
    imag = [-0.1, 0.0]
    res = [0, 0]
    solve_mandelbrot(real, imag, 6, res)
    assert res[0] > 0 and res[0] <= 6
    assert res[1] == -1

def ppm_draw(os, grid):
    iterations = 33
    os.write(f"P6 {len(grid[0])} {len(grid)} 255\n".encode())
    for row in grid:
        for j in row:
            if j == -1:
                r = 25
                g = 0
                b = 100
            else:
                r = int(j * 200 / iterations)
                g = (j * 10) % 256
                b = 100
            os.write(bytes([r, g, b]))

def test_ppm_draw_public():
    grid = [[-1, 2], [7, -1]]
    ss = io.BytesIO()
    ppm_draw(ss, grid)
    s = ss.getvalue()
    assert s.startswith(b"P6")
    assert len(s) > 10