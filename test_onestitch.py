# test_stitches_pytest.py
# Pytest version of the unittest suite.
#
# Assumption: your drawing code is saved as stitches.py in the same folder.
# If not, change `import stitches as m`.

from unittest.mock import patch

import one_stitch as m


class FakePen:
    """Minimal pen so .color() and .pensize() don't crash."""

    def color(self, *_args, **_kwargs):
        pass

    def pensize(self, *_args, **_kwargs):
        pass


class SegmentRecorder:
    """Collects draw_segment(pen, x1, y1, x2, y2) calls."""

    def __init__(self):
        self.segments = []

    def __call__(self, pen, x1, y1, x2, y2):
        self.segments.append((x1, y1, x2, y2))


def test_bit_at_empty_and_zero():
    assert m.bit_at("", 0) == 0
    assert m.bit_at("0", 123) == 0


def test_bit_at_one():
    assert m.bit_at("1", 0) == 1
    assert m.bit_at("1", 999) == 1


def test_bit_at_repeats_pattern():
    pat = "0011"
    got = [m.bit_at(pat, i) for i in range(8)]
    assert got == [0, 0, 1, 1, 0, 0, 1, 1]


def test_pat_for_wraps():
    arr = ["a", "b", "c"]
    assert m.pat_for(arr, 0) == "a"
    assert m.pat_for(arr, 3) == "a"
    assert m.pat_for(arr, 4) == "b"


def test_pat_for_empty():
    assert m.pat_for([], 0) == "0"
    assert m.pat_for(None, 10) == "0"


def test_draw_bg_grid_segment_count():
    rec = SegmentRecorder()
    pen = FakePen()

    cols, rows, cell = 4, 3, 10
    x0, y0 = 0, 0

    with patch.object(m, "draw_segment", new=rec):
        m.draw_bg_grid(pen, x0, y0, cols, rows, cell)

    assert len(rec.segments) == (cols + 1) + (rows + 1)

    # First recorded segment should be a vertical line from y0 to y0+rows*cell
    x1, y1, x2, y2 = rec.segments[0]
    assert y1 == y0
    assert y2 == y0 + rows * cell


def test_draw_horizontal_stitches_expected_positions():
    rec = SegmentRecorder()
    pen = FakePen()

    cols, rows, cell = 4, 1, 10
    x0, y0 = 0, 0

    # row0 all off, row1 uses 0011 -> stitches at col 2 and 3
    with patch.object(m, "H_ROW_PATTERNS", ["0", "0011"]):
        with patch.object(m, "draw_segment", new=rec):
            m.draw_horizontal_stitches(pen, x0, y0, cols, rows, cell)

    assert len(rec.segments) == 2
    assert (20, 10, 30, 10) in rec.segments  # col 2 on row 1
    assert (30, 10, 40, 10) in rec.segments  # col 3 on row 1


def test_draw_vertical_stitches_expected_positions():
    rec = SegmentRecorder()
    pen = FakePen()

    cols, rows, cell = 1, 4, 10
    x0, y0 = 0, 0

    # col0 all off, col1 uses 0011 -> stitches at row 2 and 3
    with patch.object(m, "V_COL_PATTERNS", ["0", "0011"]):
        with patch.object(m, "draw_segment", new=rec):
            m.draw_vertical_stitches(pen, x0, y0, cols, rows, cell)

    assert len(rec.segments) == 2
    assert (10, 20, 10, 30) in rec.segments  # row 2 on col 1
    assert (10, 30, 10, 40) in rec.segments  # row 3 on col 1


def test_draw_ne_diagonals_all_on_draws_cols_times_rows():
    rec = SegmentRecorder()
    pen = FakePen()

    cols, rows, cell = 3, 3, 10
    x0, y0 = 0, 0

    # Force every diagonal step "on"
    with patch.object(m, "NE_DIAG_PATTERNS", ["1"]):
        with patch.object(m, "draw_segment", new=rec):
            m.draw_ne_diagonal_stitches(pen, x0, y0, cols, rows, cell)

    # NE segments exist for every cell (c,r) with c in [0..cols-1], r in [0..rows-1]
    assert len(rec.segments) == cols * rows

    for x1, y1, x2, y2 in rec.segments:
        assert 0 <= x1 <= cols * cell
        assert 0 <= x2 <= cols * cell
        assert 0 <= y1 <= rows * cell
        assert 0 <= y2 <= rows * cell
        assert (x2 - x1) == cell
        assert (y2 - y1) == cell


def test_draw_nw_diagonals_all_on_draws_cols_times_rows():
    rec = SegmentRecorder()
    pen = FakePen()

    cols, rows, cell = 3, 3, 10
    x0, y0 = 0, 0

    # Force every diagonal step "on"
    with patch.object(m, "NW_DIAG_PATTERNS", ["1"]):
        with patch.object(m, "draw_segment", new=rec):
            m.draw_nw_diagonal_stitches(pen, x0, y0, cols, rows, cell)

    # NW segments exist for every cell (c,r) with c in [1..cols], r in [0..rows-1]
    assert len(rec.segments) == cols * rows

    for x1, y1, x2, y2 in rec.segments:
        assert 0 <= x1 <= cols * cell
        assert 0 <= x2 <= cols * cell
        assert 0 <= y1 <= rows * cell
        assert 0 <= y2 <= rows * cell
        assert (x2 - x1) == -cell
        assert (y2 - y1) == cell
