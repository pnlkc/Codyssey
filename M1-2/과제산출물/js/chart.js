/**
 * AI Agent Assistant - Interactive Canvas Time-Series Chart
 * 외부 라이브러리 없는 순수 바닐라 HTML5 Canvas 기반 시계열 차트 렌더러
 */

class TimeSeriesChart {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.data = [];
    this.hoverIndex = -1;

    this.init();
  }

  init() {
    this.resize();
    window.addEventListener("resize", () => this.resize());

    // 마우스 호버 이벤트
    this.canvas.addEventListener("mousemove", (e) => this.handleMouseMove(e));
    this.canvas.addEventListener("mouseleave", () => {
      this.hoverIndex = -1;
      this.render();
    });
  }

  resize() {
    if (!this.canvas) return;
    const rect = this.canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = 260 * dpr;
    this.canvas.style.width = `${rect.width}px`;
    this.canvas.style.height = `260px`;
    this.ctx.scale(dpr, dpr);
    this.render();
  }

  setData(dataList) {
    // 날짜 오름차순 정렬
    this.data = [...dataList].sort((a, b) => (a.date > b.date ? 1 : -1));
    this.render();
  }

  handleMouseMove(e) {
    if (!this.data.length) return;
    const rect = this.canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;

    const padding = { left: 45, right: 25, top: 25, bottom: 35 };
    const chartWidth = rect.width - padding.left - padding.right;

    if (mouseX < padding.left || mouseX > rect.width - padding.right) {
      this.hoverIndex = -1;
      this.render();
      return;
    }

    const step = chartWidth / (this.data.length - 1 || 1);
    const index = Math.round((mouseX - padding.left) / step);

    if (index >= 0 && index < this.data.length && this.hoverIndex !== index) {
      this.hoverIndex = index;
      this.render();
    }
  }

  render() {
    if (!this.canvas || !this.ctx) return;
    const ctx = this.ctx;
    const rect = this.canvas.getBoundingClientRect();
    const width = rect.width;
    const height = 260;

    ctx.clearRect(0, 0, width, height);

    if (!this.data.length) {
      ctx.fillStyle = "#94a3b8";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("표시할 시계열 데이터가 없습니다.", width / 2, height / 2);
      return;
    }

    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    const padding = { left: 50, right: 30, top: 30, bottom: 35 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    const values = this.data.map((d) => Number(d.value) || 0);
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);
    const range = maxVal - minVal || 1;

    // 1. 그리드 라인 및 Y축 레이블
    ctx.strokeStyle = isDark ? "#1e293b" : "#f1f5f9";
    ctx.fillStyle = isDark ? "#64748b" : "#94a3b8";
    ctx.font = "11px sans-serif";
    ctx.textAlign = "right";

    const yTicks = 4;
    for (let i = 0; i <= yTicks; i++) {
      const yVal = minVal + (range / yTicks) * (yTicks - i);
      const yPos = padding.top + (chartHeight / yTicks) * i;

      ctx.beginPath();
      ctx.moveTo(padding.left, yPos);
      ctx.lineTo(width - padding.right, yPos);
      ctx.stroke();

      // 금액 표시 (예: 75,000원)
      const labelText = yVal >= 1000 ? `${Math.round(yVal).toLocaleString()}원` : `${Math.round(yVal)}`;
      ctx.fillText(labelText, padding.left - 8, yPos + 4);
    }

    // 2. 데이터 좌표 계산
    const stepX = chartWidth / (this.data.length - 1 || 1);
    const points = this.data.map((d, i) => {
      const x = padding.left + i * stepX;
      const val = Number(d.value) || 0;
      const y = padding.top + chartHeight - ((val - minVal) / range) * chartHeight;
      return { x, y, ...d };
    });

    // 3. 그라디언트 영역 채우기
    ctx.beginPath();
    ctx.moveTo(points[0].x, padding.top + chartHeight);
    for (let i = 0; i < points.length; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.lineTo(points[points.length - 1].x, padding.top + chartHeight);
    ctx.closePath();

    const gradient = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
    if (isDark) {
      gradient.addColorStop(0, "rgba(59, 130, 246, 0.35)");
      gradient.addColorStop(1, "rgba(59, 130, 246, 0.0)");
    } else {
      gradient.addColorStop(0, "rgba(37, 99, 235, 0.25)");
      gradient.addColorStop(1, "rgba(37, 99, 235, 0.0)");
    }
    ctx.fillStyle = gradient;
    ctx.fill();

    // 4. 메인 라인 그리기
    ctx.beginPath();
    ctx.strokeStyle = isDark ? "#60a5fa" : "#2563eb";
    ctx.lineWidth = 2.5;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    for (let i = 0; i < points.length; i++) {
      if (i === 0) ctx.moveTo(points[i].x, points[i].y);
      else ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.stroke();

    // 5. X축 주요 날짜 라벨 (처음, 중간, 끝)
    ctx.fillStyle = isDark ? "#64748b" : "#94a3b8";
    ctx.textAlign = "center";
    const xLabelsIndices = [0, Math.floor(points.length / 2), points.length - 1];
    xLabelsIndices.forEach((idx) => {
      if (points[idx]) {
        ctx.fillText(points[idx].date, points[idx].x, height - 10);
      }
    });

    // 6. 호버 하이라이트 및 툴팁
    if (this.hoverIndex >= 0 && this.hoverIndex < points.length) {
      const p = points[this.hoverIndex];

      // 세로 가이드라인
      ctx.beginPath();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = isDark ? "#94a3b8" : "#64748b";
      ctx.lineWidth = 1;
      ctx.moveTo(p.x, padding.top);
      ctx.lineTo(p.x, padding.top + chartHeight);
      ctx.stroke();
      ctx.setLineDash([]);

      // 포인트 원
      ctx.beginPath();
      ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#ffffff";
      ctx.fill();
      ctx.strokeStyle = "#2563eb";
      ctx.lineWidth = 3;
      ctx.stroke();

      // 툴팁 박스
      const categoryTag = p.category ? `[${p.category}] ` : "";
      const tooltipText = `${categoryTag}${p.date}: ${Number(p.value).toLocaleString()}원 (${p.memo || "거래"})`;
      ctx.font = "bold 11px sans-serif";
      const textWidth = ctx.measureText(tooltipText).width;
      const boxW = textWidth + 20;
      const boxH = 26;
      let boxX = p.x - boxW / 2;
      let boxY = p.y - 36;

      if (boxX < 10) boxX = 10;
      if (boxX + boxW > width - 10) boxX = width - boxW - 10;
      if (boxY < 10) boxY = p.y + 12;

      ctx.fillStyle = isDark ? "#1e293b" : "#0f172a";
      ctx.strokeStyle = isDark ? "#3b82f6" : "#2563eb";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(boxX, boxY, boxW, boxH, 4);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.textAlign = "left";
      ctx.fillText(tooltipText, boxX + 10, boxY + 17);
    }
  }
}

window.TimeSeriesChart = TimeSeriesChart;
