from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "last_laba.ipynb"

META = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "pygments_lexer": "ipython3",
    },
}


def md(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


cells = [
    md(
        r"""
        # last_laba: геодезические на катеноиде

        В этой лабораторной рассматривается **катеноид**:

        $$
        r(u,v)=\bigl(a\cosh u\cos v,\ a\cosh u\sin v,\ au\bigr).
        $$

        Катеноид является поверхностью вращения вокруг оси \(Oz\), поэтому
        геодезические удобно исследовать напрямую через **теорему Клеро**:

        $$
        \rho\cos\varphi=C,
        $$

        где \(\rho\) - расстояние от точки до оси вращения, а \(\varphi\) -
        угол между геодезической и параллелью.

        Для катеноида

        $$
        \rho(u)=a\cosh u.
        $$

        Поэтому

        $$
        a\cosh u\cos\varphi=C.
        $$

        Так как \(\rho_{\min}=a\), все типы геодезических определяются
        сравнением \(c=|C|\) с \(a\).
        """
    ),
    md(
        r"""
        ## 1. Метрика катеноида

        Найдем производные:

        $$
        r_u=(a\sinh u\cos v,\ a\sinh u\sin v,\ a),
        $$

        $$
        r_v=(-a\cosh u\sin v,\ a\cosh u\cos v,\ 0).
        $$

        Тогда

        $$
        (r_u,r_u)=a^2\cosh^2u,\qquad (r_u,r_v)=0,\qquad
        (r_v,r_v)=a^2\cosh^2u.
        $$

        Значит, первая квадратичная форма:

        $$
        ds^2=a^2\cosh^2u(du^2+dv^2).
        $$
        """
    ),
    md(
        r"""
        ## 2. Формула геодезической из теоремы Клеро

        Выберем натуральный параметр \(s\), то есть \(|\gamma'(s)|=1\).
        Тогда из метрики:

        $$
        1=a^2\cosh^2u(\dot u^2+\dot v^2).
        $$

        Теорема Клеро дает:

        $$
        C=\rho\cos\varphi.
        $$

        Для натурального параметра

        $$
        C=\rho^2\dot v=a^2\cosh^2u\,\dot v.
        $$

        Отсюда

        $$
        \dot v=\frac{C}{a^2\cosh^2u}.
        $$

        Подставляя в условие единичной скорости, получаем:

        $$
        \dot u^2=
        \frac{a^2\cosh^2u-C^2}{a^4\cosh^4u}.
        $$

        Поэтому

        $$
        \frac{dv}{du}
        =
        \pm
        \frac{C}{\sqrt{a^2\cosh^2u-C^2}}.
        $$

        То есть геодезические строятся по формуле

        $$
        v(u)=v_0\pm
        \int
        \frac{C\,du}{\sqrt{a^2\cosh^2u-C^2}}.
        $$
        """
    ),
    md(
        r"""
        ## 3. Все типы геодезических

        Поскольку \(\rho(u)=a\cosh u\ge a\), сравниваем \(c=|C|\) с \(a\).

        1. \(c=0\): меридианы \(v=\mathrm{const}\).
        2. \(0<c<a\): сквозные спирали, проходящие через горловину.
        3. \(c=a,\ u=0\): сама горловина катеноида.
        4. \(c=a,\ u\ne0\): спирали, асимптотически наматывающиеся на горловину.
        5. \(c>a\): геодезические отражаются от запрещенной зоны \(\rho<c\).

        Это не пять отдельных линий, а пять качественно разных классов поведения.
        В каждом классе бесконечно много геодезических.
        """
    ),
    code(
        r"""
        import numpy as np
        import plotly.graph_objects as go
        from scipy.integrate import cumulative_trapezoid

        A = 1.0
        U_MAX = 2.35


        def rho(u, a=A):
            return a * np.cosh(u)


        def catenoid_xyz(u, v, a=A):
            radius = rho(u, a)
            return radius * np.cos(v), radius * np.sin(v), a * u


        def cumulative_v(u, clairaut_c, sign=1.0):
            denominator = np.sqrt(np.maximum(rho(u) ** 2 - clairaut_c**2, 1e-14))
            dv_du = sign * clairaut_c / denominator
            return cumulative_trapezoid(dv_du, u, initial=0.0)


        def meridian(v0, n=600, u_limit=U_MAX):
            u = np.linspace(-u_limit, u_limit, n)
            return u, np.full_like(u, v0)


        def through_spiral(clairaut_c, n=1500, u_limit=U_MAX):
            u = np.linspace(-u_limit, u_limit, n)
            v = cumulative_v(u, clairaut_c, sign=1.0)
            return u, v - 0.5 * v[-1]


        def neck_circle(n=720):
            v = np.linspace(0.0, 2.0 * np.pi, n)
            return np.zeros_like(v), v


        def asymptotic_spiral(upper=True, n=1600, eps=3e-5, u_limit=U_MAX):
            if upper:
                u = np.linspace(u_limit, eps, n)
                v = cumulative_v(u, A, sign=-1.0)
            else:
                u = np.linspace(-u_limit, -eps, n)
                v = cumulative_v(u, A, sign=1.0)
            return u, v - 0.5 * v[-1]


        def reflecting_spiral(clairaut_c, upper=True, n=1200, eps=2e-4, u_limit=U_MAX):
            u_turn = np.arccosh(clairaut_c / A)
            if upper:
                incoming = np.linspace(u_limit, u_turn + eps, n)
                outgoing = np.linspace(u_turn + eps, u_limit, n)
            else:
                incoming = np.linspace(-u_limit, -u_turn - eps, n)
                outgoing = np.linspace(-u_turn - eps, -u_limit, n)

            v_in = cumulative_v(incoming, clairaut_c, sign=-1.0 if upper else 1.0)
            v_out = v_in[-1] + cumulative_v(
                outgoing,
                clairaut_c,
                sign=1.0 if upper else -1.0,
            )
            u = np.concatenate([incoming, outgoing[1:]])
            v = np.concatenate([v_in, v_out[1:]])
            return u, v - 0.5 * v[-1]


        def add_curve(fig, u, v, name, color, width=7, showlegend=True):
            x, y, z = catenoid_xyz(u, v)
            fig.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="lines",
                    name=name,
                    showlegend=showlegend,
                    line={"color": color, "width": width},
                )
            )


        def build_surface():
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
            )
        """
    ),
    code(
        r"""
        fig = go.Figure(data=[build_surface()])

        for index, v0 in enumerate([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0]):
            add_curve(
                fig,
                *meridian(v0),
                "1. C=0: меридианы",
                "#1f2a7c",
                width=8,
                showlegend=index == 0,
            )

        add_curve(
            fig,
            *through_spiral(0.55 * A),
            "2. 0<C<a: сквозная спираль",
            "#ef6c00",
            width=8,
        )

        add_curve(
            fig,
            *neck_circle(),
            "3. C=a: горловина",
            "#c62828",
            width=9,
        )

        for index, upper in enumerate([True, False]):
            add_curve(
                fig,
                *asymptotic_spiral(upper=upper),
                "4. C=a: асимптотика к горловине",
                "#6a1b9a",
                width=8,
                showlegend=index == 0,
            )

        reflect_c = 1.65 * A
        for index, upper in enumerate([True, False]):
            add_curve(
                fig,
                *reflecting_spiral(reflect_c, upper=upper),
                "5. C>a: отражение от запрещенной зоны",
                "#2e7d32",
                width=8,
                showlegend=index == 0,
            )

        fig.update_layout(
            title={
                "text": "Геодезические на катеноиде: пять типов по теореме Клеро",
                "x": 0.5,
                "xanchor": "center",
            },
            legend={
                "x": 0.02,
                "y": 0.98,
                "bgcolor": "rgba(255,255,255,0.8)",
                "bordercolor": "rgba(35,57,93,0.18)",
                "borderwidth": 1,
            },
            scene={
                "xaxis_title": "x",
                "yaxis_title": "y",
                "zaxis_title": "z",
                "aspectmode": "data",
                "camera": {"eye": {"x": 1.55, "y": -1.95, "z": 1.05}},
            },
            margin={"l": 0, "r": 0, "t": 60, "b": 0},
            template="plotly_white",
        )

        fig.show()
        """
    ),
    md(
        r"""
        ## 4. Анимация построения геодезических

        Ниже те же типы геодезических постепенно отрисовываются на катеноиде.
        Это именно анимация построения: сначала видна поверхность, потом кривые
        появляются по частям.
        """
    ),
    code(
        r"""
        def curve_xyz(u, v):
            x, y, z = catenoid_xyz(u, v)
            return np.asarray(x), np.asarray(y), np.asarray(z)


        animation_curves = []

        for index, v0 in enumerate([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0]):
            u, v = meridian(v0, n=900)
            animation_curves.append(
                {
                    "name": "1. C=0: меридианы" if index == 0 else "меридиан",
                    "color": "#1f2a7c",
                    "width": 7,
                    "showlegend": index == 0,
                    "xyz": curve_xyz(u, v),
                }
            )

        u, v = through_spiral(0.55 * A, n=1200)
        animation_curves.append(
            {
                "name": "2. 0<C<a: сквозная спираль",
                "color": "#ef6c00",
                "width": 7,
                "showlegend": True,
                "xyz": curve_xyz(u, v),
            }
        )

        u, v = neck_circle(n=900)
        animation_curves.append(
            {
                "name": "3. C=a: горловина",
                "color": "#c62828",
                "width": 8,
                "showlegend": True,
                "xyz": curve_xyz(u, v),
            }
        )

        for index, upper in enumerate([True, False]):
            u, v = asymptotic_spiral(upper=upper, n=1200)
            animation_curves.append(
                {
                    "name": "4. C=a: асимптотика к горловине" if index == 0 else "асимптотика",
                    "color": "#6a1b9a",
                    "width": 7,
                    "showlegend": index == 0,
                    "xyz": curve_xyz(u, v),
                }
            )

        reflect_c = 1.65 * A
        for index, upper in enumerate([True, False]):
            u, v = reflecting_spiral(reflect_c, upper=upper, n=1000)
            animation_curves.append(
                {
                    "name": "5. C>a: отражение от запрещенной зоны" if index == 0 else "отражение",
                    "color": "#2e7d32",
                    "width": 7,
                    "showlegend": index == 0,
                    "xyz": curve_xyz(u, v),
                }
            )

        anim_fig = go.Figure(data=[build_surface()])

        for curve in animation_curves:
            x, y, z = curve["xyz"]
            anim_fig.add_trace(
                go.Scatter3d(
                    x=x[:2],
                    y=y[:2],
                    z=z[:2],
                    mode="lines",
                    name=curve["name"],
                    showlegend=curve["showlegend"],
                    line={"color": curve["color"], "width": curve["width"]},
                )
            )

        frame_count = 85
        frames = []
        animated_trace_indices = list(range(1, len(animation_curves) + 1))

        for frame_index in range(frame_count):
            fraction = (frame_index + 1) / frame_count
            frame_data = []
            for curve in animation_curves:
                x, y, z = curve["xyz"]
                point_count = max(2, int(fraction * len(x)))
                frame_data.append(
                    go.Scatter3d(
                        x=x[:point_count],
                        y=y[:point_count],
                        z=z[:point_count],
                        mode="lines",
                        line={"color": curve["color"], "width": curve["width"]},
                    )
                )
            frames.append(
                go.Frame(
                    data=frame_data,
                    traces=animated_trace_indices,
                    name=str(frame_index),
                )
            )

        anim_fig.frames = frames

        slider_steps = [
            {
                "args": [
                    [str(i)],
                    {
                        "frame": {"duration": 0, "redraw": True},
                        "mode": "immediate",
                        "transition": {"duration": 0},
                    },
                ],
                "label": str(i + 1),
                "method": "animate",
            }
            for i in range(frame_count)
        ]

        anim_fig.update_layout(
            title={
                "text": "Анимация построения геодезических на катеноиде",
                "x": 0.5,
                "xanchor": "center",
            },
            legend={
                "x": 0.02,
                "y": 0.98,
                "bgcolor": "rgba(255,255,255,0.8)",
                "bordercolor": "rgba(35,57,93,0.18)",
                "borderwidth": 1,
            },
            scene={
                "xaxis_title": "x",
                "yaxis_title": "y",
                "zaxis_title": "z",
                "aspectmode": "data",
                "camera": {"eye": {"x": 1.55, "y": -1.95, "z": 1.05}},
            },
            margin={"l": 0, "r": 0, "t": 60, "b": 0},
            template="plotly_white",
            updatemenus=[
                {
                    "type": "buttons",
                    "direction": "left",
                    "x": 0.5,
                    "y": 1.08,
                    "xanchor": "center",
                    "yanchor": "top",
                    "buttons": [
                        {
                            "label": "Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 55, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                        {
                            "label": "Pause",
                            "method": "animate",
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                    ],
                }
            ],
            sliders=[
                {
                    "active": 0,
                    "currentvalue": {"prefix": "Кадр: "},
                    "pad": {"t": 40},
                    "steps": slider_steps,
                }
            ],
        )

        anim_fig.show()
        """
    ),
    md(
        r"""
        ## 5. Главное для защиты

        На графике показаны не пять отдельных геодезических, а пять типов:

        - \(C=0\) - меридианы;
        - \(0<C<a\) - сквозные спирали;
        - \(C=a\) - горловина;
        - \(C=a\) - асимптотическое наматывание на горловину;
        - \(C>a\) - отражение от области, где \(\rho<C\).

        Эти случаи возникают потому, что теорема Клеро требует

        $$
        |C|\le \rho(u)=a\cosh u,
        $$

        а минимальное значение \(\rho\) равно \(a\).
        """
    ),
]


nb = nbf.v4.new_notebook(cells=cells, metadata=META)
OUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, OUT)
print(f"Generated {OUT}")
