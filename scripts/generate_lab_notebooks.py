from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


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

TASK_NOTEBOOK_MARKDOWN = {
    "lab_01_2_3_cassini.ipynb": r"""
    # Лабораторная 1. Задача 2.3

    **Постановка задачи.** Написать уравнение плоской фигуры, состоящей из
    всех точек, произведение расстояний которых до двух данных точек \(F_1\)
    и \(F_2\), где \(|F_1F_2|=2b\), постоянно и равно \(a^2\)
    (овалы Кассини).
    """,
    "lab_02_2_7_2_9_2_12_curves.ipynb": r"""
    # Лабораторная 2. Задачи 2.7, 2.9, 2.12

    **2.7.** Отрезок \(AB\) постоянной длины \(2a\) скользит концами \(A\)
    и \(B\) по осям прямоугольной системы координат. Из начала координат
    на \(AB\) опущен перпендикуляр \(OM\). Составить уравнение фигуры,
    образованной точками \(M\) (четырехлепестковая роза).

    **2.9.** Отрезок постоянной длины \(b\) скользит концами \(A\) и \(B\)
    по осям прямоугольной системы координат. Точка \(M\) делит отрезок
    \(AB\) в отношении \(\lambda\). Написать неявное уравнение ее
    траектории.

    **2.12.** Найти кривую, образом которой является пересечение сферы
    радиуса \(R\) и кругового цилиндра диаметра \(R\), одна из образующих
    которого проходит через центр сферы (кривая Вивиани).
    """,
    "lab_03_4_8_4_13_frenet.ipynb": r"""
    # Лабораторная 3. Задачи 4.8 и 4.13

    **4.8.** Найти координаты векторов репера Френе \((T,N,B)\) для
    заданных пространственных кривых в указанных точках:
    \(r(t)=(t,\frac12t^2,\frac13t^3)\) при \(t=1\);
    \(r(t)=(t\sin t,t\cos t,te^t)\) в начале координат;
    \(r(t)=(a\cos t,a\sin t,bt)\) в произвольной точке;
    \(r(t)=(a(t-\sin t),a(1-\cos t),4a\cos\frac t2)\) в произвольной точке.

    **4.13.** На бинормалях винтовой линии
    \((a\cos t,a\sin t,bt)\) отложены отрезки равной длины. Доказать, что
    концы этих отрезков лежат на другой винтовой линии.
    """,
    "lab_04_5_2_5_8_surfaces_tangent.ipynb": r"""
    # Лабораторная 4. Задачи 5.2 и 5.8

    **5.2.** Составить параметрические уравнения поверхностей вращения:
    катеноида, полученного вращением цепной линии вокруг оси \(Oz\);
    псевдосферы, полученной вращением трактрисы вокруг оси \(Oz\).

    **5.8.** Составить уравнение касательной плоскости и нормали к
    поверхностям в указанных точках: пункты **б**, **г**, **и**.
    """,
    "lab_05_6_2_6_8_6_11_6_12_metric.ipynb": r"""
    # Лабораторная 5. Задачи 6.2, 6.8, 6.11, 6.12

    **6.2.** Найти первую квадратичную форму заданных поверхностей.

    **6.8.** Найти ортогональные траектории семейства линий
    \(u+v=\mathrm{const}\), лежащих на сфере.

    **6.11.** Для первой квадратичной формы
    \(ds^2=du^2+(u^2+a^2)dv^2\) найти периметр, углы и площадь указанных
    криволинейных треугольников.

    **6.12.** Для поверхности \(r(u,v)=(u\sin v,u\cos v,v)\) найти площадь,
    длины сторон и углы криволинейного треугольника
    \(0\le u\le\sinh v,\ 0\le v\le v_0\).
    """,
    "lab_06_6_16_angle_bisectors.ipynb": r"""
    # Лабораторная 6. Задача 6.16

    **Постановка задачи.** Дана первая квадратичная форма поверхности.
    Найти уравнения линий, которые в каждой своей точке делят пополам углы
    между координатными линиями поверхности, для пунктов **а**, **б**,
    **в**, **г**.
    """,
    "lab_07_7_18_dupin.ipynb": r"""
    # Лабораторная 7. Задача 7.18

    **Постановка задачи.** Найти уравнение индикатрисы Дюпена для данной
    поверхности в указанной точке: сфера, цилиндр, параболоид
    \(z=2x^2+\frac92y^2\) в начале координат и поверхность
    \(r(u,v)=(\cosh u\cos v,\cosh u\sin v,u)\).
    """,
}


def md(text: str):
    return nbf.v4.new_markdown_cell(normalize_math_delimiters(dedent(text).strip()))


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip())


def normalize_math_delimiters(text: str) -> str:
    return (
        text
        .replace(r"\[", "$$")
        .replace(r"\]", "$$")
        .replace(r"\(", "$")
        .replace(r"\)", "$")
    )


def write_notebook(name: str, cells: list):
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook(cells=cells, metadata=META)
    path = NOTEBOOKS / name
    nbf.write(nb, path)
    print(path.relative_to(ROOT).as_posix())


def separate_analytical_solutions():
    chunks = [
        "# Аналитические решения лабораторных работ",
        "В ноутбуках оставлены постановки задач и динамические визуализации. "
        "Подробные выкладки собраны здесь, чтобы их было удобно переписать отдельно.",
    ]

    for name, task_text in TASK_NOTEBOOK_MARKDOWN.items():
        path = NOTEBOOKS / name
        nb = nbf.read(path, as_version=4)
        markdown_cells = [
            normalize_math_delimiters(cell.source.strip())
            for cell in nb.cells
            if cell.cell_type == "markdown"
        ]
        code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]

        chunks.append("\n---\n")
        chunks.extend(markdown_cells)

        stripped = nbf.v4.new_notebook(metadata=META)
        stripped.cells = [md(task_text)]
        stripped.cells.extend(nbf.v4.new_code_cell(cell.source) for cell in code_cells)
        nbf.write(stripped, path)

    (NOTEBOOKS / "analytical_solutions.md").write_text(
        normalize_math_delimiters("\n\n".join(chunks).strip()) + "\n",
        encoding="utf-8",
    )


COMMON_2D = r"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

plt.rcParams["figure.figsize"] = (7, 6)
plt.rcParams["axes.grid"] = True
plt.rcParams["animation.embed_limit"] = 80


def finish_animation(anim, fig):
    html = HTML(anim.to_jshtml())
    plt.close(fig)
    return html


def setup_2d(ax, xlim, ylim, title):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="0.35", linewidth=1)
    ax.axvline(0, color="0.35", linewidth=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
"""


COMMON_3D = r"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

plt.rcParams["figure.figsize"] = (8, 6)
plt.rcParams["animation.embed_limit"] = 100


def finish_animation(anim, fig):
    html = HTML(anim.to_jshtml())
    plt.close(fig)
    return html


def set_axes_equal_3d(ax):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])
    radius = 0.5 * max([x_range, y_range, z_range])
    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)
    ax.set_xlim3d([x_middle - radius, x_middle + radius])
    ax.set_ylim3d([y_middle - radius, y_middle + radius])
    ax.set_zlim3d([z_middle - radius, z_middle + radius])


def setup_3d(ax, xlim, ylim, zlim, title):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(title)
"""


def lab_01():
    write_notebook(
        "lab_01_2_3_cassini.ipynb",
        [
            md(r"""
            # Лабораторная 1. Задача 2.3: овалы Кассини

            **Условие.** Написать уравнение плоской фигуры, состоящей из всех точек,
            произведение расстояний которых до двух данных точек \(F_1\) и \(F_2\),
            где \(|F_1F_2|=2b\), постоянно и равно \(a^2\).
            """),
            md(r"""
            ## Аналитическое решение

            Выберем систему координат так, чтобы начало координат было серединой
            отрезка \(F_1F_2\), а ось \(Ox\) проходила через фокусы:

            \[
            F_1=(-b,0),\qquad F_2=(b,0).
            \]

            Для произвольной точки \(M=(x,y)\)

            \[
            MF_1=\sqrt{(x+b)^2+y^2},\qquad
            MF_2=\sqrt{(x-b)^2+y^2}.
            \]

            По условию \(MF_1\cdot MF_2=a^2\). Возводим в квадрат:

            \[
            \bigl((x+b)^2+y^2\bigr)\bigl((x-b)^2+y^2\bigr)=a^4.
            \]

            Раскроем произведение:

            \[
            \bigl(x^2+y^2+b^2+2bx\bigr)
            \bigl(x^2+y^2+b^2-2bx\bigr)=a^4.
            \]

            Используем формулу \((A+B)(A-B)=A^2-B^2\):

            \[
            \boxed{(x^2+y^2+b^2)^2-4b^2x^2=a^4.}
            \]

            Это и есть уравнение овалов Кассини.

            В полярных координатах \(x=\rho\cos\varphi,\ y=\rho\sin\varphi\):

            \[
            \boxed{\rho^4-2b^2\rho^2\cos 2\varphi+b^4=a^4.}
            \]

            При разных отношениях \(a/b\) форма меняется: при \(a<b\) две петли,
            при \(a=b\) лемниската Бернулли, при \(a>b\) один замкнутый овал.
            """),
            code(COMMON_2D),
            code(r"""
            b = 1.0
            frames = 80
            a_values = np.linspace(0.55 * b, 1.85 * b, frames)
            xs = np.linspace(-2.5, 2.5, 420)
            ys = np.linspace(-2.0, 2.0, 360)
            X, Y = np.meshgrid(xs, ys)


            def cassini_F(X, Y, a, b):
                return (X**2 + Y**2 + b**2)**2 - 4 * b**2 * X**2 - a**4


            fig, ax = plt.subplots(figsize=(7, 5.5))


            def animate(i):
                ax.clear()
                a = a_values[i]
                setup_2d(ax, (-2.5, 2.5), (-2.0, 2.0), f"Овалы Кассини: a/b = {a / b:.2f}")
                ax.scatter([-b, b], [0, 0], color="crimson", zorder=5)
                ax.text(-b, 0.08, "$F_1$", ha="center")
                ax.text(b, 0.08, "$F_2$", ha="center")
                ax.contour(X, Y, cassini_F(X, Y, a, b), levels=[0], colors=["navy"], linewidths=2)
                ax.text(-2.42, 1.72, r"$(x^2+y^2+b^2)^2-4b^2x^2=a^4$", fontsize=10)
                return []


            anim = FuncAnimation(fig, animate, frames=frames, interval=90)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_02():
    write_notebook(
        "lab_02_2_7_2_9_2_12_curves.ipynb",
        [
            md(r"""
            # Лабораторная 2. Задачи 2.7, 2.9, 2.12

            В этой работе рассматриваются траектории, которые удобно получать
            через параметр движения: скользящий отрезок и пересечение сферы с
            цилиндром.
            """),
            code(COMMON_2D),
            md(r"""
            ## Задача 2.7: четырехлепестковая роза

            Отрезок \(AB\) постоянной длины \(2a\) скользит концами по осям
            координат. Из начала координат на \(AB\) опущен перпендикуляр \(OM\).
            Найти уравнение траектории точки \(M\).
            """),
            md(r"""
            ### Решение

            Пусть

            \[
            A=(2a\cos t,0),\qquad B=(0,2a\sin t).
            \]

            Тогда \(|AB|=2a\), потому что

            \[
            |AB|^2=(2a\cos t)^2+(2a\sin t)^2=4a^2.
            \]

            Уравнение прямой \(AB\):

            \[
            \frac{x}{2a\cos t}+\frac{y}{2a\sin t}=1,
            \]

            или

            \[
            x\sin t+y\cos t=2a\sin t\cos t.
            \]

            Вектор нормали к этой прямой равен \((\sin t,\cos t)\). Поэтому
            основание перпендикуляра из начала координат:

            \[
            M=2a\sin t\cos t(\sin t,\cos t).
            \]

            Значит,

            \[
            x=2a\sin^2t\cos t,\qquad
            y=2a\sin t\cos^2t.
            \]

            Для расстояния \(\rho=OM\) получаем

            \[
            \rho=2a|\sin t\cos t|=a|\sin 2t|.
            \]

            Если перейти к полярному углу \(\varphi\), то получается роза

            \[
            \boxed{\rho=a\sin 2\varphi.}
            \]

            Неявное уравнение:

            \[
            \boxed{(x^2+y^2)^3=4a^2x^2y^2.}
            \]
            """),
            code(r"""
            a = 2.0
            frames = 120


            def segment_endpoints(t, a=a):
                return np.array([2 * a * np.cos(t), 0.0]), np.array([0.0, 2 * a * np.sin(t)])


            def foot_from_origin(A, B):
                AB = B - A
                s = -np.dot(A, AB) / np.dot(AB, AB)
                return A + s * AB


            ts = np.linspace(0.02, 2 * np.pi - 0.02, 1200)
            rose = np.array([foot_from_origin(*segment_endpoints(t)) for t in ts])

            fig, ax = plt.subplots(figsize=(6, 6))


            def animate(i):
                ax.clear()
                setup_2d(ax, (-4.5, 4.5), (-4.5, 4.5), "2.7: скользящий отрезок и точка M")
                t = 0.02 + (2 * np.pi - 0.04) * i / (frames - 1)
                A, B = segment_endpoints(t)
                M = foot_from_origin(A, B)
                ax.plot(rose[:, 0], rose[:, 1], color="navy", linewidth=1.8, label="траектория M")
                ax.plot([A[0], B[0]], [A[1], B[1]], color="darkorange", marker="o", label="AB")
                ax.plot([0, M[0]], [0, M[1]], color="crimson", marker="o", label="OM")
                ax.scatter([0], [0], color="black", s=25)
                ax.text(A[0], A[1], " A")
                ax.text(B[0], B[1], " B")
                ax.text(M[0], M[1], " M")
                ax.legend(loc="upper right")
                return []


            anim = FuncAnimation(fig, animate, frames=frames, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 2.9: точка делит скользящий отрезок

            Отрезок \(AB\) длины \(b\) скользит концами по осям. Точка \(M\)
            делит \(AB\) в отношении \(\lambda:1\), то есть
            \(AM:MB=\lambda:1\). Нужно найти неявное уравнение траектории.
            """),
            md(r"""
            ### Решение

            Возьмем

            \[
            A=(b\cos t,0),\qquad B=(0,b\sin t).
            \]

            Если \(AM:MB=\lambda:1\), то по формуле деления отрезка

            \[
            M=\frac{A+\lambda B}{1+\lambda}.
            \]

            Поэтому

            \[
            x=\frac{b}{1+\lambda}\cos t,\qquad
            y=\frac{\lambda b}{1+\lambda}\sin t.
            \]

            Исключаем параметр \(t\):

            \[
            \cos t=\frac{(1+\lambda)x}{b},\qquad
            \sin t=\frac{(1+\lambda)y}{\lambda b}.
            \]

            Так как \(\cos^2t+\sin^2t=1\), получаем эллипс:

            \[
            \boxed{
            \frac{x^2}{\left(\frac{b}{1+\lambda}\right)^2}
            +
            \frac{y^2}{\left(\frac{\lambda b}{1+\lambda}\right)^2}=1.
            }
            \]
            """),
            code(r"""
            b = 4.0
            lam = 2.0
            frames = 120


            def sliding_segment(t, b=b):
                return np.array([b * np.cos(t), 0.0]), np.array([0.0, b * np.sin(t)])


            def divided_point(A, B, lam=lam):
                return (A + lam * B) / (1 + lam)


            ts = np.linspace(0, 2 * np.pi, 900)
            trace = np.array([divided_point(*sliding_segment(t)) for t in ts])

            fig, ax = plt.subplots(figsize=(6, 6))


            def animate(i):
                ax.clear()
                setup_2d(ax, (-4.5, 4.5), (-4.5, 4.5), "2.9: траектория точки M")
                t = 2 * np.pi * i / (frames - 1)
                A, B = sliding_segment(t)
                M = divided_point(A, B)
                ax.plot(trace[:, 0], trace[:, 1], color="navy", linewidth=2, label="эллипс")
                ax.plot([A[0], B[0]], [A[1], B[1]], color="darkorange", marker="o", label="AB")
                ax.scatter([M[0]], [M[1]], color="crimson", zorder=5, label="M")
                ax.text(M[0], M[1], " M")
                ax.legend(loc="upper right")
                return []


            anim = FuncAnimation(fig, animate, frames=frames, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 2.12: кривая Вивиани

            Нужно найти кривую пересечения сферы радиуса \(R\) и кругового
            цилиндра диаметра \(R\), одна образующая которого проходит через
            центр сферы.
            """),
            md(r"""
            ### Решение

            Пусть сфера имеет центр в начале координат:

            \[
            x^2+y^2+z^2=R^2.
            \]

            Возьмем цилиндр радиуса \(R/2\) с осью, параллельной \(Oz\), так что
            одна его образующая проходит через начало координат:

            \[
            \left(x-\frac R2\right)^2+y^2=\left(\frac R2\right)^2.
            \]

            После раскрытия скобок:

            \[
            x^2+y^2=Rx.
            \]

            Удобная параметризация цилиндра:

            \[
            x=R\cos^2t,\qquad y=R\sin t\cos t.
            \]

            Тогда

            \[
            x^2+y^2=R^2\cos^2t.
            \]

            Из уравнения сферы:

            \[
            z^2=R^2-R^2\cos^2t=R^2\sin^2t.
            \]

            Берем \(z=R\sin t\). Получаем кривую Вивиани:

            \[
            \boxed{
            r(t)=\bigl(R\cos^2t,\ R\sin t\cos t,\ R\sin t\bigr),
            \qquad 0\le t\le 2\pi.
            }
            \]
            """),
            code(COMMON_3D),
            code(r"""
            R = 2.0


            def viviani(t, R=R):
                return np.vstack([
                    R * np.cos(t) ** 2,
                    R * np.sin(t) * np.cos(t),
                    R * np.sin(t),
                ])


            u = np.linspace(-np.pi / 2, np.pi / 2, 45)
            v = np.linspace(0, 2 * np.pi, 70)
            U, V = np.meshgrid(u, v)
            Xs = R * np.cos(U) * np.cos(V)
            Ys = R * np.cos(U) * np.sin(V)
            Zs = R * np.sin(U)

            theta = np.linspace(0, 2 * np.pi, 60)
            z = np.linspace(-R, R, 35)
            Th, Zc = np.meshgrid(theta, z)
            Xc = R / 2 + (R / 2) * np.cos(Th)
            Yc = (R / 2) * np.sin(Th)

            tt = np.linspace(0, 2 * np.pi, 500)
            curve = viviani(tt)

            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            setup_3d(ax, (-2.2, 2.2), (-2.2, 2.2), (-2.2, 2.2), "2.12: кривая Вивиани")
            ax.plot_surface(Xs, Ys, Zs, alpha=0.18, linewidth=0, color="steelblue")
            ax.plot_surface(Xc, Yc, Zc, alpha=0.18, linewidth=0, color="darkorange")
            ax.plot(curve[0], curve[1], curve[2], color="navy", linewidth=2)
            point, = ax.plot([], [], [], "o", color="crimson", markersize=7)
            trace, = ax.plot([], [], [], color="crimson", linewidth=2)
            set_axes_equal_3d(ax)


            def animate(i):
                k = max(2, int((i + 1) / 100 * curve.shape[1]))
                point.set_data([curve[0, k - 1]], [curve[1, k - 1]])
                point.set_3d_properties([curve[2, k - 1]])
                trace.set_data(curve[0, :k], curve[1, :k])
                trace.set_3d_properties(curve[2, :k])
                ax.view_init(elev=24, azim=35 + 1.4 * i)
                return point, trace


            anim = FuncAnimation(fig, animate, frames=100, interval=70)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_03():
    write_notebook(
        "lab_03_4_8_4_13_frenet.ipynb",
        [
            md(r"""
            # Лабораторная 3. Задачи 4.8 и 4.13

            Здесь используются касательный вектор \(T\), главная нормаль \(N\)
            и бинормаль \(B=T\times N\).
            """),
            md(r"""
            ## Общая формула репера Френе

            Для регулярной пространственной кривой \(r(t)\):

            \[
            T=\frac{r'}{|r'|}.
            \]

            Главную нормаль удобно находить через часть ускорения, перпендикулярную
            касательной:

            \[
            A_\perp=r''-(r'',T)T,\qquad
            N=\frac{A_\perp}{|A_\perp|}.
            \]

            После этого

            \[
            B=T\times N.
            \]
            """),
            md(r"""
            ## Задача 4.8: координаты векторов репера Френе

            ### а) \(r(t)=\left(t,\frac12t^2,\frac13t^3\right)\), \(t=1\)

            \[
            r'=(1,t,t^2),\qquad r''=(0,1,2t).
            \]

            При \(t=1\):

            \[
            r'=(1,1,1),\qquad |r'|=\sqrt3,
            \]

            поэтому

            \[
            \boxed{T=\frac1{\sqrt3}(1,1,1).}
            \]

            \[
            r''=(0,1,2),\qquad (r'',T)=\sqrt3.
            \]

            \[
            A_\perp=(0,1,2)-(1,1,1)=(-1,0,1).
            \]

            \[
            \boxed{N=\frac1{\sqrt2}(-1,0,1),\qquad
            B=\frac1{\sqrt6}(1,-2,1).}
            \]

            ### б) \(r(t)=(t\sin t,\ t\cos t,\ te^t)\), \(t=0\)

            Точка \(t=0\) действительно является началом координат.

            \[
            r'(0)=(0,1,1),\qquad r''(0)=(2,0,2).
            \]

            \[
            \boxed{T=\frac1{\sqrt2}(0,1,1).}
            \]

            \[
            (r'',T)=\sqrt2,\qquad
            A_\perp=(2,0,2)-(0,1,1)=(2,-1,1).
            \]

            \[
            \boxed{N=\frac1{\sqrt6}(2,-1,1),\qquad
            B=\frac1{\sqrt3}(1,1,-1).}
            \]

            ### в) \(r(t)=(a\cos t,\ a\sin t,\ bt)\)

            Обозначим \(c=\sqrt{a^2+b^2}\). Тогда

            \[
            \boxed{T=\frac1c(-a\sin t,\ a\cos t,\ b),}
            \]

            \[
            \boxed{N=(-\cos t,-\sin t,0),}
            \]

            \[
            \boxed{B=\frac1c(b\sin t,\ -b\cos t,\ a).}
            \]

            ### г) \(r(t)=\left(a(t-\sin t),\ a(1-\cos t),\ 4a\cos\frac t2\right)\)

            Положим \(q=t/2\) и рассматриваем регулярные точки, где
            \(\sin q\ne0\). Для участка \(0<t<2\pi\):

            \[
            r'=2a\sin q(\sin q,\cos q,-1),
            \]

            поэтому

            \[
            \boxed{T=\frac1{\sqrt2}(\sin q,\cos q,-1).}
            \]

            Дифференцируя \(T\), получаем направление главной нормали:

            \[
            \boxed{N=(\cos q,-\sin q,0).}
            \]

            Тогда

            \[
            \boxed{B=\frac1{\sqrt2}(-\sin q,-\cos q,-1).}
            \]
            """),
            code(COMMON_3D),
            code(r"""
            EPS = 1e-9


            def normalize(v):
                v = np.asarray(v, dtype=float)
                n = np.linalg.norm(v)
                if n < EPS:
                    raise ValueError("Нулевой вектор нельзя нормировать")
                return v / n


            def d_curve(r, t, h=1e-5):
                return (np.asarray(r(t + h)) - np.asarray(r(t - h))) / (2 * h)


            def dd_curve(r, t, h=1e-4):
                return (np.asarray(r(t + h)) - 2 * np.asarray(r(t)) + np.asarray(r(t - h))) / (h ** 2)


            def frenet_frame(r, t):
                p = np.asarray(r(t), dtype=float)
                r1 = d_curve(r, t)
                r2 = dd_curve(r, t)
                T = normalize(r1)
                A_perp = r2 - np.dot(r2, T) * T
                N = normalize(A_perp)
                B = normalize(np.cross(T, N))
                return p, T, N, B


            a = 1.5
            b = 0.6
            curves = {
                "4.8a": (lambda t: np.array([t, 0.5 * t**2, (1 / 3) * t**3]), 1.0, (-1.0, 2.5)),
                "4.8b": (lambda t: np.array([t * np.sin(t), t * np.cos(t), t * np.exp(t)]), 0.0, (-1.4, 1.0)),
                "4.8c": (lambda t: np.array([a * np.cos(t), a * np.sin(t), b * t]), np.pi / 3, (0.0, 4 * np.pi)),
                "4.8d": (lambda t: np.array([a * (t - np.sin(t)), a * (1 - np.cos(t)), 4 * a * np.cos(t / 2)]), np.pi / 2, (0.05, 2 * np.pi - 0.05)),
            }

            for name, (r, t0, _) in curves.items():
                p, T, N, B = frenet_frame(r, t0)
                print(name)
                print("  точка:", np.round(p, 4))
                print("  T:", np.round(T, 4))
                print("  N:", np.round(N, 4))
                print("  B:", np.round(B, 4))
                print("  скалярные произведения:", round(np.dot(T, N), 8), round(np.dot(T, B), 8), round(np.dot(N, B), 8))
            """),
            code(r"""
            name = "4.8c"
            r, _, t_range = curves[name]
            ts = np.linspace(*t_range, 500)
            pts = np.array([r(t) for t in ts])

            fig = plt.figure(figsize=(7, 6))
            ax = fig.add_subplot(111, projection="3d")


            def animate(i):
                ax.clear()
                setup_3d(ax, (-3, 3), (-3, 3), (-1, 9), f"{name}: движущийся репер Френе")
                ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="navy", linewidth=2)
                t = t_range[0] + (t_range[1] - t_range[0]) * i / 100
                p, T, N, B = frenet_frame(r, t)
                ax.scatter([p[0]], [p[1]], [p[2]], color="crimson", s=35)
                for vec, label, color in [(T, "T", "crimson"), (N, "N", "darkgreen"), (B, "B", "purple")]:
                    q = p + 0.85 * vec
                    ax.quiver(p[0], p[1], p[2], 0.85 * vec[0], 0.85 * vec[1], 0.85 * vec[2],
                              color=color, arrow_length_ratio=0.18)
                    ax.text(q[0], q[1], q[2], label, color=color)
                ax.view_init(elev=24, azim=40 + i)
                set_axes_equal_3d(ax)
                return []


            anim = FuncAnimation(fig, animate, frames=101, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 4.13: отрезки на бинормалях винтовой линии

            Винтовая линия:

            \[
            r(t)=(a\cos t,\ a\sin t,\ bt),\qquad c=\sqrt{a^2+b^2}.
            \]

            Для нее

            \[
            B(t)=\frac1c(b\sin t,\ -b\cos t,\ a).
            \]

            Отложим на бинормали отрезок постоянной длины \(d\):

            \[
            q(t)=r(t)+dB(t).
            \]

            Тогда

            \[
            q(t)=
            \left(
            a\cos t+\frac{db}{c}\sin t,\ 
            a\sin t-\frac{db}{c}\cos t,\ 
            bt+\frac{da}{c}
            \right).
            \]

            Обозначим \(D=\frac{db}{c}\) и
            \(\rho=\sqrt{a^2+D^2}\). Первые две координаты имеют вид

            \[
            x=a\cos t+D\sin t,\qquad
            y=a\sin t-D\cos t.
            \]

            Следовательно,

            \[
            x^2+y^2=a^2+D^2=\rho^2.
            \]

            При этом \(z=bt+\frac{da}{c}\) линейно зависит от того же параметра.
            Значит, точки \(q(t)\) лежат на другой винтовой линии радиуса

            \[
            \boxed{\rho=\sqrt{a^2+\left(\frac{db}{\sqrt{a^2+b^2}}\right)^2}.}
            \]
            """),
            code(r"""
            a = 2.0
            b = 0.8
            d = 0.9
            c = np.sqrt(a**2 + b**2)


            def helix(t):
                return np.array([a * np.cos(t), a * np.sin(t), b * t])


            def binormal(t):
                return np.vstack([b * np.sin(t) / c, -b * np.cos(t) / c, np.full_like(t, a / c)])


            ts = np.linspace(0, 4 * np.pi, 600)
            H = helix(ts)
            Q = H + d * binormal(ts)

            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            setup_3d(ax, (-3.2, 3.2), (-3.2, 3.2), (-0.5, 11), "4.13: концы отрезков на бинормалях")
            ax.plot(H[0], H[1], H[2], color="navy", linewidth=2, label="исходная винтовая линия")
            ax.plot(Q[0], Q[1], Q[2], color="darkorange", linewidth=2, label="новая винтовая линия")
            segment, = ax.plot([], [], [], color="crimson", linewidth=2)
            point_h, = ax.plot([], [], [], "o", color="navy")
            point_q, = ax.plot([], [], [], "o", color="darkorange")
            ax.legend()
            set_axes_equal_3d(ax)


            def animate(i):
                k = int(i / 100 * (len(ts) - 1))
                segment.set_data([H[0, k], Q[0, k]], [H[1, k], Q[1, k]])
                segment.set_3d_properties([H[2, k], Q[2, k]])
                point_h.set_data([H[0, k]], [H[1, k]])
                point_h.set_3d_properties([H[2, k]])
                point_q.set_data([Q[0, k]], [Q[1, k]])
                point_q.set_3d_properties([Q[2, k]])
                ax.view_init(elev=24, azim=35 + i)
                return segment, point_h, point_q


            anim = FuncAnimation(fig, animate, frames=101, interval=70)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_04():
    write_notebook(
        "lab_04_5_2_5_8_surfaces_tangent.ipynb",
        [
            md(r"""
            # Лабораторная 4. Задачи 5.2 и 5.8

            В этой работе строятся поверхности вращения, касательные плоскости
            и нормали.
            """),
            md(r"""
            ## Задача 5.2: поверхности вращения

            ### а) Катеноид

            Цепная линия в плоскости \(y=0\):

            \[
            x=a\cosh\frac ua,\qquad z=u.
            \]

            При вращении вокруг оси \(Oz\) радиус точки равен
            \(a\cosh(u/a)\), а угол вращения обозначим \(v\). Поэтому

            \[
            \boxed{
            r(u,v)=
            \left(
            a\cosh\frac ua\cos v,\ 
            a\cosh\frac ua\sin v,\ 
            u
            \right).
            }
            \]

            ### б) Псевдосфера

            Трактриса:

            \[
            x=a\sin u,\qquad
            z=a\left(\ln\tan\frac u2+\cos u\right).
            \]

            Вращаем вокруг \(Oz\):

            \[
            \boxed{
            r(u,v)=
            \left(
            a\sin u\cos v,\ 
            a\sin u\sin v,\ 
            a\left(\ln\tan\frac u2+\cos u\right)
            \right),
            \quad 0<u<\pi.
            }
            \]
            """),
            code(COMMON_3D),
            code(r"""
            a = 1.0


            def catenoid(u, v):
                radius = a * np.cosh(u / a)
                return radius * np.cos(v), radius * np.sin(v), u


            def pseudosphere(u, v):
                radius = a * np.sin(u)
                z = a * (np.log(np.tan(u / 2)) + np.cos(u))
                return radius * np.cos(v), radius * np.sin(v), z


            u1 = np.linspace(-1.8, 1.8, 70)
            v = np.linspace(0, 2 * np.pi, 90)
            U1, V1 = np.meshgrid(u1, v)
            X1, Y1, Z1 = catenoid(U1, V1)

            u2 = np.linspace(0.18, 2.75, 80)
            U2, V2 = np.meshgrid(u2, v)
            X2, Y2, Z2 = pseudosphere(U2, V2)

            fig = plt.figure(figsize=(12, 5))
            ax1 = fig.add_subplot(121, projection="3d")
            ax2 = fig.add_subplot(122, projection="3d")
            setup_3d(ax1, (-3, 3), (-3, 3), (-2, 2), "5.2а: катеноид")
            setup_3d(ax2, (-1.5, 1.5), (-1.5, 1.5), (-2.8, 1.2), "5.2б: псевдосфера")
            ax1.plot_surface(X1, Y1, Z1, alpha=0.75, linewidth=0, color="steelblue")
            ax2.plot_surface(X2, Y2, Z2, alpha=0.75, linewidth=0, color="darkorange")
            line1, = ax1.plot([], [], [], color="crimson", linewidth=3, label="вращающаяся цепная линия")
            line2, = ax2.plot([], [], [], color="crimson", linewidth=3, label="вращающаяся трактриса")
            trace1 = [None]
            trace2 = [None]
            ax1.legend(loc="upper left")
            ax2.legend(loc="upper left")
            set_axes_equal_3d(ax1)
            set_axes_equal_3d(ax2)


            def animate(i):
                phi = 2 * np.pi * i / 119

                r1 = a * np.cosh(u1 / a)
                line1.set_data(r1 * np.cos(phi), r1 * np.sin(phi))
                line1.set_3d_properties(u1)

                r2 = a * np.sin(u2)
                z2 = a * (np.log(np.tan(u2 / 2)) + np.cos(u2))
                line2.set_data(r2 * np.cos(phi), r2 * np.sin(phi))
                line2.set_3d_properties(z2)

                if trace1[0] is not None:
                    trace1[0].remove()
                if trace2[0] is not None:
                    trace2[0].remove()

                vv = np.linspace(0, phi, max(2, i + 2))
                Ug1, Vg1 = np.meshgrid(u1, vv)
                Tx1, Ty1, Tz1 = catenoid(Ug1, Vg1)
                trace1[0] = ax1.plot_surface(Tx1, Ty1, Tz1, alpha=0.28, linewidth=0, color="crimson")

                Ug2, Vg2 = np.meshgrid(u2, vv)
                Tx2, Ty2, Tz2 = pseudosphere(Ug2, Vg2)
                trace2[0] = ax2.plot_surface(Tx2, Ty2, Tz2, alpha=0.28, linewidth=0, color="crimson")

                ax1.view_init(elev=24, azim=35)
                ax2.view_init(elev=24, azim=35)
                return line1, line2


            anim = FuncAnimation(fig, animate, frames=120, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 5.8: касательные плоскости и нормали

            Общий алгоритм:

            - если поверхность задана параметрически \(r(u,v)\), то
              \[
              N=r_u\times r_v
              \]
              является нормальным вектором;
            - касательная плоскость в точке \(r(u_0,v_0)\):
              \[
              N\cdot\bigl((x,y,z)-r(u_0,v_0)\bigr)=0;
              \]
            - нормаль:
              \[
              (x,y,z)=r(u_0,v_0)+sN.
              \]

            Для неявной поверхности \(F(x,y,z)=0\) нормальный вектор равен
            \(\nabla F\).
            """),
            md(r"""
            ### б) \(r(u,v)=(u+v,\ u^2-2v,\ u^3-uv)\), \(u=1,\ v=2\)

            Точка:

            \[
            r(1,2)=(3,-3,-1).
            \]

            Производные:

            \[
            r_u=(1,2u,3u^2-v),\qquad r_v=(1,-2,-u).
            \]

            В точке:

            \[
            r_u(1,2)=(1,2,1),\qquad r_v(1,2)=(1,-2,-1).
            \]

            \[
            N=r_u\times r_v=(0,2,-4)\sim(0,1,-2).
            \]

            Касательная плоскость:

            \[
            (0,1,-2)\cdot(x-3,\ y+3,\ z+1)=0,
            \]

            то есть

            \[
            \boxed{y-2z+1=0.}
            \]

            Нормаль:

            \[
            \boxed{x=3,\quad y=-3+s,\quad z=-1-2s.}
            \]

            ### г) \(r(u,v)=(au,\ \sin u,\ bv)\), произвольная точка

            \[
            r_u=(a,\cos u,0),\qquad r_v=(0,0,b).
            \]

            \[
            N=r_u\times r_v=(b\cos u,\ -ab,\ 0)\sim(\cos u,-a,0).
            \]

            В точке \(r(u_0,v_0)=(au_0,\sin u_0,bv_0)\):

            \[
            \boxed{
            \cos u_0(x-au_0)-a(y-\sin u_0)=0.
            }
            \]

            Нормаль:

            \[
            \boxed{
            (x,y,z)=(au_0,\sin u_0,bv_0)+s(\cos u_0,-a,0).
            }
            \]

            ### и) \(\frac{x^2}{a^2}+\frac{y^2}{b^2}=2z\), точка \((x_0,y_0,z_0)\)

            Запишем

            \[
            F(x,y,z)=\frac{x^2}{a^2}+\frac{y^2}{b^2}-2z.
            \]

            Тогда

            \[
            \nabla F=
            \left(\frac{2x}{a^2},\frac{2y}{b^2},-2\right)
            \sim
            \left(\frac{x}{a^2},\frac{y}{b^2},-1\right).
            \]

            В точке \((x_0,y_0,z_0)\):

            \[
            \boxed{
            \frac{x_0}{a^2}(x-x_0)+
            \frac{y_0}{b^2}(y-y_0)-
            (z-z_0)=0.
            }
            \]

            Нормаль:

            \[
            \boxed{
            (x,y,z)=(x_0,y_0,z_0)+
            s\left(\frac{x_0}{a^2},\frac{y_0}{b^2},-1\right).
            }
            \]
            """),
            code(r"""
            fig = plt.figure(figsize=(14, 4.8))
            axes = [fig.add_subplot(131, projection="3d"),
                    fig.add_subplot(132, projection="3d"),
                    fig.add_subplot(133, projection="3d")]

            # 5.8б
            u = np.linspace(0.25, 1.7, 45)
            v = np.linspace(1.1, 2.7, 45)
            U, V = np.meshgrid(u, v)
            X = U + V
            Y = U**2 - 2 * V
            Z = U**3 - U * V
            P = np.array([3, -3, -1])
            N = np.array([0, 1, -2], dtype=float)
            xx, zz = np.meshgrid(np.linspace(1.8, 4.2, 8), np.linspace(-2.2, 0.2, 8))
            yy = 2 * zz - 1
            axes[0].plot_surface(X, Y, Z, alpha=0.55, linewidth=0, color="steelblue")
            axes[0].plot_surface(xx, yy, zz, alpha=0.35, color="crimson")
            axes[0].plot([P[0], P[0] + N[0]], [P[1], P[1] + N[1]], [P[2], P[2] + N[2]], color="black", linewidth=2)
            axes[0].scatter(*P, color="black")
            setup_3d(axes[0], (1.5, 4.5), (-5.5, 0.5), (-3, 1), "5.8б")

            # 5.8г
            apar, bpar, u0, v0 = 1.4, 1.1, 0.8, 0.6
            u = np.linspace(-1.8, 1.8, 55)
            v = np.linspace(-1.2, 1.7, 45)
            U, V = np.meshgrid(u, v)
            X = apar * U
            Y = np.sin(U)
            Z = bpar * V
            P = np.array([apar * u0, np.sin(u0), bpar * v0])
            N = np.array([np.cos(u0), -apar, 0.0])
            xx, zz = np.meshgrid(np.linspace(-1, 2.5, 8), np.linspace(-1.4, 2, 8))
            yy = np.sin(u0) + np.cos(u0) / apar * (xx - apar * u0)
            axes[1].plot_surface(X, Y, Z, alpha=0.55, linewidth=0, color="darkorange")
            axes[1].plot_surface(xx, yy, zz, alpha=0.35, color="crimson")
            axes[1].plot([P[0], P[0] + N[0]], [P[1], P[1] + N[1]], [P[2], P[2] + N[2]], color="black", linewidth=2)
            axes[1].scatter(*P, color="black")
            setup_3d(axes[1], (-2.8, 2.8), (-1.8, 1.8), (-1.5, 2), "5.8г")

            # 5.8и
            apar, bpar = 1.5, 1.0
            x0, y0 = 0.8, 0.6
            z0 = 0.5 * (x0**2 / apar**2 + y0**2 / bpar**2)
            x = np.linspace(-1.8, 1.8, 55)
            y = np.linspace(-1.4, 1.4, 55)
            X, Y = np.meshgrid(x, y)
            Z = 0.5 * (X**2 / apar**2 + Y**2 / bpar**2)
            P = np.array([x0, y0, z0])
            N = np.array([x0 / apar**2, y0 / bpar**2, -1.0])
            xx, yy = np.meshgrid(np.linspace(-0.5, 1.9, 8), np.linspace(-0.5, 1.6, 8))
            zz = z0 + x0 / apar**2 * (xx - x0) + y0 / bpar**2 * (yy - y0)
            axes[2].plot_surface(X, Y, Z, alpha=0.55, linewidth=0, color="seagreen")
            axes[2].plot_surface(xx, yy, zz, alpha=0.35, color="crimson")
            axes[2].plot([P[0], P[0] + N[0]], [P[1], P[1] + N[1]], [P[2], P[2] + N[2]], color="black", linewidth=2)
            axes[2].scatter(*P, color="black")
            setup_3d(axes[2], (-2, 2), (-1.7, 1.7), (-0.4, 2.2), "5.8и")

            for ax in axes:
                set_axes_equal_3d(ax)


            def animate(i):
                for ax in axes:
                    ax.view_init(elev=24, azim=35 + 2 * i)
                return []


            anim = FuncAnimation(fig, animate, frames=120, interval=70)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_05():
    write_notebook(
        "lab_05_6_2_6_8_6_11_6_12_metric.ipynb",
        [
            md(r"""
            # Лабораторная 5. Задачи 6.2, 6.8, 6.11, 6.12

            Тема работы: первая квадратичная форма, ортогональные траектории,
            длины, площади и углы на поверхности.
            """),
            md(r"""
            ## Задача 6.2: первая квадратичная форма

            Пусть \(l\) — натуральный параметр кривой \(\gamma(l)\), то есть
            \(|\gamma'(l)|=1\). Обозначим \(T=\gamma'\), кривизну \(k(l)\),
            кручение \(\tau(l)\), главную нормаль \(n(l)\) и бинормаль \(b(l)\).

            ### а) \(r(l,\lambda)=\gamma(l)+\lambda a,\ a=\mathrm{const}\)

            \[
            r_l=T,\qquad r_\lambda=a.
            \]

            Поэтому

            \[
            \boxed{
            I=dl^2+2(T,a)\,dl\,d\lambda+|a|^2d\lambda^2.
            }
            \]

            Если направляющая выбрана ортогонально образующим, то \((T,a)=0\).

            ### б) \(r(l,\lambda)=\gamma(l)+\lambda e(l),\ |e(l)|=1\)

            \[
            r_l=T+\lambda e',\qquad r_\lambda=e.
            \]

            Так как \(|e|=1\), имеем \((e',e)=0\). Тогда

            \[
            \boxed{
            E=1+2\lambda(T,e')+\lambda^2|e'|^2,\quad
            F=(T,e),\quad G=1.
            }
            \]

            ### в) \(r(l,\lambda)=\gamma(l)+\lambda n(l)\)

            По формулам Френе:

            \[
            n'=-kT+\tau b.
            \]

            Значит,

            \[
            r_l=(1-\lambda k)T+\lambda\tau b,\qquad r_\lambda=n.
            \]

            Отсюда

            \[
            \boxed{
            I=\bigl((1-\lambda k)^2+\lambda^2\tau^2\bigr)\,dl^2+d\lambda^2.
            }
            \]

            ### г) \(r(l,\varphi)=\gamma(l)+n(l)\cos\varphi+b(l)\sin\varphi\)

            \[
            r_l=(1-k\cos\varphi)T-\tau\sin\varphi\,n+\tau\cos\varphi\,b,
            \]

            \[
            r_\varphi=-n\sin\varphi+b\cos\varphi.
            \]

            Поэтому

            \[
            \boxed{
            E=(1-k\cos\varphi)^2+\tau^2,\quad
            F=\tau,\quad
            G=1.
            }
            \]

            И первая форма:

            \[
            \boxed{
            I=\bigl((1-k\cos\varphi)^2+\tau^2\bigr)\,dl^2
            +2\tau\,dl\,d\varphi+d\varphi^2.
            }
            \]
            """),
            code(COMMON_3D),
            code(r"""
            # Динамическая иллюстрация к 6.2г: трубка вокруг винтовой линии.
            a = 1.2
            b = 0.35
            radius = 0.28


            def helix(t):
                return np.array([a * np.cos(t), a * np.sin(t), b * t])


            def frame(t):
                c = np.sqrt(a**2 + b**2)
                T = np.array([-a * np.sin(t) / c, a * np.cos(t) / c, np.full_like(t, b / c)])
                N = np.array([-np.cos(t), -np.sin(t), np.zeros_like(t)])
                B = np.array([b * np.sin(t) / c, -b * np.cos(t) / c, np.full_like(t, a / c)])
                return T, N, B


            t = np.linspace(0, 5 * np.pi, 160)
            phi = np.linspace(0, 2 * np.pi, 28)
            Tgrid, Phigrid = np.meshgrid(t, phi)
            base = helix(Tgrid)
            _, N, Bv = frame(Tgrid)
            tube = base + radius * (N * np.cos(Phigrid) + Bv * np.sin(Phigrid))

            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            setup_3d(ax, (-1.8, 1.8), (-1.8, 1.8), (-0.5, 6.0), "6.2: каналовая поверхность")
            ax.plot_surface(tube[0], tube[1], tube[2], alpha=0.65, linewidth=0, color="steelblue")
            center = helix(t)
            ax.plot(center[0], center[1], center[2], color="navy", linewidth=2)
            ring_line, = ax.plot([], [], [], color="crimson", linewidth=2)
            set_axes_equal_3d(ax)


            def animate(i):
                k = int(i / 100 * (len(t) - 1))
                ring = tube[:, :, k]
                ring_line.set_data(ring[0], ring[1])
                ring_line.set_3d_properties(ring[2])
                ax.view_init(elev=24, azim=35 + i)
                return ring_line,


            anim = FuncAnimation(fig, animate, frames=101, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 6.8: ортогональные траектории на сфере

            Сфера:

            \[
            r(u,v)=(R\cos u\cos v,\ R\cos u\sin v,\ R\sin u).
            \]

            Первая квадратичная форма:

            \[
            r_u=(-R\sin u\cos v,-R\sin u\sin v,R\cos u),
            \]

            \[
            r_v=(-R\cos u\sin v,R\cos u\cos v,0).
            \]

            Поэтому

            \[
            E=R^2,\qquad F=0,\qquad G=R^2\cos^2u.
            \]

            Дано семейство

            \[
            u+v=C.
            \]

            Его касательный вектор в параметрической плоскости можно взять как
            \((du,dv)=(1,-1)\). Пусть ортогональная траектория имеет касательный
            вектор \((du,dv)\). Условие ортогональности:

            \[
            R^2du-R^2\cos^2u\,dv=0.
            \]

            Значит,

            \[
            \frac{dv}{du}=\sec^2u.
            \]

            Интегрируем:

            \[
            \boxed{v=\tan u+C.}
            \]
            """),
            code(r"""
            R = 1.6


            def sphere_uv(u, v):
                return np.array([R * np.cos(u) * np.cos(v), R * np.cos(u) * np.sin(v), R * np.sin(u)])


            u = np.linspace(-1.1, 1.1, 300)
            family = []
            orth = []
            for c0 in np.linspace(-2.0, 2.0, 9):
                family.append(sphere_uv(u, c0 - u))
                orth.append(sphere_uv(u, np.tan(u) + c0))

            su = np.linspace(-np.pi / 2, np.pi / 2, 45)
            sv = np.linspace(0, 2 * np.pi, 70)
            SU, SV = np.meshgrid(su, sv)
            S = sphere_uv(SU, SV)

            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")
            setup_3d(ax, (-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8), "6.8: семейство и ортогональные траектории")
            ax.plot_surface(S[0], S[1], S[2], alpha=0.12, linewidth=0, color="steelblue")
            for curve in family:
                ax.plot(curve[0], curve[1], curve[2], color="navy", linewidth=1)
            for curve in orth:
                ax.plot(curve[0], curve[1], curve[2], color="crimson", linewidth=1)
            set_axes_equal_3d(ax)


            def animate(i):
                ax.view_init(elev=24, azim=35 + 2 * i)
                return []


            anim = FuncAnimation(fig, animate, frames=120, interval=70)
            finish_animation(anim, fig)
            """),
            md(r"""
            ## Задача 6.11: форма \(ds^2=du^2+(u^2+a^2)dv^2\)

            Здесь

            \[
            E=1,\qquad F=0,\qquad G=u^2+a^2,
            \]

            а элемент площади равен

            \[
            dS=\sqrt{EG-F^2}\,du\,dv=\sqrt{u^2+a^2}\,du\,dv.
            \]

            ### а) Периметр треугольника \(u=\pm\frac a2v^2,\ v=1\)

            Вершины: \((0,0)\), \((a/2,1)\), \((-a/2,1)\).

            Верхняя сторона \(v=1\):

            \[
            ds=|du|,\qquad L_0=a.
            \]

            Правая боковая сторона \(u=\frac a2v^2\):

            \[
            du=av\,dv.
            \]

            Тогда

            \[
            ds^2=a^2v^2dv^2+
            \left(\frac{a^2v^4}{4}+a^2\right)dv^2
            =a^2\left(1+\frac{v^2}{2}\right)^2dv^2.
            \]

            \[
            L_1=a\int_0^1\left(1+\frac{v^2}{2}\right)dv
            =a\left(1+\frac16\right)=\frac{7a}{6}.
            \]

            Две боковые стороны равны, поэтому

            \[
            \boxed{P=a+2\cdot\frac{7a}{6}=\frac{10a}{3}.}
            \]

            ### б) Углы этого треугольника

            В нижней вершине обе боковые стороны имеют общую касательную
            \(du/dv=0\), поэтому угол равен \(0\).

            В правой верхней вершине \((a/2,1)\) берем два направления внутрь
            треугольника:

            \[
            X=(-1,0),\qquad Y=(-a,-1).
            \]

            Там \(G=(a/2)^2+a^2=5a^2/4\). Тогда

            \[
            (X,Y)=a,\qquad |X|=1,\qquad
            |Y|=\sqrt{a^2+\frac{5a^2}{4}}=\frac{3a}{2}.
            \]

            \[
            \cos\alpha=\frac{2}{3}.
            \]

            Оба верхних угла равны:

            \[
            \boxed{\alpha_1=0,\qquad
            \alpha_2=\alpha_3=\arccos\frac23.}
            \]

            ### в) Площадь треугольника \(u=\pm av,\ v=1\)

            Область:

            \[
            0\le v\le1,\qquad -av\le u\le av.
            \]

            \[
            S=\int_0^1\int_{-av}^{av}\sqrt{u^2+a^2}\,du\,dv.
            \]

            Подстановка \(u=as\):

            \[
            S=2a^2\int_0^1(1-s)\sqrt{1+s^2}\,ds.
            \]

            После интегрирования:

            \[
            \boxed{
            S=a^2\left(\operatorname{arsinh}1+\frac{2-\sqrt2}{3}\right).
            }
            \]
            """),
            md(r"""
            ## Задача 6.12: поверхность \(r(u,v)=(u\sin v,u\cos v,v)\)

            Производные:

            \[
            r_u=(\sin v,\cos v,0),\qquad
            r_v=(u\cos v,-u\sin v,1).
            \]

            Поэтому

            \[
            \boxed{E=1,\quad F=0,\quad G=1+u^2.}
            \]

            Область:

            \[
            0\le u\le\sinh v,\qquad 0\le v\le v_0.
            \]

            ### а) Площадь

            \[
            S=\int_0^{v_0}\int_0^{\sinh v}\sqrt{1+u^2}\,du\,dv.
            \]

            Так как

            \[
            \int_0^{\sinh v}\sqrt{1+u^2}\,du
            =\frac12(\sinh v\cosh v+v),
            \]

            получаем

            \[
            \boxed{S=\frac14\sinh^2v_0+\frac14v_0^2.}
            \]

            ### б) Длины сторон

            1. \(u=0,\ 0\le v\le v_0\):

            \[
            ds=dv,\qquad \boxed{L_1=v_0.}
            \]

            2. \(v=v_0,\ 0\le u\le\sinh v_0\):

            \[
            ds=du,\qquad \boxed{L_2=\sinh v_0.}
            \]

            3. \(u=\sinh v\):

            \[
            du=\cosh v\,dv,\qquad G=1+\sinh^2v=\cosh^2v.
            \]

            \[
            ds^2=\cosh^2v\,dv^2+\cosh^2v\,dv^2
            =2\cosh^2v\,dv^2.
            \]

            \[
            \boxed{L_3=\sqrt2\sinh v_0.}
            \]

            ### в) Углы

            В точке \((0,v_0)\) пересекаются координатные линии \(u=0\) и
            \(v=v_0\), а \(F=0\), поэтому угол равен \(\pi/2\).

            В точке \((0,0)\) направления сторон можно взять как \((0,1)\) и
            \((1,1)\). Метрика там евклидова, значит угол равен \(\pi/4\).

            В третьей вершине получается такой же угол \(\pi/4\). Итак,

            \[
            \boxed{\alpha_1=\frac\pi4,\qquad
            \alpha_2=\frac\pi2,\qquad
            \alpha_3=\frac\pi4.}
            \]
            """),
            code(r"""
            # Динамика области из 6.12 на поверхности при росте v0.
            v0_final = 1.4
            frames = 90


            def surf(u, v):
                return np.array([u * np.sin(v), u * np.cos(v), v])


            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection="3d")


            def animate(i):
                ax.clear()
                v0 = 0.15 + (v0_final - 0.15) * i / (frames - 1)
                vv = np.linspace(0, v0, 70)
                ss = np.linspace(0, 1, 28)
                Sg, Vg = np.meshgrid(ss, vv)
                Ug = Sg * np.sinh(Vg)
                P = surf(Ug, Vg)
                setup_3d(ax, (-1.4, 1.4), (-0.2, 1.8), (-0.1, 1.6), f"6.12: область, v0={v0:.2f}")
                ax.plot_surface(P[0], P[1], P[2], alpha=0.70, linewidth=0, color="steelblue")
                for uu, vv_line, color in [
                    (np.zeros_like(vv), vv, "crimson"),
                    (np.linspace(0, np.sinh(v0), 80), np.full(80, v0), "darkorange"),
                    (np.sinh(vv), vv, "purple"),
                ]:
                    C = surf(uu, vv_line)
                    ax.plot(C[0], C[1], C[2], color=color, linewidth=2.5)
                ax.view_init(elev=25, azim=35 + i)
                set_axes_equal_3d(ax)
                return []


            anim = FuncAnimation(fig, animate, frames=frames, interval=80)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_06():
    write_notebook(
        "lab_06_6_16_angle_bisectors.ipynb",
        [
            md(r"""
            # Лабораторная 6. Задача 6.16: биссектрисы координатных линий

            Дана первая квадратичная форма поверхности. Нужно найти линии,
            которые в каждой точке делят пополам углы между координатными
            линиями.
            """),
            md(r"""
            ## Общий принцип

            Пусть

            \[
            ds^2=E\,du^2+2F\,du\,dv+G\,dv^2.
            \]

            Координатные направления в касательной плоскости — это \(r_u\) и
            \(r_v\). Их единичные направления:

            \[
            \frac{r_u}{\sqrt E},\qquad \frac{r_v}{\sqrt G}.
            \]

            Направления биссектрис задаются суммой и разностью этих единичных
            векторов:

            \[
            \frac{r_u}{\sqrt E}\pm \frac{r_v}{\sqrt G}.
            \]

            Если касательный вектор искомой линии равен
            \(dr=r_u\,du+r_v\,dv\), то коэффициенты должны быть пропорциональны:

            \[
            du:dv=\frac1{\sqrt E}:\pm\frac1{\sqrt G}.
            \]

            Поэтому для двух семейств биссектрис:

            \[
            \boxed{\frac{dv}{du}=\pm\sqrt{\frac EG}.}
            \]

            Важно: коэффициент \(F\) влияет на сам угол между координатными
            линиями, но направления биссектрис в координатах \(u,v\) выражаются
            через длины \(r_u\) и \(r_v\), то есть через \(E\) и \(G\).
            """),
            md(r"""
            ## а)

            \[
            ds^2=(1+e^{2v})du^2-2e^{2u}du\,dv+e^{2u}dv^2.
            \]

            \[
            E=1+e^{2v},\qquad G=e^{2u}.
            \]

            \[
            \frac{dv}{du}=\pm e^{-u}\sqrt{1+e^{2v}}.
            \]

            Разделяем переменные:

            \[
            \frac{dv}{\sqrt{1+e^{2v}}}=\pm e^{-u}du.
            \]

            \[
            \int\frac{dv}{\sqrt{1+e^{2v}}}
            =-\operatorname{arsinh}(e^{-v}).
            \]

            Значит,

            \[
            \boxed{\operatorname{arsinh}(e^{-v})\pm e^{-u}=C.}
            \]

            ## б)

            \[
            ds^2=du^2+(2u-1)du\,dv+(1+u^2)dv^2.
            \]

            \[
            E=1,\qquad G=1+u^2.
            \]

            \[
            \frac{dv}{du}=\pm\frac1{\sqrt{1+u^2}}.
            \]

            \[
            \boxed{v=\pm\operatorname{arsinh}u+C.}
            \]

            ## в)

            \[
            ds^2=du^2+2\sin(u-v)du\,dv+dv^2.
            \]

            Здесь \(E=G=1\), поэтому

            \[
            \frac{dv}{du}=\pm1.
            \]

            \[
            \boxed{v-u=C,\qquad v+u=C.}
            \]

            ## г)

            \[
            ds^2=\bigl(1+(1+v)^2\bigr)du^2
            -2(1+v)^2du\,dv+(1+v)^2dv^2.
            \]

            \[
            E=1+(1+v)^2,\qquad G=(1+v)^2.
            \]

            Для области \(1+v>0\):

            \[
            \frac{dv}{du}=
            \pm\frac{\sqrt{1+(1+v)^2}}{1+v}.
            \]

            Удобнее перевернуть:

            \[
            \frac{du}{dv}=\pm\frac{1+v}{\sqrt{1+(1+v)^2}}.
            \]

            Интегрируем:

            \[
            \boxed{u\mp\sqrt{1+(1+v)^2}=C.}
            \]
            """),
            code(COMMON_2D),
            code(r"""
            def curves_for_case(case, sign, constants, u_grid=None, v_grid=None):
                if case == "a":
                    # asinh(exp(-v)) - sign*exp(-u) = C
                    u = np.linspace(-0.2, 2.1, 400)
                    result = []
                    for C in constants:
                        A = C + sign * np.exp(-u)
                        mask = A > 0.03
                        v = np.full_like(u, np.nan)
                        v[mask] = -np.log(np.sinh(A[mask]))
                        result.append((u, v))
                    return result
                if case == "b":
                    u = np.linspace(-2.2, 2.2, 400)
                    return [(u, sign * np.arcsinh(u) + C) for C in constants]
                if case == "c":
                    u = np.linspace(-2.2, 2.2, 400)
                    return [(u, sign * u + C) for C in constants]
                if case == "d":
                    v = np.linspace(-0.75, 2.2, 400)
                    return [(C + sign * np.sqrt(1 + (1 + v) ** 2), v) for C in constants]
                raise ValueError(case)


            cases = ["a", "b", "c", "d"]
            titles = {
                "a": "6.16а",
                "b": "6.16б",
                "c": "6.16в",
                "d": "6.16г",
            }
            constants = np.linspace(-1.5, 1.5, 9)

            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            axes = axes.ravel()


            def animate(frame):
                for ax, case in zip(axes, cases):
                    ax.clear()
                    setup_2d(ax, (-2.5, 2.5), (-2.5, 2.5), titles[case])
                    shift = 0.6 * np.sin(2 * np.pi * frame / 100)
                    for sign, color in [(1, "navy"), (-1, "crimson")]:
                        for u, v in curves_for_case(case, sign, constants + shift):
                            ax.plot(u, v, color=color, linewidth=1.2, alpha=0.75)
                    ax.text(-2.35, 2.15, "синие и красные линии — два семейства", fontsize=8)
                return []


            anim = FuncAnimation(fig, animate, frames=100, interval=80)
            finish_animation(anim, fig)
            """),
        ],
    )


def lab_07():
    write_notebook(
        "lab_07_7_18_dupin.ipynb",
        [
            md(r"""
            # Лабораторная 7. Задача 7.18: индикатриса Дюпена

            Индикатриса Дюпена в точке поверхности задается второй квадратичной
            формой. В ортонормированных главных координатах \((\xi,\eta)\):

            \[
            k_1\xi^2+k_2\eta^2=\pm1,
            \]

            где \(k_1,k_2\) — главные кривизны.
            """),
            md(r"""
            ## а) Сфера

            \[
            r(u,v)=(R\cos u\cos v,\ R\cos u\sin v,\ R\sin u),
            \quad u=v=\frac\pi4.
            \]

            Для сферы радиуса \(R\) обе главные кривизны по модулю равны
            \(1/R\). При внешней нормали они отрицательны:

            \[
            k_1=k_2=-\frac1R.
            \]

            Индикатриса является окружностью:

            \[
            -\frac1R(\xi^2+\eta^2)=-1.
            \]

            \[
            \boxed{\xi^2+\eta^2=R.}
            \]

            В параметрических приращениях:

            \[
            E=R^2,\qquad G=R^2\cos^2u.
            \]

            При \(u=\pi/4\):

            \[
            \xi=R\,du,\qquad \eta=\frac{R}{\sqrt2}\,dv,
            \]

            и

            \[
            \boxed{R\,du^2+\frac R2\,dv^2=1.}
            \]

            ## б) Цилиндр

            \[
            r(u,v)=(a\cos v,\ a\sin v,\ u).
            \]

            Одна главная кривизна равна нулю, другая по модулю равна \(1/a\):

            \[
            k_1=0,\qquad k_2=-\frac1a.
            \]

            Поэтому индикатриса вырождается в пару параллельных прямых:

            \[
            -\frac1a\eta^2=-1.
            \]

            \[
            \boxed{\eta^2=a,\qquad \eta=\pm\sqrt a.}
            \]

            ## в) \(z=2x^2+\frac92y^2\), начало координат

            В начале координат касательная плоскость горизонтальна, первая форма
            совпадает с \(dx^2+dy^2\). Для графика \(z=f(x,y)\):

            \[
            f_{xx}=4,\qquad f_{xy}=0,\qquad f_{yy}=9.
            \]

            Поэтому

            \[
            II=4\,dx^2+9\,dy^2.
            \]

            Индикатриса:

            \[
            \boxed{4\xi^2+9\eta^2=1.}
            \]

            Это эллипс.

            ## г) \(r(u,v)=(\cosh u\cos v,\cosh u\sin v,u)\)

            Производные:

            \[
            r_u=(\sinh u\cos v,\sinh u\sin v,1),
            \]

            \[
            r_v=(-\cosh u\sin v,\cosh u\cos v,0).
            \]

            Первая форма:

            \[
            E=G=\cosh^2u,\qquad F=0.
            \]

            При выборе нормали

            \[
            n=\left(-\frac{\cos v}{\cosh u},-\frac{\sin v}{\cosh u},\tanh u\right)
            \]

            получаем

            \[
            L=-1,\qquad M=0,\qquad N=1.
            \]

            Значит,

            \[
            II=-du^2+dv^2.
            \]

            В ортонормированных координатах
            \(\xi=\cosh u\,du,\ \eta=\cosh u\,dv\):

            \[
            II=\frac{-\xi^2+\eta^2}{\cosh^2u}.
            \]

            Индикатриса:

            \[
            \boxed{\eta^2-\xi^2=\pm\cosh^2u.}
            \]

            Это пара сопряженных гипербол.
            """),
            code(COMMON_2D),
            code(r"""
            frames = 100
            theta = np.linspace(0, 2 * np.pi, 500)
            t = np.linspace(-2.2, 2.2, 500)

            fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex="col")
            axes = axes.ravel()


            def animate(i):
                for ax in axes:
                    ax.clear()
                    ax.axhline(0, color="0.35", linewidth=1)
                    ax.axvline(0, color="0.35", linewidth=1)
                    ax.set_aspect("equal", adjustable="box")
                    ax.set_xlabel(r"$\xi$")
                    ax.set_ylabel(r"$\eta$")

                R = 1.0 + 1.2 * i / (frames - 1)
                axes[0].plot(np.sqrt(R) * np.cos(theta), np.sqrt(R) * np.sin(theta), color="navy", linewidth=2)
                axes[0].set_title(f"7.18а: сфера, R={R:.2f}")
                axes[0].set_xlim(-1.8, 1.8)
                axes[0].set_ylim(-1.8, 1.8)

                a = 0.6 + 1.5 * i / (frames - 1)
                y = np.sqrt(a)
                axes[1].plot(t, np.full_like(t, y), color="crimson", linewidth=2)
                axes[1].plot(t, -np.full_like(t, y), color="crimson", linewidth=2)
                axes[1].set_title(f"7.18б: цилиндр, a={a:.2f}")
                axes[1].set_xlim(-2.2, 2.2)
                axes[1].set_ylim(-2.2, 2.2)

                axes[2].plot(0.5 * np.cos(theta), (1 / 3) * np.sin(theta), color="darkgreen", linewidth=1.2, alpha=0.25)
                phi = 2 * np.pi * i / (frames - 1)
                theta_trace = np.linspace(0, phi, max(2, 5 * i + 2))
                axes[2].plot(
                    0.5 * np.cos(theta_trace),
                    (1 / 3) * np.sin(theta_trace),
                    color="darkgreen",
                    linewidth=2.5,
                )
                axes[2].scatter(
                    [0.5 * np.cos(phi)],
                    [(1 / 3) * np.sin(phi)],
                    color="crimson",
                    s=35,
                    zorder=5,
                )
                axes[2].set_title(r"7.18в: $4\xi^2+9\eta^2=1$")
                axes[2].set_ylim(-0.8, 0.8)

                u = -1.2 + 2.4 * i / (frames - 1)
                c = np.cosh(u)
                x = np.linspace(-2.3, 2.3, 500)
                y1 = np.sqrt(x**2 + c**2)
                x2 = np.sqrt(t**2 + c**2)
                axes[3].plot(x, y1, color="purple", linewidth=2)
                axes[3].plot(x, -y1, color="purple", linewidth=2)
                axes[3].plot(x2, t, color="purple", linewidth=1.2, linestyle="--")
                axes[3].plot(-x2, t, color="purple", linewidth=1.2, linestyle="--")
                axes[3].set_title(f"7.18г: u={u:.2f}")
                axes[3].set_ylim(-3, 3)
                axes[0].set_xlim(-1.8, 1.8)
                axes[1].set_xlim(-3, 3)
                return []


            anim = FuncAnimation(fig, animate, frames=frames, interval=80)
            finish_animation(anim, fig)
            """),
        ],
    )


def main():
    lab_01()
    lab_02()
    lab_03()
    lab_04()
    lab_05()
    lab_06()
    lab_07()
    separate_analytical_solutions()


if __name__ == "__main__":
    main()
