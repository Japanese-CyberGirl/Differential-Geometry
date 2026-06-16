from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.integrate import cumulative_trapezoid


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "catenoid_geodesics.html"

A = 1.0
U_MAX = 2.35
U_EXT = 3.45


@dataclass(frozen=True)
class CurveStyle:
    name: str
    color: str
    width: int = 7


def rho(u: np.ndarray | float, a: float = A) -> np.ndarray | float:
    return a * np.cosh(u)


def catenoid_xyz(
    u: np.ndarray | float,
    v: np.ndarray | float,
    a: float = A,
) -> tuple[np.ndarray | float, np.ndarray | float, np.ndarray | float]:
    radius = rho(u, a)
    return radius * np.cos(v), radius * np.sin(v), a * u


def add_curve(
    fig: go.Figure,
    u: np.ndarray,
    v: np.ndarray,
    style: CurveStyle,
    *,
    showlegend: bool = True,
    hover_text: str | None = None,
    visible: bool = True,
    opacity: float | None = None,
) -> int:
    x, y, z = catenoid_xyz(u, v)
    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            name=style.name,
            showlegend=showlegend,
            hovertemplate=(hover_text or style.name) + "<extra></extra>",
            line={"color": style.color, "width": style.width},
            visible=visible,
            opacity=opacity,
        )
    )
    return len(fig.data) - 1


def add_parallel(
    fig: go.Figure,
    u0: float,
    *,
    name: str,
    color: str = "rgba(70, 70, 70, 0.55)",
    showlegend: bool = False,
) -> None:
    v = np.linspace(0.0, 2.0 * np.pi, 360)
    u = np.full_like(v, u0)
    add_curve(
        fig,
        u,
        v,
        CurveStyle(name=name, color=color, width=4),
        showlegend=showlegend,
        hover_text=name,
    )


def cumulative_v(u: np.ndarray, clairaut_c: float, sign: float) -> np.ndarray:
    denominator = np.sqrt(np.maximum(rho(u) ** 2 - clairaut_c**2, 1e-14))
    dv_du = sign * clairaut_c / denominator
    return cumulative_trapezoid(dv_du, u, initial=0.0)


def meridian(
    v0: float,
    n: int = 600,
    u_limit: float = U_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    u = np.linspace(-u_limit, u_limit, n)
    return u, np.full_like(u, v0)


def through_spiral(
    clairaut_c: float,
    n: int = 1500,
    u_limit: float = U_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    u = np.linspace(-u_limit, u_limit, n)
    v = cumulative_v(u, clairaut_c, sign=1.0)
    return u, v - 0.5 * v[-1]


def neck_circle(n: int = 720) -> tuple[np.ndarray, np.ndarray]:
    v = np.linspace(0.0, 2.0 * np.pi, n)
    return np.zeros_like(v), v


def asymptotic_spiral(
    *,
    upper: bool,
    n: int = 1600,
    eps: float = 3e-5,
    u_limit: float = U_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    if upper:
        u = np.linspace(u_limit, eps, n)
        v = cumulative_v(u, A, sign=-1.0)
    else:
        u = np.linspace(-u_limit, -eps, n)
        v = cumulative_v(u, A, sign=1.0)
    return u, v - 0.5 * v[-1]


def reflecting_spiral(
    clairaut_c: float,
    *,
    upper: bool,
    n: int = 1200,
    eps: float = 2e-4,
    u_limit: float = U_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    u_turn = np.arccosh(clairaut_c / A)
    if upper:
        incoming = np.linspace(u_limit, u_turn + eps, n)
        outgoing = np.linspace(u_turn + eps, u_limit, n)
    else:
        incoming = np.linspace(-u_limit, -u_turn - eps, n)
        outgoing = np.linspace(-u_turn - eps, -u_limit, n)

    v_in = cumulative_v(incoming, clairaut_c, sign=-1.0 if upper else 1.0)
    v_out = v_in[-1] + cumulative_v(outgoing, clairaut_c, sign=1.0 if upper else -1.0)
    u = np.concatenate([incoming, outgoing[1:]])
    v = np.concatenate([v_in, v_out[1:]])
    return u, v - 0.5 * v[-1]


def free_spiral(n: int = 1200) -> tuple[np.ndarray, np.ndarray]:
    u = np.linspace(-U_MAX, U_MAX, n)
    v = 3.4 * u + 0.45 * np.sin(4.0 * u)
    return u, v


def wavy_loop(n: int = 1400) -> tuple[np.ndarray, np.ndarray]:
    t = np.linspace(0.0, 4.0 * np.pi, n)
    u = 0.55 + 0.35 * np.sin(3.0 * t)
    v = t
    return u, v


def surface_trace() -> go.Surface:
    u = np.linspace(-U_MAX, U_MAX, 110)
    v = np.linspace(0.0, 2.0 * np.pi, 150)
    uu, vv = np.meshgrid(u, v)
    x, y, z = catenoid_xyz(uu, vv)
    return go.Surface(
        x=x,
        y=y,
        z=z,
        name="Катеноид",
        showscale=False,
        opacity=0.58,
        colorscale=[
            [0.0, "rgb(214, 232, 246)"],
            [0.48, "rgb(246, 248, 249)"],
            [1.0, "rgb(218, 235, 225)"],
        ],
        hovertemplate="u=%{z:.2f}<extra>Катеноид</extra>",
    )


def build_figure() -> go.Figure:
    fig = go.Figure(data=[surface_trace()])

    styles = {
        "meridian": CurveStyle("1. C=0: меридианы", "#1f2a7c", 8),
        "through": CurveStyle("2. 0<C<a: сквозная спираль", "#ef6c00", 8),
        "neck": CurveStyle("3. C=a: горловина", "#c62828", 9),
        "critical": CurveStyle("4. C=a: асимптотика к горловине", "#6a1b9a", 8),
        "reflect": CurveStyle("5. C>a: отражение от запретной зоны", "#2e7d32", 8),
        "meridian_ext": CurveStyle("продолжение: меридианы", "rgba(31, 42, 124, 0.42)", 5),
        "through_ext": CurveStyle("продолжение: сквозная спираль", "rgba(239, 108, 0, 0.42)", 5),
        "critical_ext": CurveStyle("продолжение: асимптотика", "rgba(106, 27, 154, 0.42)", 5),
        "reflect_ext": CurveStyle("продолжение: отражение", "rgba(46, 125, 50, 0.42)", 5),
        "free": CurveStyle("сравнение: произвольная спираль, не геодезическая", "#6c757d", 5),
        "wavy": CurveStyle("сравнение: волнистая линия, не геодезическая", "#00838f", 5),
    }

    for index, v0 in enumerate([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0]):
        add_curve(fig, *meridian(v0), styles["meridian"], showlegend=index == 0)

    add_curve(
        fig,
        *through_spiral(0.55 * A),
        styles["through"],
        hover_text="0<C<a: геодезическая проходит через горловину",
    )

    add_curve(fig, *neck_circle(), styles["neck"], hover_text="C=a, u=0: замкнутая геодезическая")

    for upper in [True, False]:
        add_curve(
            fig,
            *asymptotic_spiral(upper=upper),
            styles["critical"],
            showlegend=upper,
            hover_text="C=a: спираль асимптотически наматывается на горловину",
        )

    reflect_c = 1.65 * A
    u_turn = np.arccosh(reflect_c / A)
    add_parallel(fig, u_turn, name="граница rho=C для C>a")
    add_parallel(fig, -u_turn, name="граница rho=C для C>a")

    for upper in [True, False]:
        add_curve(
            fig,
            *reflecting_spiral(reflect_c, upper=upper),
            styles["reflect"],
            showlegend=upper,
            hover_text="C>a: геодезическая разворачивается при rho(u)=C",
        )

    add_parallel(fig, 0.0, name="горловина rho=a", color="rgba(190, 20, 20, 0.35)")

    extension_trace_indices = []
    for index, v0 in enumerate([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0]):
        extension_trace_indices.append(
            add_curve(
                fig,
                *meridian(v0, u_limit=U_EXT),
                styles["meridian_ext"],
                showlegend=index == 0,
                visible=False,
                hover_text="Продолжение меридиана за пределы текущего куска поверхности",
                opacity=0.7,
            )
        )

    extension_trace_indices.append(
        add_curve(
            fig,
            *through_spiral(0.55 * A, u_limit=U_EXT),
            styles["through_ext"],
            visible=False,
            hover_text="Продолжение сквозной спирали на более длинном участке катеноида",
            opacity=0.7,
        )
    )

    for upper in [True, False]:
        extension_trace_indices.append(
            add_curve(
                fig,
                *asymptotic_spiral(upper=upper, u_limit=U_EXT),
                styles["critical_ext"],
                showlegend=upper,
                visible=False,
                hover_text="Продолжение критической спирали; она все равно асимптотически идет к горловине",
                opacity=0.7,
            )
        )

    for upper in [True, False]:
        extension_trace_indices.append(
            add_curve(
                fig,
                *reflecting_spiral(reflect_c, upper=upper, u_limit=U_EXT),
                styles["reflect_ext"],
                showlegend=upper,
                visible=False,
                hover_text="Продолжение отражающейся геодезической на более дальний участок",
                opacity=0.7,
            )
        )

    comparison_trace_indices = [
        add_curve(
            fig,
            *free_spiral(),
            styles["free"],
            visible=False,
            hover_text=(
                "Произвольная линия на катеноиде: она не является геодезической "
                "и добавлена только для сравнения"
            ),
        ),
        add_curve(
            fig,
            *wavy_loop(),
            styles["wavy"],
            visible=False,
            hover_text=(
                "Волнистая линия на катеноиде: не геодезическая; "
                "показывает, что не всякая линия на поверхности является геодезической"
            ),
        ),
    ]

    hidden_extra_indices = set(comparison_trace_indices + extension_trace_indices)
    comparison_indices = set(comparison_trace_indices)
    extension_indices = set(extension_trace_indices)
    geodesic_visibility = [
        index not in hidden_extra_indices for index in range(len(fig.data))
    ]
    extension_visibility = [
        index not in comparison_indices for index in range(len(fig.data))
    ]
    comparison_visibility = [
        index not in extension_indices for index in range(len(fig.data))
    ]
    all_visibility = [True for _ in fig.data]

    fig.update_layout(
        title={
            "text": "Геодезические на катеноиде: все случаи по теореме Клеро",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24, "color": "#23395d"},
        },
        legend={
            "x": 0.02,
            "y": 0.98,
            "bgcolor": "rgba(255,255,255,0.78)",
            "bordercolor": "rgba(35,57,93,0.18)",
            "borderwidth": 1,
            "font": {"size": 14},
        },
        margin={"l": 0, "r": 0, "t": 68, "b": 0},
        updatemenus=[
            {
                "type": "buttons",
                "direction": "right",
                "x": 0.5,
                "y": 1.08,
                "xanchor": "center",
                "yanchor": "top",
                "pad": {"r": 8, "t": 4},
                "buttons": [
                    {
                        "label": "Только геодезические",
                        "method": "update",
                        "args": [
                            {"visible": geodesic_visibility},
                            {
                                "title.text": (
                                    "Геодезические на катеноиде: все случаи "
                                    "по теореме Клеро"
                                )
                            },
                        ],
                    },
                    {
                        "label": "Показать продолжение",
                        "method": "update",
                        "args": [
                            {"visible": extension_visibility},
                            {
                                "title.text": (
                                    "Геодезические на катеноиде: продолжение "
                                    "за пределами текущего куска поверхности"
                                )
                            },
                        ],
                    },
                    {
                        "label": "Показать линии для сравнения",
                        "method": "update",
                        "args": [
                            {"visible": comparison_visibility},
                            {
                                "title.text": (
                                    "Геодезические на катеноиде + "
                                    "негеодезические линии для сравнения"
                                )
                            },
                        ],
                    },
                    {
                        "label": "Продолжение + сравнение",
                        "method": "update",
                        "args": [
                            {"visible": all_visibility},
                            {
                                "title.text": (
                                    "Геодезические на катеноиде: продолжение "
                                    "+ негеодезические линии для сравнения"
                                )
                            },
                        ],
                    },
                ],
            }
        ],
        scene={
            "xaxis_title": "x",
            "yaxis_title": "y",
            "zaxis_title": "z",
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.55, "y": -1.95, "z": 1.05}},
        },
        template="plotly_white",
    )
    return fig


def main() -> None:
    fig = build_figure()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT,
        include_plotlyjs=True,
        full_html=True,
        config={
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": True,
        },
    )
    print(f"Saved interactive visualization to {OUT}")


if __name__ == "__main__":
    main()
