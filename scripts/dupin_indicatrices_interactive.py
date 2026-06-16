from __future__ import annotations

from pathlib import Path

try:
    from plotly.offline import get_plotlyjs
except ImportError as exc:  # pragma: no cover - user-facing dependency hint
    raise SystemExit(
        "Plotly is required. Install it with: "
        "venv\\Scripts\\python.exe -m pip install plotly"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "dupin_indicatrices_interactive.html"


HTML = r"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Индикатрисы Дюпена: интерактивные графики</title>
  <style>
    :root {
      --ink: #18233b;
      --muted: #5d6880;
      --panel: #ffffff;
      --line: #d9e1ec;
      --accent: #2b6cb0;
      --surface: #e8f1f6;
      --plane: #f1bd50;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      color: var(--ink);
      background: #f4f7fb;
      font-family: Inter, Segoe UI, Arial, sans-serif;
    }

    header {
      padding: 24px 28px 14px;
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }

    h1 {
      margin: 0 0 8px;
      font-size: 28px;
      line-height: 1.15;
      letter-spacing: 0;
    }

    header p {
      margin: 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.45;
      max-width: 1120px;
    }

    main {
      display: grid;
      grid-template-columns: repeat(2, minmax(420px, 1fr));
      gap: 18px;
      padding: 18px;
    }

    .panel {
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 8px 26px rgba(24, 35, 59, 0.07);
    }

    .panel-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      padding: 16px 18px 8px;
      border-bottom: 1px solid #edf2f7;
    }

    .panel-title {
      min-width: 0;
    }

    h2 {
      margin: 0 0 6px;
      font-size: 19px;
      line-height: 1.2;
      letter-spacing: 0;
    }

    .formula {
      margin: 0;
      color: var(--muted);
      font-family: Cambria Math, Times New Roman, serif;
      font-size: 16px;
      line-height: 1.25;
    }

    .badge {
      flex: 0 0 auto;
      padding: 5px 8px;
      border: 1px solid #d7e3f3;
      border-radius: 999px;
      color: #244a7a;
      background: #eef6ff;
      font-size: 12px;
      font-weight: 700;
    }

    .plot {
      height: 540px;
      width: 100%;
    }

    .controls {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px 16px;
      padding: 12px 18px 18px;
      border-top: 1px solid #edf2f7;
      background: #fbfdff;
    }

    .control {
      min-width: 0;
    }

    .control-row {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 6px;
      color: #24324d;
      font-size: 13px;
      font-weight: 700;
    }

    output {
      color: var(--accent);
      font-variant-numeric: tabular-nums;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--accent);
    }

    @media (max-width: 980px) {
      main {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 560px) {
      header {
        padding: 20px 16px 12px;
      }

      main {
        padding: 12px;
      }

      .plot {
        height: 460px;
      }

      .controls {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <header>
    <h1>Индикатрисы Дюпена для задачи 7.18</h1>
    <p>
      В каждой сцене показана вся поверхность в естественном диапазоне угла вращения,
      выбранная точка, касательная плоскость и индикатриса Дюпена в этой плоскости.
      Параметры меняются ползунками прямо во время просмотра.
    </p>
  </header>

  <main>
    <section class="panel">
      <div class="panel-head">
        <div class="panel-title">
          <h2>а) Сфера</h2>
          <p class="formula">r(u,v)=(R cos u cos v, R cos u sin v, R sin u), u=v=pi/4</p>
        </div>
        <div class="badge">эллиптическая</div>
      </div>
      <div id="spherePlot" class="plot"></div>
      <div class="controls">
        <div class="control">
          <div class="control-row"><span>Радиус R</span><output id="sphereRValue"></output></div>
          <input id="sphereR" type="range" min="0.6" max="4.0" step="0.05" value="2.0" />
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div class="panel-title">
          <h2>б) Круговой цилиндр</h2>
          <p class="formula">r(u,v)=(a cos v, a sin v, u), точка произвольная</p>
        </div>
        <div class="badge">параболическая</div>
      </div>
      <div id="cylinderPlot" class="plot"></div>
      <div class="controls">
        <div class="control">
          <div class="control-row"><span>Радиус a</span><output id="cylinderAValue"></output></div>
          <input id="cylinderA" type="range" min="0.5" max="3.5" step="0.05" value="1.4" />
        </div>
        <div class="control">
          <div class="control-row"><span>Высота точки u0</span><output id="cylinderUValue"></output></div>
          <input id="cylinderU" type="range" min="-4.0" max="4.0" step="0.05" value="0.8" />
        </div>
        <div class="control">
          <div class="control-row"><span>Угол точки v0</span><output id="cylinderVValue"></output></div>
          <input id="cylinderV" type="range" min="0" max="6.2831853" step="0.01" value="0.8" />
        </div>
        <div class="control">
          <div class="control-row"><span>Половина высоты</span><output id="cylinderHValue"></output></div>
          <input id="cylinderH" type="range" min="1.0" max="6.0" step="0.05" value="3.0" />
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div class="panel-title">
          <h2>в) Эллиптический параболоид</h2>
          <p class="formula">z=A x^2+B y^2, по условию A=2, B=9/2, точка (0,0,0)</p>
        </div>
        <div class="badge">эллиптическая</div>
      </div>
      <div id="paraboloidPlot" class="plot"></div>
      <div class="controls">
        <div class="control">
          <div class="control-row"><span>Коэффициент A</span><output id="paraboloidAValue"></output></div>
          <input id="paraboloidA" type="range" min="0.5" max="4.0" step="0.05" value="2.0" />
        </div>
        <div class="control">
          <div class="control-row"><span>Коэффициент B</span><output id="paraboloidBValue"></output></div>
          <input id="paraboloidB" type="range" min="0.5" max="7.0" step="0.05" value="4.5" />
        </div>
        <div class="control">
          <div class="control-row"><span>Размер области</span><output id="paraboloidDValue"></output></div>
          <input id="paraboloidD" type="range" min="0.5" max="2.0" step="0.05" value="1.0" />
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div class="panel-title">
          <h2>г) Катеноид</h2>
          <p class="formula">r(u,v)=(cosh u cos v, cosh u sin v, u), точка произвольная</p>
        </div>
        <div class="badge">гиперболическая</div>
      </div>
      <div id="catenoidPlot" class="plot"></div>
      <div class="controls">
        <div class="control">
          <div class="control-row"><span>Параметр точки u0</span><output id="catenoidUValue"></output></div>
          <input id="catenoidU" type="range" min="-1.8" max="1.8" step="0.02" value="0.8" />
        </div>
        <div class="control">
          <div class="control-row"><span>Угол точки v0</span><output id="catenoidVValue"></output></div>
          <input id="catenoidV" type="range" min="0" max="6.2831853" step="0.01" value="0.9" />
        </div>
        <div class="control">
          <div class="control-row"><span>Диапазон |u|</span><output id="catenoidRangeValue"></output></div>
          <input id="catenoidRange" type="range" min="1.2" max="3.0" step="0.05" value="2.4" />
        </div>
      </div>
    </section>
  </main>

  <script>
__PLOTLY_JS__
  </script>
  <script>
    const PI = Math.PI;
    const CONFIG = {
      displaylogo: false,
      responsive: true,
      scrollZoom: true,
      modeBarButtonsToRemove: ["lasso2d", "select2d"]
    };

    const surfaceScale = [
      [0.0, "rgb(219, 235, 247)"],
      [0.5, "rgb(246, 249, 251)"],
      [1.0, "rgb(219, 235, 225)"]
    ];

    const paraboloidScale = [
      [0.0, "rgb(231, 241, 235)"],
      [0.55, "rgb(248, 249, 244)"],
      [1.0, "rgb(235, 223, 244)"]
    ];

    function num(id) {
      return Number(document.getElementById(id).value);
    }

    function setOut(id, value, digits = 2) {
      document.getElementById(id).value = Number(value).toFixed(digits);
    }

    function linspace(start, end, count) {
      const result = [];
      if (count === 1) return [start];
      const step = (end - start) / (count - 1);
      for (let i = 0; i < count; i += 1) result.push(start + step * i);
      return result;
    }

    function add(a, b) {
      return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
    }

    function scale(a, s) {
      return [a[0] * s, a[1] * s, a[2] * s];
    }

    function surfaceTrace(name, data, colorscale = surfaceScale, opacity = 0.68) {
      return {
        type: "surface",
        name,
        x: data.x,
        y: data.y,
        z: data.z,
        colorscale,
        showscale: false,
        opacity,
        hoverinfo: "skip",
        contours: {
          x: { show: false },
          y: { show: false },
          z: { show: false }
        }
      };
    }

    function tangentPlaneTrace(center, e1, e2, size, name = "касательная плоскость") {
      const coords = [-size, size];
      const x = [];
      const y = [];
      const z = [];
      for (const s of coords) {
        const rowX = [];
        const rowY = [];
        const rowZ = [];
        for (const t of coords) {
          const p = add(center, add(scale(e1, s), scale(e2, t)));
          rowX.push(p[0]);
          rowY.push(p[1]);
          rowZ.push(p[2]);
        }
        x.push(rowX);
        y.push(rowY);
        z.push(rowZ);
      }
      return {
        type: "surface",
        name,
        x,
        y,
        z,
        surfacecolor: [[0, 0], [0, 0]],
        colorscale: [[0, "rgb(245, 190, 80)"], [1, "rgb(245, 190, 80)"]],
        showscale: false,
        opacity: 0.35,
        hoverinfo: "skip"
      };
    }

    function curveTrace(name, points, color, width = 8) {
      return {
        type: "scatter3d",
        mode: "lines",
        name,
        x: points.map((p) => p[0]),
        y: points.map((p) => p[1]),
        z: points.map((p) => p[2]),
        line: { color, width },
        hoverinfo: "name"
      };
    }

    function markerTrace(name, point, color = "#d62828", size = 5) {
      return {
        type: "scatter3d",
        mode: "markers",
        name,
        x: [point[0]],
        y: [point[1]],
        z: [point[2]],
        marker: {
          color,
          size,
          line: { color: "#ffffff", width: 1.5 }
        },
        hoverinfo: "name"
      };
    }

    function lineTrace(name, a, b, color = "#7a869a", width = 5) {
      return {
        type: "scatter3d",
        mode: "lines",
        name,
        x: [a[0], b[0]],
        y: [a[1], b[1]],
        z: [a[2], b[2]],
        line: { color, width },
        hoverinfo: "name",
        showlegend: false
      };
    }

    function tangentCurve(center, e1, e2, xyPairs) {
      return xyPairs.map(([x, y]) => add(center, add(scale(e1, x), scale(e2, y))));
    }

    function sceneLayout(title, camera, height = 540) {
      const axis = {
        backgroundcolor: "rgb(244, 248, 252)",
        gridcolor: "rgb(210, 220, 233)",
        zerolinecolor: "rgb(151, 164, 184)",
        showspikes: false
      };
      return {
        title: {
          text: title,
          x: 0.5,
          xanchor: "center",
          font: { size: 17, color: "#18233b" }
        },
        height,
        margin: { l: 0, r: 0, t: 42, b: 0 },
        paper_bgcolor: "#ffffff",
        legend: {
          x: 0.02,
          y: 0.98,
          bgcolor: "rgba(255,255,255,0.78)",
          bordercolor: "rgba(24,35,59,0.12)",
          borderwidth: 1,
          font: { size: 12 }
        },
        scene: {
          aspectmode: "data",
          xaxis: { ...axis, title: "x" },
          yaxis: { ...axis, title: "y" },
          zaxis: { ...axis, title: "z" },
          camera
        }
      };
    }

    function buildSphereSurface(R) {
      const us = linspace(-PI / 2, PI / 2, 70);
      const vs = linspace(0, 2 * PI, 130);
      const x = [];
      const y = [];
      const z = [];
      for (const u of us) {
        const rowX = [];
        const rowY = [];
        const rowZ = [];
        for (const v of vs) {
          rowX.push(R * Math.cos(u) * Math.cos(v));
          rowY.push(R * Math.cos(u) * Math.sin(v));
          rowZ.push(R * Math.sin(u));
        }
        x.push(rowX);
        y.push(rowY);
        z.push(rowZ);
      }
      return { x, y, z };
    }

    function renderSphere() {
      const R = num("sphereR");
      setOut("sphereRValue", R);

      const u0 = PI / 4;
      const v0 = PI / 4;
      const center = [
        R * Math.cos(u0) * Math.cos(v0),
        R * Math.cos(u0) * Math.sin(v0),
        R * Math.sin(u0)
      ];
      const eU = [-Math.sin(u0) * Math.cos(v0), -Math.sin(u0) * Math.sin(v0), Math.cos(u0)];
      const eV = [-Math.sin(v0), Math.cos(v0), 0];
      const normal = [Math.cos(u0) * Math.cos(v0), Math.cos(u0) * Math.sin(v0), Math.sin(u0)];

      const indicatrixRadius = Math.sqrt(R);
      const ts = linspace(0, 2 * PI, 260);
      const circleXY = ts.map((t) => [indicatrixRadius * Math.cos(t), indicatrixRadius * Math.sin(t)]);

      const traces = [
        surfaceTrace("сфера целиком", buildSphereSurface(R)),
        tangentPlaneTrace(center, eU, eV, Math.max(1.2 * indicatrixRadius, 0.35 * R)),
        curveTrace("индикатриса: окружность X^2+Y^2=R", tangentCurve(center, eU, eV, circleXY), "#7b2cbf", 9),
        markerTrace("точка u=v=pi/4", center),
        lineTrace("нормаль", center, add(center, scale(normal, 0.45 * Math.max(R, 1))))
      ];

      Plotly.react(
        "spherePlot",
        traces,
        sceneLayout("Сфера: индикатриса Дюпена является окружностью", { eye: { x: 1.55, y: -1.8, z: 1.1 } }),
        CONFIG
      );
    }

    function buildCylinderSurface(a, halfHeight) {
      const us = linspace(-halfHeight, halfHeight, 80);
      const vs = linspace(0, 2 * PI, 130);
      const x = [];
      const y = [];
      const z = [];
      for (const u of us) {
        const rowX = [];
        const rowY = [];
        const rowZ = [];
        for (const v of vs) {
          rowX.push(a * Math.cos(v));
          rowY.push(a * Math.sin(v));
          rowZ.push(u);
        }
        x.push(rowX);
        y.push(rowY);
        z.push(rowZ);
      }
      return { x, y, z };
    }

    function renderCylinder() {
      const a = num("cylinderA");
      const u0 = num("cylinderU");
      const v0 = num("cylinderV");
      const halfHeight = Math.max(num("cylinderH"), Math.abs(u0) + 0.8);
      setOut("cylinderAValue", a);
      setOut("cylinderUValue", u0);
      setOut("cylinderVValue", v0);
      setOut("cylinderHValue", halfHeight);

      const center = [a * Math.cos(v0), a * Math.sin(v0), u0];
      const eCirc = [-Math.sin(v0), Math.cos(v0), 0];
      const eAxis = [0, 0, 1];
      const normal = [Math.cos(v0), Math.sin(v0), 0];

      const x0 = Math.sqrt(a);
      const lineLength = Math.max(1.4, 0.38 * halfHeight + 0.9);
      const ts = linspace(-lineLength, lineLength, 90);
      const line1 = tangentCurve(center, eCirc, eAxis, ts.map((t) => [x0, t]));
      const line2 = tangentCurve(center, eCirc, eAxis, ts.map((t) => [-x0, t]));

      const traces = [
        surfaceTrace("цилиндр: полный оборот 0..2pi", buildCylinderSurface(a, halfHeight)),
        tangentPlaneTrace(center, eCirc, eAxis, Math.max(lineLength, x0 * 1.35)),
        curveTrace("индикатриса: две параллельные прямые", line1, "#006d77", 8),
        curveTrace("индикатриса: вторая прямая", line2, "#006d77", 8),
        markerTrace("произвольная точка", center),
        lineTrace("нормаль", center, add(center, scale(normal, 0.7 * Math.max(a, 1))))
      ];

      Plotly.react(
        "cylinderPlot",
        traces,
        sceneLayout("Цилиндр: параболический случай, одна кривизна равна нулю", { eye: { x: 1.8, y: -1.65, z: 1.25 } }),
        CONFIG
      );
    }

    function buildParaboloidSurface(A, B, domain) {
      const xs = linspace(-domain, domain, 95);
      const ys = linspace(-domain, domain, 95);
      const gridX = [];
      const gridY = [];
      const gridZ = [];
      for (const y of ys) {
        const rowX = [];
        const rowY = [];
        const rowZ = [];
        for (const x of xs) {
          rowX.push(x);
          rowY.push(y);
          rowZ.push(A * x * x + B * y * y);
        }
        gridX.push(rowX);
        gridY.push(rowY);
        gridZ.push(rowZ);
      }
      return { x: gridX, y: gridY, z: gridZ };
    }

    function renderParaboloid() {
      const A = num("paraboloidA");
      const B = num("paraboloidB");
      const domain = num("paraboloidD");
      setOut("paraboloidAValue", A);
      setOut("paraboloidBValue", B);
      setOut("paraboloidDValue", domain);

      const center = [0, 0, 0];
      const eX = [1, 0, 0];
      const eY = [0, 1, 0];
      const normal = [0, 0, 1];
      const semiX = 1 / Math.sqrt(2 * A);
      const semiY = 1 / Math.sqrt(2 * B);
      const ts = linspace(0, 2 * PI, 280);
      const ellipseXY = ts.map((t) => [semiX * Math.cos(t), semiY * Math.sin(t)]);

      const traces = [
        surfaceTrace("параболоид", buildParaboloidSurface(A, B, domain), paraboloidScale, 0.74),
        tangentPlaneTrace(center, eX, eY, Math.max(domain * 0.55, semiX * 1.45, semiY * 1.45)),
        curveTrace("индикатриса: 2A X^2+2B Y^2=1", tangentCurve(center, eX, eY, ellipseXY), "#b51700", 9),
        markerTrace("начало координат", center),
        lineTrace("нормаль", center, add(center, scale(normal, Math.max(0.45, 0.22 * domain * (A + B)))))
      ];

      Plotly.react(
        "paraboloidPlot",
        traces,
        sceneLayout("Параболоид: эллипс в касательной плоскости", { eye: { x: 1.65, y: -1.75, z: 1.15 } }),
        CONFIG
      );
    }

    function buildCatenoidSurface(uRange) {
      const us = linspace(-uRange, uRange, 110);
      const vs = linspace(0, 2 * PI, 140);
      const x = [];
      const y = [];
      const z = [];
      for (const u of us) {
        const rowX = [];
        const rowY = [];
        const rowZ = [];
        const cu = Math.cosh(u);
        for (const v of vs) {
          rowX.push(cu * Math.cos(v));
          rowY.push(cu * Math.sin(v));
          rowZ.push(u);
        }
        x.push(rowX);
        y.push(rowY);
        z.push(rowZ);
      }
      return { x, y, z };
    }

    function renderCatenoid() {
      const u0 = num("catenoidU");
      const v0 = num("catenoidV");
      const uRange = Math.max(num("catenoidRange"), Math.abs(u0) + 0.4);
      setOut("catenoidUValue", u0);
      setOut("catenoidVValue", v0);
      setOut("catenoidRangeValue", uRange);

      const cu = Math.cosh(u0);
      const su = Math.sinh(u0);
      const center = [cu * Math.cos(v0), cu * Math.sin(v0), u0];
      const eU = [su * Math.cos(v0) / cu, su * Math.sin(v0) / cu, 1 / cu];
      const eV = [-Math.sin(v0), Math.cos(v0), 0];
      const normal = [-Math.cos(v0) / cu, -Math.sin(v0) / cu, Math.tanh(u0)];

      const ts = linspace(-1.25, 1.25, 140);
      const s = cu;
      const branchA1 = tangentCurve(center, eU, eV, ts.map((t) => [s * Math.sinh(t), s * Math.cosh(t)]));
      const branchA2 = tangentCurve(center, eU, eV, ts.map((t) => [s * Math.sinh(t), -s * Math.cosh(t)]));
      const branchB1 = tangentCurve(center, eU, eV, ts.map((t) => [s * Math.cosh(t), s * Math.sinh(t)]));
      const branchB2 = tangentCurve(center, eU, eV, ts.map((t) => [-s * Math.cosh(t), s * Math.sinh(t)]));
      const planeSize = Math.max(1.7, 1.2 * s * Math.cosh(1.15));

      const traces = [
        surfaceTrace("катеноид: полный оборот 0..2pi", buildCatenoidSurface(uRange)),
        tangentPlaneTrace(center, eU, eV, planeSize),
        curveTrace("индикатриса: Y^2-X^2=cosh^2 u0", branchA1, "#2e7d32", 8),
        curveTrace("вторая ветвь", branchA2, "#2e7d32", 8),
        curveTrace("сопряженная гипербола", branchB1, "#7b2cbf", 8),
        curveTrace("вторая сопряженная ветвь", branchB2, "#7b2cbf", 8),
        markerTrace("произвольная точка", center),
        lineTrace("нормаль", center, add(center, scale(normal, 0.85)))
      ];

      Plotly.react(
        "catenoidPlot",
        traces,
        sceneLayout("Катеноид: гиперболическая индикатриса", { eye: { x: 1.65, y: -1.9, z: 1.1 } }),
        CONFIG
      );
    }

    function bind(ids, render) {
      ids.forEach((id) => {
        const input = document.getElementById(id);
        input.addEventListener("input", render);
      });
    }

    document.addEventListener("DOMContentLoaded", () => {
      bind(["sphereR"], renderSphere);
      bind(["cylinderA", "cylinderU", "cylinderV", "cylinderH"], renderCylinder);
      bind(["paraboloidA", "paraboloidB", "paraboloidD"], renderParaboloid);
      bind(["catenoidU", "catenoidV", "catenoidRange"], renderCatenoid);

      renderSphere();
      renderCylinder();
      renderParaboloid();
      renderCatenoid();
    });
  </script>
</body>
</html>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        HTML.replace("__PLOTLY_JS__", get_plotlyjs()),
        encoding="utf-8",
    )
    print(f"Saved interactive Dupin indicatrix visualizations to {OUT}")


if __name__ == "__main__":
    main()
