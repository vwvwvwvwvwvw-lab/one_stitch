import turtle as t

# ----------------------------
# CONFIG
# ----------------------------
COLS = 30
ROWS = 30
CELL = 12

SHOW_BG_GRID = False
NO_ANIMATION = False
BG_GRID_COLOR = "#d0d0d0"
BG_GRID_THICKNESS = 1

STITCH_THICKNESS = 5

# Patterns can be:
# - "" or "0" -> all off
# - "1" -> all on
# - "0011" etc -> repeats forever

H_ROW_PATTERNS = ["0101", "1010"]
V_COL_PATTERNS =  ["0011", "1100"]
NE_DIAG_PATTERNS = []

NW_DIAG_PATTERNS = []

H_COLOR = "#0e2964"
V_COLOR = "#0e2964"
NE_COLOR = "#0e2964"
NW_COLOR = "#0e2964"


def bit_at(pattern: str, idx: int) -> int:
    """Return 0/1 for pattern repeated forever."""
    if not pattern or pattern == "0":
        return 0
    if pattern == "1":
        return 1
    return 1 if pattern[idx % len(pattern)] == "1" else 0


def pat_for(arr, i):
    if not arr:
        return "0"
    return arr[i % len(arr)]


def jump(pen, x, y):
    pen.up()
    pen.goto(x, y)
    pen.down()


def draw_segment(pen, x1, y1, x2, y2):
    jump(pen, x1, y1)
    pen.goto(x2, y2)


def draw_bg_grid(pen, x0, y0, cols, rows, cell):
    pen.color(BG_GRID_COLOR)
    pen.pensize(BG_GRID_THICKNESS)

    # vertical lines
    for col in range(cols + 1):
        x = x0 + col * cell
        draw_segment(pen, x, y0, x, y0 + rows * cell)

    # horizontal lines
    for row in range(rows + 1):
        y = y0 + row * cell
        draw_segment(pen, x0, y, x0 + cols * cell, y)


def draw_horizontal_stitches(pen, x0, y0, cols, rows, cell):
    pen.color(H_COLOR)
    pen.pensize(STITCH_THICKNESS)

    for row in range(rows + 1):
        pattern = pat_for(H_ROW_PATTERNS, row)
        y = y0 + row * cell
        for col in range(cols):
            if bit_at(pattern, col):
                x1 = x0 + col * cell
                x2 = x0 + (col + 1) * cell
                draw_segment(pen, x1, y, x2, y)


def draw_vertical_stitches(pen, x0, y0, cols, rows, cell):
    pen.color(V_COLOR)
    pen.pensize(STITCH_THICKNESS)

    for col in range(cols + 1):
        pattern = pat_for(V_COL_PATTERNS, col)
        x = x0 + col * cell
        for row in range(rows):
            if bit_at(pattern, row):
                y1 = y0 + row * cell
                y2 = y0 + (row + 1) * cell
                draw_segment(pen, x, y1, x, y2)


def draw_ne_diagonal_stitches(pen, x0, y0, cols, rows, cell):
    pen.color(NE_COLOR)
    pen.pensize(STITCH_THICKNESS)

    diag_index = 0

    for start_col in range(-cols, cols + 1):
        pattern = pat_for(NE_DIAG_PATTERNS, diag_index)

        col = start_col
        row = 0
        while col < cols and row < rows:
            if bit_at(pattern, row):
                x1 = x0 + col * cell
                y1 = y0 + row * cell
                x2 = x0 + (col + 1) * cell
                y2 = y0 + (row + 1) * cell
                if row >= 0 and col >= 0:
                    draw_segment(pen, x1, y1, x2, y2)
            col += 1
            row += 1

        diag_index += 1


def draw_nw_diagonal_stitches(pen, x0, y0, cols, rows, cell):
    pen.color(NW_COLOR)
    pen.pensize(STITCH_THICKNESS)

    diag_index = 0

    for start_col in range(2 * cols - 1, -cols, -1):
        pattern = pat_for(NW_DIAG_PATTERNS, diag_index)

        col = start_col
        row = 0
        while col > 0 and row < rows:
            if bit_at(pattern, row):
                x1 = x0 + col * cell
                y1 = y0 + row * cell
                x2 = x0 + (col - 1) * cell
                y2 = y0 + (row + 1) * cell
                if row >= 0 and col <= cols:
                    draw_segment(pen, x1, y1, x2, y2)

            col -= 1
            row += 1

        diag_index += 1


def main():
    screen = t.Screen()
    if NO_ANIMATION:
        screen.tracer(0, 0)
    screen.setup(1100, 800)
    screen.title("")

    pen = t.Turtle(visible=False)
    pen.speed(0)
    pen.hideturtle()
    pen.pencolor("black")

    x0 = -COLS * CELL / 2
    y0 = -ROWS * CELL / 2

    if SHOW_BG_GRID:
        draw_bg_grid(pen, x0, y0, COLS, ROWS, CELL)

    draw_horizontal_stitches(pen, x0, y0, COLS, ROWS, CELL)
    draw_vertical_stitches(pen, x0, y0, COLS, ROWS, CELL)
    draw_nw_diagonal_stitches(pen, x0, y0, COLS, ROWS, CELL)
    draw_ne_diagonal_stitches(pen, x0, y0, COLS, ROWS, CELL)

    screen.update()
    t.done()


if __name__ == "__main__":
    main()
