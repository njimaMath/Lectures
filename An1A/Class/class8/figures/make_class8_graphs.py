#!/usr/bin/env python3
from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/class8_mplconfig")

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


OUT_DIR = Path(__file__).resolve().parent
JP_FONT_PATH = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"

if Path(JP_FONT_PATH).exists():
    font_manager.fontManager.addfont(JP_FONT_PATH)
    JP_FONT = font_manager.FontProperties(fname=JP_FONT_PATH).get_name()
else:
    JP_FONT = "DejaVu Sans"

plt.rcParams.update(
    {
        "font.family": JP_FONT,
        "mathtext.fontset": "dejavusans",
        "axes.unicode_minus": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def save(fig, name):
    fig.savefig(OUT_DIR / name, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def save_pair(fig, stem):
    fig.savefig(OUT_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT_DIR / f"{stem}.png", dpi=180, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def setup_plane_axis(ax, xlim, ylim, xticks=None, yticks=None, aspect=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if aspect:
        ax.set_aspect("equal", adjustable="box")
    ax.grid(True, which="major", color="#dddddd", linewidth=0.55)
    ax.grid(True, which="minor", color="#eeeeee", linewidth=0.35)
    ax.minorticks_on()
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_linewidth(0.8)
    ax.spines["left"].set_linewidth(0.8)
    ax.tick_params(labelsize=9, length=3, width=0.6, pad=2)


def axis_labels(ax, xlim, ylim, xlabel="$x$", ylabel="$y$"):
    ax.annotate(
        "",
        xy=(xlim[1], 0),
        xytext=(xlim[1] - 0.05 * (xlim[1] - xlim[0]), 0),
        arrowprops={"arrowstyle": "->", "lw": 0.8, "color": "black"},
        clip_on=False,
    )
    ax.annotate(
        "",
        xy=(0, ylim[1]),
        xytext=(0, ylim[1] - 0.05 * (ylim[1] - ylim[0])),
        arrowprops={"arrowstyle": "->", "lw": 0.8, "color": "black"},
        clip_on=False,
    )
    ax.text(xlim[1], 0.08 * (ylim[1] - ylim[0]), xlabel, ha="right", va="bottom", fontsize=11)
    ax.text(0.04 * (xlim[1] - xlim[0]), ylim[1], ylabel, ha="left", va="top", fontsize=11)


def setup_surface_axis(ax, xlim, ylim, zlim, view=(27, -58)):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    ax.set_xlabel("$x$", labelpad=2)
    ax.set_ylabel("$y$", labelpad=2)
    ax.set_zlabel("$z$", labelpad=2)
    ax.view_init(elev=view[0], azim=view[1])
    ax.tick_params(labelsize=8, pad=0)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
        axis.pane.set_edgecolor("#cccccc")
    ax.grid(True, color="#d0d0d0")


def graph_domain_sqrt():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    xlim = (-3, 3)
    ylim = (-3, 3)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2])
    ax.fill([-3, 3, 3], [3, -3, 3], color="#dfe3ff", zorder=0)
    xs = np.linspace(-3, 3, 300)
    ax.plot(xs, -xs, color="#001fc4", linewidth=2.0, zorder=3)
    ax.text(-2.9, 1.25, "$x+y=0$", color="#001fc4", fontsize=11, rotation=-43)
    ax.text(
        1.05,
        1.35,
        "$x+y\\geq 0$",
        fontsize=11,
        bbox={"boxstyle": "round,pad=0.25", "fc": "#dfe3ff", "ec": "#4e65c8", "lw": 0.8},
    )
    ax.text(-2.75, -1.75, "定義されない", color="#8f8f8f", fontsize=9)
    axis_labels(ax, xlim, ylim)
    save(fig, "domain_sqrt.pdf")


def graph_domain_rational():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    xlim = (-2.4, 2.4)
    ylim = (-2.4, 2.4)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2])
    ax.set_facecolor("#e6ffe7")
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="white", linewidth=5.0, zorder=3)
    ax.plot(np.cos(theta), np.sin(theta), color="#c40b19", linestyle=(0, (3, 2)), linewidth=2.0, zorder=4)
    ax.annotate(
        "$x^2+y^2=1$",
        xy=(0, 1),
        xytext=(-0.85, 1.55),
        color="#c40b19",
        fontsize=11,
        arrowprops={"arrowstyle": "->", "color": "#c40b19", "lw": 1.0},
        bbox={"fc": "white", "ec": "none", "pad": 1.2},
    )
    ax.text(
        -1.35,
        -1.8,
        "$x^2+y^2\\neq 1$",
        fontsize=11,
        bbox={"boxstyle": "round,pad=0.25", "fc": "#e6ffe7", "ec": "#237a36", "lw": 0.8},
    )
    axis_labels(ax, xlim, ylim)
    save(fig, "domain_rational.pdf")


def graph_paraboloid_contours():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    xlim = (-2.3, 2.3)
    ylim = (-2.3, 2.3)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2])
    theta = np.linspace(0, 2 * np.pi, 500)
    color = "#006c70"
    for c, label_xy in [(1, (0.47, 0.48)), (2, (0.9, 1.0)), (3, (1.35, 1.45))]:
        r = np.sqrt(c)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=color, linewidth=1.5)
        ax.text(*label_xy, f"$c={c}$", color=color, fontsize=10, bbox={"fc": "white", "ec": "none", "pad": 0.5})
    axis_labels(ax, xlim, ylim)
    save(fig, "paraboloid_contours.pdf")


def graph_paraboloid_surface():
    fig = plt.figure(figsize=(3.25, 2.65))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-2, 2, 70)
    y = np.linspace(-2, 2, 70)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0.0, antialiased=True, alpha=0.96)
    setup_surface_axis(ax, (-2, 2), (-2, 2), (0, 8), view=(24, -48))
    ax.set_zticks([0, 5])
    save(fig, "paraboloid_surface.pdf")


def graph_plane_surface():
    fig = plt.figure(figsize=(3.25, 2.65))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-2, 2, 2)
    y = np.linspace(-2, 2, 2)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    cmap = LinearSegmentedColormap.from_list("plane", ["#78aae6", "#ebf5ff"])
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0.5, edgecolor="#6f8eb2", alpha=0.9)
    setup_surface_axis(ax, (-2, 2), (-2, 2), (-4, 4), view=(24, -48))
    ax.set_zticks([-4, -2, 0, 2, 4])
    save(fig, "plane_surface.pdf")


def graph_temperature_contours():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    xlim = (-11, 11)
    ylim = (-11, 11)
    setup_plane_axis(ax, xlim, ylim, [-10, -5, 0, 5, 10], [-10, -5, 0, 5, 10])
    theta = np.linspace(0, 2 * np.pi, 500)
    color = "#c76300"
    label_pos = {90: (1.25, 2.05), 70: (3.2, 4.05), 50: (-7.2, 4.4), 10: (6.9, 8.45)}
    for level in [90, 70, 50, 10]:
        r = np.sqrt(100 - level)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=color, linewidth=1.45)
        ax.text(*label_pos[level], f"$T={level}$", color=color, fontsize=10, bbox={"fc": "white", "ec": "none", "pad": 0.5})
    ax.scatter([0], [0], color="#bd1f1f", s=16, zorder=4)
    ax.annotate(
        "中心が高温",
        xy=(0, 0),
        xytext=(0.7, -2.45),
        color="#bd1f1f",
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "#bd1f1f", "lw": 0.9},
        bbox={"fc": "white", "ec": "none", "pad": 0.5},
    )
    axis_labels(ax, xlim, ylim)
    save(fig, "temperature_contours.pdf")


def graph_partial_directions():
    fig, ax = plt.subplots(figsize=(3.7, 2.8))
    xlim = (-3.0, 3.2)
    ylim = (-2.2, 2.4)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(-3, 4, 1))
    ax.set_yticks(np.arange(-2, 3, 1))
    ax.grid(True, color="#dcdcdc", linewidth=0.55)
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.annotate("", xy=(xlim[1], 0), xytext=(xlim[0], 0), arrowprops={"arrowstyle": "->", "lw": 0.9, "color": "black"})
    ax.annotate("", xy=(0, ylim[1]), xytext=(0, ylim[0]), arrowprops={"arrowstyle": "->", "lw": 0.9, "color": "black"})
    ax.text(xlim[1], -0.08, "$x$", ha="right", va="top", fontsize=11)
    ax.text(0.08, ylim[1], "$y$", ha="left", va="top", fontsize=11)
    a, b = 0.8, 0.7
    ax.plot([a], [b], "o", color="black", markersize=4)
    ax.text(a + 0.1, b + 0.12, "$(a,b)$", fontsize=10)
    ax.axhline(b, color="#c92331", linewidth=1.0, linestyle=(0, (3, 2)), alpha=0.65)
    ax.axvline(a, color="#174bb4", linewidth=1.0, linestyle=(0, (3, 2)), alpha=0.65)
    ax.annotate("", xy=(2.4, b), xytext=(a, b), arrowprops={"arrowstyle": "->", "lw": 2.0, "color": "#c92331"})
    ax.annotate("", xy=(a, 1.95), xytext=(a, b), arrowprops={"arrowstyle": "->", "lw": 2.0, "color": "#174bb4"})
    ax.text(1.45, b - 0.35, "$x$ 方向", color="#c92331", fontsize=10)
    ax.text(a + 0.15, 1.38, "$y$ 方向", color="#174bb4", fontsize=10)
    save(fig, "partial_directions.pdf")


def graph_partial_surface():
    fig = plt.figure(figsize=(4.65, 2.9))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-2, 2, 70)
    y = np.linspace(-2, 2, 70)
    X, Y = np.meshgrid(x, y)
    Z = 0.35 * X**2 + 0.18 * Y**2 + 0.7 * X - 0.45 * Y + 1
    cmap = LinearSegmentedColormap.from_list("soft", ["#d7ebff", "#5a96d2"])
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True, alpha=0.72)
    xs = np.linspace(-2, 2, 160)
    ys = np.linspace(-2, 2, 160)
    ax.plot(xs, 0.8 * np.ones_like(xs), 0.35 * xs**2 + 0.18 * 0.8**2 + 0.7 * xs - 0.45 * 0.8 + 1, color="#c92331", linewidth=2.1)
    ax.plot(0.4 * np.ones_like(ys), ys, 0.35 * 0.4**2 + 0.18 * ys**2 + 0.7 * 0.4 - 0.45 * ys + 1, color="#174bb4", linewidth=2.1)
    ax.scatter([0.4], [0.8], [1.012], color="black", s=18)
    ax.text(-1.85, 0.8, 2.25, "$y=b$ で切る", color="#c92331", fontsize=9)
    ax.text(0.4, -1.8, 2.1, "$x=a$ で切る", color="#174bb4", fontsize=9)
    setup_surface_axis(ax, (-2, 2), (-2, 2), (-1, 5), view=(24, -52))
    save(fig, "partial_surface.pdf")


def graph_tangent_plane():
    fig = plt.figure(figsize=(4.55, 2.9))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-1.4, 2.2, 70)
    y = np.linspace(-0.7, 2.7, 70)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    P = 2 * X + 2 * Y - 2
    cmap = LinearSegmentedColormap.from_list("surface", ["#d7f0eb", "#28917d"])
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True, alpha=0.78)
    ax.plot_surface(X, Y, P, color="#e35f5f", linewidth=0.7, edgecolor="#c92331", alpha=0.34)
    ax.scatter([1], [1], [2], color="black", s=18)
    ax.text(1.78, 0.05, 2.25, "接平面", color="#c92331", fontsize=9)
    ax.text(1.08, 1.06, 2.55, "$(1,1,2)$", color="black", fontsize=9)
    setup_surface_axis(ax, (-1.4, 2.2), (-0.7, 2.7), (-1, 8), view=(24, -52))
    save(fig, "tangent_plane.pdf")


def graph_nondiff_surface():
    fig = plt.figure(figsize=(3.25, 2.65))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-2, 2, 90)
    y = np.linspace(-2, 2, 90)
    X, Y = np.meshgrid(x, y)
    Z = X * Y / np.sqrt(X**2 + Y**2 + 0.02)
    cmap = LinearSegmentedColormap.from_list("mixed", ["#3c6ebe", "#f5f5f5", "#d2463c"])
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True, alpha=0.92)
    setup_surface_axis(ax, (-2, 2), (-2, 2), (-1.2, 1.2), view=(25, -48))
    ax.set_zticks([-1, 0, 1])
    save(fig, "nondiff_surface.pdf")


def graph_direction_slice():
    fig, ax = plt.subplots(figsize=(3.15, 2.45))
    xlim = (-2, 2)
    ylim = (-0.3, 1.7)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [0, 0.5, 1.0, 1.5], aspect=False)
    t = np.linspace(-2, 2, 400)
    ax.plot(t, np.abs(t) / np.sqrt(2), color="#c92331", linewidth=2.0, label="$f(t,t)$")
    ax.plot(t, np.zeros_like(t), color="#174bb4", linewidth=2.0, linestyle="--", label="$f(t,0)$")
    axis_labels(ax, xlim, ylim, xlabel="$t$", ylabel="値")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=8, frameon=True, edgecolor="#cccccc")
    save(fig, "direction_slice.pdf")


def graph_abs_value():
    fig, ax = plt.subplots(figsize=(3.15, 2.45))
    xlim = (-2, 2)
    ylim = (-0.4, 2.4)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [0, 1, 2], aspect=False)
    x = np.linspace(-2, 2, 400)
    ax.plot(x, np.abs(x), color="black", linewidth=2.0, label="$|x|$")
    axis_labels(ax, xlim, ylim, xlabel="$x$", ylabel="$|x|$")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), fontsize=8, frameon=True, edgecolor="#cccccc")
    save(fig, "abs_value.pdf")


def graph_derivative_line():
    fig, ax = plt.subplots(figsize=(3.15, 2.45))
    xlim = (-2, 2)
    ylim = (-2.4, 2.4)
    setup_plane_axis(ax, xlim, ylim, [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2], aspect=False)
    x = np.linspace(-2, 2, 400)
    ax.plot(x, 2 * x, color="#007a75", linewidth=2.0, label="$x^2$ の導関数")
    axis_labels(ax, xlim, ylim, xlabel="$x$", ylabel="$2x$")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), fontsize=8, frameon=True, edgecolor="#cccccc")
    save(fig, "derivative_line.pdf")


def mesh(xlim, ylim, n=85):
    x = np.linspace(xlim[0], xlim[1], n)
    y = np.linspace(ylim[0], ylim[1], n)
    return np.meshgrid(x, y)


def example_surface(stem, func, xlim, ylim, zlim, view=(25, -48), cmap="viridis", point=None):
    fig = plt.figure(figsize=(4.0, 2.75))
    ax = fig.add_subplot(111, projection="3d")
    X, Y = mesh(xlim, ylim)
    Z = func(X, Y)
    ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True, alpha=0.92)
    if point is not None:
        px, py, pz, label = point
        ax.scatter([px], [py], [pz], color="black", s=18)
        if label:
            ax.text(px, py, pz, label, color="black", fontsize=9)
    setup_surface_axis(ax, xlim, ylim, zlim, view=view)
    save_pair(fig, stem)


def example_contours(stem, func, xlim, ylim, levels, fill=True):
    fig, ax = plt.subplots(figsize=(3.25, 2.75))
    X, Y = mesh(xlim, ylim, n=180)
    Z = func(X, Y)
    if fill:
        ax.contourf(X, Y, Z, levels=24, cmap="YlGnBu", alpha=0.72)
    lines = ax.contour(X, Y, Z, levels=levels, colors="#1d5f99", linewidths=1.25)
    ax.clabel(lines, inline=True, fontsize=8, fmt="%g")
    xticks = np.linspace(np.ceil(xlim[0]), np.floor(xlim[1]), 5)
    yticks = np.linspace(np.ceil(ylim[0]), np.floor(ylim[1]), 5)
    setup_plane_axis(ax, xlim, ylim, xticks, yticks)
    axis_labels(ax, xlim, ylim)
    save_pair(fig, stem)


def example_line(stem, xlim, ylim, lines, xlabel="$x$", ylabel="値"):
    fig, ax = plt.subplots(figsize=(3.35, 2.55))
    setup_plane_axis(ax, xlim, ylim, aspect=False)
    for x, y, label, color, style in lines:
        ax.plot(x, y, color=color, linewidth=2.0, linestyle=style, label=label)
    axis_labels(ax, xlim, ylim, xlabel=xlabel, ylabel=ylabel)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=min(2, len(lines)), fontsize=8, frameon=True, edgecolor="#cccccc")
    save_pair(fig, stem)


def graph_example_mv_1():
    example_contours("example_mv_1", lambda X, Y: X**2 + Y**2, (-3, 3), (-3, 3), [1, 2, 4, 6, 8])


def graph_example_mv_2():
    example_surface("example_mv_2", lambda X, Y: X + Y, (-2, 2), (-2, 2), (-4, 4), cmap="Blues")


def graph_example_mv_3():
    example_contours("example_mv_3", lambda X, Y: X - Y, (-3, 3), (-3, 3), [-2, -1, 0, 1, 2], fill=False)


def graph_example_mv_4():
    example_contours("example_mv_4", lambda X, Y: 4 - X**2 - Y**2, (-3, 3), (-3, 3), [-4, -1, 0, 2, 3, 4])


def graph_example_mv_5():
    example_contours("example_mv_5", lambda X, Y: 100 - X**2 - Y**2, (-11, 11), (-11, 11), [10, 30, 50, 70, 90])


def graph_example_partial_1():
    example_surface(
        "example_partial_1",
        lambda X, Y: X**2 + 3 * X * Y + Y**2,
        (-2, 2),
        (-2, 2),
        (-5, 10),
        view=(27, -52),
        cmap="PuBuGn",
    )


def graph_example_partial_2():
    y = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    example_line(
        "example_partial_2",
        (-2 * np.pi, 2 * np.pi),
        (-4.4, 4.4),
        [
            (y, np.sin(y), "$x=1$", "#174bb4", "-"),
            (y, 4 * np.sin(y), "$x=2$", "#c92331", "-"),
        ],
        xlabel="$y$",
        ylabel="$x^2\\sin y$",
    )


def graph_example_partial_3():
    example_surface("example_partial_3", lambda X, Y: np.exp(X * Y), (-1.5, 1.5), (-1.5, 1.5), (0, 10), cmap="viridis")


def graph_example_partial_4():
    example_surface(
        "example_partial_4",
        lambda X, Y: X**2 * Y + Y,
        (-2, 2),
        (-2, 2),
        (-10, 10),
        view=(25, -55),
        cmap="coolwarm",
    )


def graph_example_partial_5():
    fig, ax = plt.subplots(figsize=(3.35, 2.75))
    xlim = (-4, 4)
    ylim = (-4, 4)
    X, Y = mesh(xlim, ylim, n=160)
    T = 50 + 2 * X - Y**2
    ax.contourf(X, Y, T, levels=24, cmap="YlOrRd", alpha=0.72)
    lines = ax.contour(X, Y, T, levels=[34, 42, 50, 58], colors="#6d2d00", linewidths=1.1)
    ax.clabel(lines, inline=True, fontsize=8, fmt="%g")
    setup_plane_axis(ax, xlim, ylim, [-4, -2, 0, 2, 4], [-4, -2, 0, 2, 4])
    ax.annotate("", xy=(2.8, 0), xytext=(0.6, 0), arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#174bb4"})
    ax.annotate("", xy=(0, -2.7), xytext=(0, -0.5), arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#c92331"})
    ax.text(1.15, 0.32, "$T_x=2$", color="#174bb4", fontsize=10)
    ax.text(0.28, -1.95, "$T_y=-2y$", color="#c92331", fontsize=10)
    axis_labels(ax, xlim, ylim)
    save_pair(fig, "example_partial_5")


def graph_example_diff_1():
    example_surface(
        "example_diff_1",
        lambda X, Y: X**2 + X * Y + Y**2,
        (-0.5, 2.5),
        (0, 3),
        (0, 14),
        view=(24, -54),
        cmap="YlGnBu",
        point=(1, 2, 7, "$(1,2)$"),
    )


def graph_example_diff_2():
    example_surface("example_diff_2", lambda X, Y: X**2 * Y + Y**3, (-2, 2), (-1.6, 1.6), (-8, 8), cmap="Spectral")


def graph_example_diff_3():
    fig = plt.figure(figsize=(4.0, 2.75))
    ax = fig.add_subplot(111, projection="3d")
    xlim = (-0.6, 2.3)
    ylim = (-0.6, 2.3)
    X, Y = mesh(xlim, ylim)
    Z = X**2 + Y**2
    P = 2 * X + 2 * Y - 2
    ax.plot_surface(X, Y, Z, cmap="Greens", linewidth=0, antialiased=True, alpha=0.75)
    ax.plot_surface(X, Y, P, color="#e35f5f", linewidth=0.3, edgecolor="#c92331", alpha=0.35)
    ax.scatter([1], [1], [2], color="black", s=18)
    ax.text(1.05, 1.05, 2.4, "$(1,1,2)$", color="black", fontsize=9)
    setup_surface_axis(ax, xlim, ylim, (-1, 9), view=(24, -52))
    save_pair(fig, "example_diff_3")


def graph_example_diff_4():
    example_surface("example_diff_4", lambda X, Y: np.abs(X) + np.abs(Y), (-2, 2), (-2, 2), (0, 4), cmap="Oranges")


def graph_example_diff_5():
    t = np.linspace(-2, 2, 450)
    example_line(
        "example_diff_5",
        (-2, 2),
        (-0.2, 1.7),
        [
            (t, np.zeros_like(t), "$f(t,0)$", "#174bb4", "--"),
            (t, np.abs(t) / np.sqrt(2), "$f(t,t)$", "#c92331", "-"),
        ],
        xlabel="$t$",
        ylabel="値",
    )


def graph_example_cn_1():
    example_surface("example_cn_1", lambda X, Y: np.abs(X) + Y**2, (-2, 2), (-2, 2), (0, 6), cmap="YlGn")


def graph_example_cn_2():
    example_surface("example_cn_2", lambda X, Y: X**3 * Y + X * Y**2, (-1.6, 1.6), (-1.6, 1.6), (-10, 10), cmap="coolwarm")


def graph_example_cn_3():
    example_surface("example_cn_3", lambda X, Y: np.exp(X * Y), (-1.5, 1.5), (-1.5, 1.5), (0, 10), cmap="viridis")


def graph_example_cn_4():
    example_surface("example_cn_4", lambda X, Y: X * np.abs(Y), (-2, 2), (-2, 2), (-4, 4), cmap="coolwarm")


def graph_example_cn_5():
    example_contours("example_cn_5", lambda X, Y: np.abs(X) + Y**2, (-2, 2), (-2, 2), [0.5, 1, 2, 3, 4, 5])


def main():
    graph_domain_sqrt()
    graph_domain_rational()
    graph_paraboloid_contours()
    graph_paraboloid_surface()
    graph_plane_surface()
    graph_temperature_contours()
    graph_partial_directions()
    graph_partial_surface()
    graph_tangent_plane()
    graph_nondiff_surface()
    graph_direction_slice()
    graph_abs_value()
    graph_derivative_line()
    graph_example_mv_1()
    graph_example_mv_2()
    graph_example_mv_3()
    graph_example_mv_4()
    graph_example_mv_5()
    graph_example_partial_1()
    graph_example_partial_2()
    graph_example_partial_3()
    graph_example_partial_4()
    graph_example_partial_5()
    graph_example_diff_1()
    graph_example_diff_2()
    graph_example_diff_3()
    graph_example_diff_4()
    graph_example_diff_5()
    graph_example_cn_1()
    graph_example_cn_2()
    graph_example_cn_3()
    graph_example_cn_4()
    graph_example_cn_5()


if __name__ == "__main__":
    main()
