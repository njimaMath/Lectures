#!/usr/bin/env python3
from html import escape
from math import cos, exp, floor, pi, sin, sqrt
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
W = 760
H = 420
M = 58


def sx(x, xlim):
    return M + (x - xlim[0]) * (W - 2 * M) / (xlim[1] - xlim[0])


def sy(y, ylim):
    return H - M - (y - ylim[0]) * (H - 2 * M) / (ylim[1] - ylim[0])


def pts(points, xlim, ylim):
    return " ".join(f"{sx(x, xlim):.1f},{sy(y, ylim):.1f}" for x, y in points)


def line(x1, y1, x2, y2, xlim, ylim, color="#222", width=2.0, dash=None, arrow=False):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if arrow:
        extra += ' marker-end="url(#arrow)"'
    return (
        f'<line x1="{sx(x1, xlim):.1f}" y1="{sy(y1, ylim):.1f}" '
        f'x2="{sx(x2, xlim):.1f}" y2="{sy(y2, ylim):.1f}" '
        f'stroke="{color}" stroke-width="{width}" fill="none"{extra}/>'
    )


def poly(points, xlim, ylim, color="#1d5f99", width=2.4, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts(points, xlim, ylim)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def text(x, y, value, xlim, ylim, color="#333", size=18, anchor="middle"):
    return f'<text x="{sx(x, xlim):.1f}" y="{sy(y, ylim):.1f}" fill="{color}" font-size="{size}" text-anchor="{anchor}">{escape(value)}</text>'


def circle(cx, cy, r, xlim, ylim, color="#1d5f99", width=2.4, fill="none"):
    rx = r * (W - 2 * M) / (xlim[1] - xlim[0])
    ry = r * (H - 2 * M) / (ylim[1] - ylim[0])
    return f'<ellipse cx="{sx(cx, xlim):.1f}" cy="{sy(cy, ylim):.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'


def ellipse(cx, cy, rx_value, ry_value, xlim, ylim, color="#1d5f99", width=2.4, fill="none"):
    rx = rx_value * (W - 2 * M) / (xlim[1] - xlim[0])
    ry = ry_value * (H - 2 * M) / (ylim[1] - ylim[0])
    return f'<ellipse cx="{sx(cx, xlim):.1f}" cy="{sy(cy, ylim):.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'


def axes(xlim, ylim, xtick=None, ytick=None):
    xtick = xtick if xtick is not None else range(floor(xlim[0]), floor(xlim[1]) + 1)
    ytick = ytick if ytick is not None else range(floor(ylim[0]), floor(ylim[1]) + 1)
    out = [
        '<rect x="0" y="0" width="760" height="420" rx="18" fill="#ffffff"/>',
        f'<rect x="{M}" y="{M}" width="{W - 2 * M}" height="{H - 2 * M}" fill="#fbfcfe" stroke="#d8e1e8" stroke-width="1"/>',
    ]
    for x in xtick:
        if xlim[0] <= x <= xlim[1]:
            c = "#d9e0e7" if abs(x) < 1e-9 else "#edf0f3"
            w = 1.35 if abs(x) < 1e-9 else 0.8
            out.append(line(x, ylim[0], x, ylim[1], xlim, ylim, c, w))
    for y in ytick:
        if ylim[0] <= y <= ylim[1]:
            c = "#d9e0e7" if abs(y) < 1e-9 else "#edf0f3"
            w = 1.35 if abs(y) < 1e-9 else 0.8
            out.append(line(xlim[0], y, xlim[1], y, xlim, ylim, c, w))
    out.append(line(xlim[0], 0, xlim[1], 0, xlim, ylim, "#24323a", 1.4, arrow=True))
    out.append(line(0, ylim[0], 0, ylim[1], xlim, ylim, "#24323a", 1.4, arrow=True))
    out.append(text(xlim[1] - 0.15 * (xlim[1] - xlim[0]), -0.08 * (ylim[1] - ylim[0]), "x", xlim, ylim, "#24323a", 18))
    out.append(text(0.08 * (xlim[1] - xlim[0]), ylim[1] - 0.08 * (ylim[1] - ylim[0]), "y", xlim, ylim, "#24323a", 18))
    return "\n".join(out)


def sample(fn, xmin, xmax, n=260):
    return [(xmin + (xmax - xmin) * i / (n - 1), fn(xmin + (xmax - xmin) * i / (n - 1))) for i in range(n)]


def clipped_line_for_level(kind, c, xlim, ylim):
    points = []
    for i in range(240):
        x = xlim[0] + (xlim[1] - xlim[0]) * i / 239
        if kind == "x-y":
            y = x - c
        elif kind == "quarter-x-plus-y":
            y = c - 0.25 * x
        elif kind == "quarter-x-minus-y":
            y = 0.25 * x - c
        else:
            y = c - x
        if ylim[0] <= y <= ylim[1]:
            points.append((x, y))
    return points


def write(name, xlim, ylim, title, body):
    defs = """
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#24323a"/>
  </marker>
</defs>
"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
{defs}
<style>
  text {{ font-family: Arial, sans-serif; }}
</style>
{axes(xlim, ylim)}
<text x="{M + 12}" y="{M - 22}" fill="#334" font-size="20">{escape(title)}</text>
{body}
</svg>
"""
    (OUT_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")


def circles_graph(name, title, xlim, ylim, levels, radius_from_level, label_prefix):
    body = []
    colors = ["#1d5f99", "#2476a8", "#2c8c7c", "#d27a22", "#c92331"]
    for i, level in enumerate(levels):
        r = radius_from_level(level)
        if r == 0:
            body.append(f'<circle cx="{sx(0, xlim):.1f}" cy="{sy(0, ylim):.1f}" r="5" fill="#c92331"/>')
        else:
            body.append(circle(0, 0, r, xlim, ylim, colors[i % len(colors)], 2.5))
        body.append(text(r * 0.68 if r else 0.25, r * 0.68 if r else 0.2, f"{label_prefix}{level:g}", xlim, ylim, colors[i % len(colors)], 16))
    write(name, xlim, ylim, title, "\n".join(body))


def graph_mv_1():
    xlim, ylim = (-5, 5), (-3, 3)
    body = []
    colors = ["#1d5f99", "#2476a8", "#2c8c7c", "#d27a22"]
    for level, color in zip([1, 2, 4, 6], colors):
        body.append(ellipse(0, 0, 2 * sqrt(level), sqrt(level), xlim, ylim, color, 2.5))
        body.append(text(1.35 * sqrt(level), 0.7 * sqrt(level), f"c={level:g}", xlim, ylim, color, 16))
    write("example_mv_1", xlim, ylim, "f=(1/4)x^2+y^2", "\n".join(body))


def graph_mv_2():
    def z(x, y):
        return 0.25 * x + y

    def project(x, y, z_value):
        return 380 + 72 * x - 50 * y, 220 - 22 * x - 22 * y - 34 * z_value

    def p3(points):
        return " ".join(f"{project(x, y, z_value)[0]:.1f},{project(x, y, z_value)[1]:.1f}" for x, y, z_value in points)

    def line3(a, b, color="#24323a", width=1.4, dash=None, arrow=False):
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        if arrow:
            extra += ' marker-end="url(#arrow)"'
        return f'<polyline points="{p3([a, b])}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

    plane_corners = [(-2, -2, z(-2, -2)), (2, -2, z(2, -2)), (2, 2, z(2, 2)), (-2, 2, z(-2, 2))]
    grid = []
    for x in [-2, -1, 0, 1, 2]:
        grid.append(line3((x, -2, z(x, -2)), (x, 2, z(x, 2)), "#8fb7df", 1.0))
    for y in [-2, -1, 0, 1, 2]:
        grid.append(line3((-2, y, z(-2, y)), (2, y, z(2, y)), "#8fb7df", 1.0))
    axes3 = [
        line3((-2.5, 0, 0), (2.75, 0, 0), "#24323a", 1.6, arrow=True),
        line3((0, -2.5, 0), (0, 2.75, 0), "#24323a", 1.6, arrow=True),
        line3((0, 0, -3), (0, 0, 3), "#24323a", 1.6, arrow=True),
    ]
    x_label = project(2.9, 0, 0)
    y_label = project(0, 2.95, 0)
    z_label = project(0, 0, 3.15)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="z=(1/4)x+y">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#24323a"/>
  </marker>
</defs>
<style>
  text {{ font-family: Arial, sans-serif; }}
</style>
<rect x="0" y="0" width="760" height="420" rx="18" fill="#ffffff"/>
<rect x="54" y="36" width="652" height="336" fill="#fbfcfe" stroke="#d8e1e8" stroke-width="1"/>
<text x="70" y="36" fill="#334" font-size="20">z=(1/4)x+y</text>
{"\n".join(axes3)}
<polygon points="{p3(plane_corners)}" fill="#8dbcea" fill-opacity="0.62" stroke="#376f9f" stroke-width="2.2"/>
{"\n".join(grid)}
<text x="{x_label[0]:.1f}" y="{x_label[1]:.1f}" fill="#24323a" font-size="18">x</text>
<text x="{y_label[0]:.1f}" y="{y_label[1]:.1f}" fill="#24323a" font-size="18">y</text>
<text x="{z_label[0]:.1f}" y="{z_label[1]:.1f}" fill="#24323a" font-size="18">z</text>
<text x="84" y="346" fill="#174bb4" font-size="16">x +1 -> z +1/4</text>
<text x="84" y="368" fill="#c92331" font-size="16">y +1 -> z +1</text>
</svg>
"""
    (OUT_DIR / "example_mv_2.svg").write_text(svg, encoding="utf-8")


def graph_mv_3():
    xlim, ylim = (-4, 4), (-3, 3)
    body = []
    for c, color in [(-2, "#8aa6c8"), (-1, "#487eb0"), (0, "#2c8c7c"), (1, "#d27a22"), (2, "#c92331")]:
        points = clipped_line_for_level("quarter-x-minus-y", c, xlim, ylim)
        body.append(poly(points, xlim, ylim, color, 2.4))
        if points:
            body.append(text(points[len(points) // 2][0], points[len(points) // 2][1] + 0.22, f"c={c}", xlim, ylim, color, 15))
    write("example_mv_3", xlim, ylim, "f=(1/4)x-y", "\n".join(body))


def graph_mv_4():
    circles_graph("example_mv_4", "f=4-x^2-y^2", (-3, 3), (-3, 3), [4, 3, 0, -4], lambda c: sqrt(max(0, 4 - c)), "c=")


def graph_mv_5():
    circles_graph("example_mv_5", "T=100-x^2-y^2", (-11, 11), (-11, 11), [90, 70, 50, 10], lambda c: sqrt(100 - c), "T=")


def graph_partial_1():
    xlim, ylim = (-4, 2), (-3, 7)
    curve = sample(lambda x: x * x + 3 * x + 1, xlim[0], xlim[1])
    tangent = sample(lambda x: 3 * x + 1, xlim[0], xlim[1])
    body = poly(curve, xlim, ylim, "#174bb4", 3) + poly(tangent, xlim, ylim, "#c92331", 2.5, "8 7")
    body += text(-2.2, 5.7, "y=1 slice", xlim, ylim, "#174bb4", 16)
    body += text(0.4, 2.7, "slope 3 at x=0", xlim, ylim, "#c92331", 16)
    write("example_partial_1", xlim, ylim, "f=x^2+3xy+y^2", body)


def graph_partial_2():
    xlim, ylim = (-2 * pi, 2 * pi), (-4.5, 4.5)
    t = sample(lambda y: sin(y), xlim[0], xlim[1])
    u = sample(lambda y: 4 * sin(y), xlim[0], xlim[1])
    body = poly(t, xlim, ylim, "#174bb4", 3) + poly(u, xlim, ylim, "#c92331", 3)
    body += text(-4.8, 1.4, "x=1", xlim, ylim, "#174bb4", 16)
    body += text(4.1, -3.4, "x=2", xlim, ylim, "#c92331", 16)
    write("example_partial_2", xlim, ylim, "x^2 sin y", body)


def graph_partial_3():
    xlim, ylim = (-2, 2), (-0.2, 8.2)
    curve = sample(lambda t: exp(t), xlim[0], xlim[1])
    body = poly(curve, xlim, ylim, "#174bb4", 3)
    body += poly(curve, xlim, ylim, "#c92331", 2.4, "9 6")
    body += text(0.55, 5.2, "e^t slice", xlim, ylim, "#174bb4", 16)
    write("example_partial_3", xlim, ylim, "f=e^(xy)", body)


def graph_partial_4():
    xlim, ylim = (-2, 2), (-5, 6)
    a = sample(lambda t: t * t + 1, xlim[0], xlim[1])
    b = sample(lambda t: 2 * t, xlim[0], xlim[1])
    body = poly(a, xlim, ylim, "#174bb4", 3) + poly(b, xlim, ylim, "#c92331", 3)
    body += text(-1.2, 4.4, "f(x,1,1)", xlim, ylim, "#174bb4", 16)
    body += text(1.05, 2.8, "f(1,y,1)", xlim, ylim, "#c92331", 16)
    write("example_partial_4", xlim, ylim, "slice of x^2y+yz^3", body)


def graph_partial_5():
    xlim, ylim = (-4, 4), (-4, 4)
    body = []
    for level, color in [(34, "#8aa6c8"), (42, "#487eb0"), (50, "#2c8c7c"), (58, "#c92331")]:
        points = []
        for i in range(260):
            y = ylim[0] + (ylim[1] - ylim[0]) * i / 259
            x = (level - 50 + y * y) / 2
            if xlim[0] <= x <= xlim[1]:
                points.append((x, y))
        body.append(poly(points, xlim, ylim, color, 2.4))
    body.append(line(-0.5, 0, 2.8, 0, xlim, ylim, "#174bb4", 3, arrow=True))
    body.append(line(0, -0.5, 0, -2.8, xlim, ylim, "#c92331", 3, arrow=True))
    body.append(text(1.6, 0.45, "T_x=2", xlim, ylim, "#174bb4", 16))
    body.append(text(0.65, -2.1, "T_y=-2y", xlim, ylim, "#c92331", 16))
    write("example_partial_5", xlim, ylim, "T=50+2x-y^2", "\n".join(body))


def graph_diff_1():
    xlim, ylim = (-3, 3), (-3, 3)
    body = []
    for c, color in [(2, "#8aa6c8"), (4, "#487eb0"), (7, "#2c8c7c"), (10, "#c92331")]:
        points = []
        for i in range(361):
            th = 2 * pi * i / 360
            denom = cos(th) ** 2 + cos(th) * sin(th) + sin(th) ** 2
            r = sqrt(c / denom)
            points.append((r * cos(th), r * sin(th)))
        body.append(poly(points, xlim, ylim, color, 2.2))
    body.append(f'<circle cx="{sx(1, xlim):.1f}" cy="{sy(2, ylim):.1f}" r="6" fill="#111"/>')
    body.append(text(1.35, 2.25, "(1,2)", xlim, ylim, "#111", 16))
    write("example_diff_1", xlim, ylim, "f=x^2+xy+y^2", "\n".join(body))


def graph_diff_2():
    xlim, ylim = (-2, 2), (-6, 8)
    a = sample(lambda t: t * t + 1, xlim[0], xlim[1])
    b = sample(lambda t: t + t**3, xlim[0], xlim[1])
    body = poly(a, xlim, ylim, "#174bb4", 3) + poly(b, xlim, ylim, "#c92331", 3)
    body += text(-1.25, 5.0, "f(x,1)", xlim, ylim, "#174bb4", 16)
    body += text(1.05, 4.7, "f(1,y)", xlim, ylim, "#c92331", 16)
    write("example_diff_2", xlim, ylim, "f=x^2y+y^3", body)


def graph_diff_3():
    xlim, ylim = (-0.2, 2.2), (-1, 10)
    curve = sample(lambda t: 2 * t * t, xlim[0], xlim[1])
    tangent = sample(lambda t: 4 * t - 2, xlim[0], xlim[1])
    body = poly(curve, xlim, ylim, "#174bb4", 3) + poly(tangent, xlim, ylim, "#c92331", 2.6, "8 7")
    body += f'<circle cx="{sx(1, xlim):.1f}" cy="{sy(2, ylim):.1f}" r="6" fill="#111"/>'
    body += text(1.2, 2.35, "t=1", xlim, ylim, "#111", 16)
    write("example_diff_3", xlim, ylim, "slice and tangent plane", body)


def graph_diff_4():
    xlim, ylim = (-3, 3), (-3, 3)
    body = []
    for c, color in [(1, "#487eb0"), (2, "#2c8c7c"), (3, "#c92331")]:
        diamond = [(0, c), (c, 0), (0, -c), (-c, 0), (0, c)]
        body.append(poly(diamond, xlim, ylim, color, 2.4))
        body.append(text(c * 0.45, c * 0.45, f"c={c}", xlim, ylim, color, 16))
    write("example_diff_4", xlim, ylim, "f=|x|+|y|", "\n".join(body))


def graph_diff_5():
    xlim, ylim = (-2, 2), (-0.2, 1.7)
    t = sample(lambda x: 0, xlim[0], xlim[1])
    d = sample(lambda x: abs(x) / sqrt(2), xlim[0], xlim[1])
    body = poly(t, xlim, ylim, "#174bb4", 3, "9 6") + poly(d, xlim, ylim, "#c92331", 3)
    body += text(-1.15, 0.25, "axis", xlim, ylim, "#174bb4", 16)
    body += text(1.15, 1.15, "y=x", xlim, ylim, "#c92331", 16)
    write("example_diff_5", xlim, ylim, "direction slices", body)


def graph_cn_1():
    xlim, ylim = (-2, 2), (-0.2, 2.4)
    body = poly(sample(abs, xlim[0], xlim[1]), xlim, ylim, "#c92331", 3)
    body += text(0.55, 0.45, "corner at x=0", xlim, ylim, "#c92331", 16)
    write("example_cn_1", xlim, ylim, "f=|x|+y^2 at y=0", body)


def graph_cn_2():
    xlim, ylim = (-2, 2), (-6, 10)
    a = sample(lambda t: t**3 + t, xlim[0], xlim[1])
    b = sample(lambda t: t + t * t, xlim[0], xlim[1])
    body = poly(a, xlim, ylim, "#174bb4", 3) + poly(b, xlim, ylim, "#c92331", 3)
    body += text(-1.2, -4.0, "f(x,1)", xlim, ylim, "#174bb4", 16)
    body += text(1.0, 3.6, "f(1,y)", xlim, ylim, "#c92331", 16)
    write("example_cn_2", xlim, ylim, "f=x^3y+xy^2", body)


def graph_cn_3():
    xlim, ylim = (-1.35, 1.35), (-0.2, 10)
    curve = sample(lambda t: (1 + t * t) * exp(t * t), xlim[0], xlim[1])
    body = poly(curve, xlim, ylim, "#174bb4", 3)
    body += poly(curve, xlim, ylim, "#c92331", 2.2, "8 7")
    body += text(0.65, 4.2, "f_xy=f_yx", xlim, ylim, "#174bb4", 16)
    write("example_cn_3", xlim, ylim, "mixed partials", body)


def graph_cn_4():
    xlim, ylim = (-2, 2), (-2.3, 2.3)
    a = sample(abs, xlim[0], xlim[1])
    b = sample(lambda t: -abs(t), xlim[0], xlim[1])
    body = poly(a, xlim, ylim, "#174bb4", 3) + poly(b, xlim, ylim, "#c92331", 3)
    body += text(-1.05, 1.25, "x=1", xlim, ylim, "#174bb4", 16)
    body += text(1.05, -1.25, "x=-1", xlim, ylim, "#c92331", 16)
    write("example_cn_4", xlim, ylim, "f=x|y|", body)


def graph_cn_5():
    xlim, ylim = (-3, 3), (-2.2, 2.2)
    body = []
    for c, color in [(0.5, "#8aa6c8"), (1, "#487eb0"), (2, "#2c8c7c"), (3, "#c92331")]:
        right = []
        left = []
        ymax = sqrt(c)
        for i in range(240):
            y = -ymax + 2 * ymax * i / 239
            x = c - y * y
            right.append((x, y))
            left.append((-x, y))
        body.append(poly(right, xlim, ylim, color, 2.4))
        body.append(poly(left, xlim, ylim, color, 2.4))
    body.append(text(0.35, 1.85, "fold along x=0", xlim, ylim, "#c92331", 16))
    write("example_cn_5", xlim, ylim, "f=|x|+y^2", "\n".join(body))


def main():
    graph_mv_1()
    graph_mv_2()
    graph_mv_3()
    graph_mv_4()
    graph_mv_5()
    graph_partial_1()
    graph_partial_2()
    graph_partial_3()
    graph_partial_4()
    graph_partial_5()
    graph_diff_1()
    graph_diff_2()
    graph_diff_3()
    graph_diff_4()
    graph_diff_5()
    graph_cn_1()
    graph_cn_2()
    graph_cn_3()
    graph_cn_4()
    graph_cn_5()


if __name__ == "__main__":
    main()
