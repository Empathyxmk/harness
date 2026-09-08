import pytest

import collections

# We simulate the FindFitZoom function
def find_fit_zoom(bg_size, sticker_size, roi_normalized_size):
    # Implements the logic to find scaling factor so that sticker fits ROI in bg
    bg_w, bg_h = bg_size
    st_w, st_h = sticker_size
    norm_w, norm_h = roi_normalized_size
    # Compute size of ROI in bg pixels
    roi_px_w = bg_w * norm_w
    roi_px_h = bg_h * norm_h
    scale_w = roi_px_w / st_w
    scale_h = roi_px_h / st_h
    return min(scale_w, scale_h)

FindFitZoomTestCase = collections.namedtuple(
    "FindFitZoomTestCase",
    ["test_name", "bg_size", "sticker_size", "roi_normalized_size", "expected_fit_zoom"]
)

test_cases = [
    FindFitZoomTestCase("same_size_full_image", (64, 64), (64, 64), (1.0, 1.0), 1.0),
    FindFitZoomTestCase("same_size_half_image", (64, 64), (32, 32), (0.5, 0.5), 1.0),
    FindFitZoomTestCase("square_double_zoom", (64, 64), (32, 32), (1.0, 1.0), 2.0),
    FindFitZoomTestCase("square_half_zoom", (64, 64), (64, 64), (0.5, 0.5), 0.5),
    FindFitZoomTestCase("square_sprite_with_horizontal_rect_roi_requires_scaling_for_horizontal_coverage", (64, 64), (16, 16), (0.5, 0.25), 2.0),
    FindFitZoomTestCase("square_sprite_with_vertical_rect_roi_requires_scaling_for_vertical_coverage", (64, 64), (16, 16), (0.25, 0.5), 2.0),
    FindFitZoomTestCase("square_sprite_with_vertical_rect_roi_and_horizontal_rect_background", (64, 32), (8, 16), (0.125, 0.5), 1.0),
    FindFitZoomTestCase("square_sprite_with_horizontal_rect_roi_and_vertical_rect_background", (32, 64), (16, 8), (0.5, 0.125), 1.0),
]

@pytest.mark.parametrize("test_case", test_cases, ids=[tc.test_name for tc in test_cases])
def test_find_fit_zoom(test_case):
    result = find_fit_zoom(test_case.bg_size, test_case.sticker_size, test_case.roi_normalized_size)
    assert pytest.approx(result, abs=1e-6) == test_case.expected_fit_zoom