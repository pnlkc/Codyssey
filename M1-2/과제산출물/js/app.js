/**
 * AI Agent Assistant - Main Application Controller
 * UI 이벤트 오케스트레이션 및 상태 관리
 */

document.addEventListener("DOMContentLoaded", () => {
  // 전역 상태
  let currentConversationId = null;
  let chartInstance = null;
  let currentDataList = [];
  let editingDataId = null;

  // DOM 요소 캐시
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const serverStatusBadge = document.getElementById("serverStatusBadge");
  const coldstartBanner = document.getElementById("coldstartBanner");
  
  // 통계 요약 카드 요소
  const metricCount = document.getElementById("metricCount");
  const metricAverage = document.getElementById("metricAverage");
  const metricMax = document.getElementById("metricMax");
  const metricTotal = document.getElementById("metricTotal");
  const trendText = document.getElementById("trendText");
  const summaryPeriod = document.getElementById("summaryPeriod");

  // 채팅 요소
  const chatMessages = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const promptChips = document.getElementById("promptChips");
  const newChatBtn = document.getElementById("newChatBtn");
  const conversationList = document.getElementById("conversationList");

  // 데이터 관리 테이블 및 모달 요소
  const dataTableBody = document.getElementById("dataTableBody");
  const openAddModalBtn = document.getElementById("openAddModalBtn");
  const dataModal = document.getElementById("dataModal");
  const dataModalTitle = document.getElementById("dataModalTitle");
  const dataForm = document.getElementById("dataForm");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const cancelModalBtn = document.getElementById("cancelModalBtn");
  
  // 폼 인풋
  const inputDate = document.getElementById("inputDate");
  const inputValue = document.getElementById("inputValue");
  const inputMemo = document.getElementById("inputMemo");
  const inputCategory = document.getElementById("inputCategory");

  // 내보내기 버튼
  const exportCsvBtn = document.getElementById("exportCsvBtn");
  const exportJsonBtn = document.getElementById("exportJsonBtn");

  // 토스트 컨테이너
  const toastContainer = document.getElementById("toastContainer");

  // =========================================================================
  // 1. 테마 토글 (다크/라이트)
  // =========================================================================
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  themeToggleBtn.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    localStorage.setItem("theme", nextTheme);
    updateThemeIcon(nextTheme);
    if (chartInstance) chartInstance.render();
  });

  function updateThemeIcon(theme) {
    themeToggleBtn.innerHTML = theme === "dark" ? "☀️" : "🌙";
  }

  // =========================================================================
  // 2. 초기화 및 서버 헬스체크
  // =========================================================================
  async function initApp() {
    chartInstance = new window.TimeSeriesChart("timeSeriesChart");

    // 기본 오늘 날짜 폼에 세팅
    inputDate.value = new Date().toISOString().split("T")[0];

    // Swagger 링크 동적 설정
    const swaggerDocBtn = document.getElementById("swaggerDocBtn");
    if (swaggerDocBtn) {
      const isLocal = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1");
      swaggerDocBtn.href = isLocal ? "http://localhost:8000/docs" : "https://codyssey-m1-2.onrender.com/docs";
    }

    // 헬스체크 및 데이터 로드 병렬 수행
    checkServerHealth();
    await Promise.all([loadSummaryAndChart(), loadDataTable(), loadConversationList()]);
  }

  async function checkServerHealth() {
    try {
      const health = await window.ApiClient.checkHealth();
      serverStatusBadge.innerHTML = `<span class="status-dot"></span><span>API 온라인 (${health.ai_engine || "정상"})</span>`;
      if (coldstartBanner) coldstartBanner.style.display = "none";
    } catch (e) {
      serverStatusBadge.innerHTML = `<span class="status-dot loading"></span><span>서버 연결 중...</span>`;
      if (coldstartBanner) coldstartBanner.style.display = "flex";
    }
  }

  // =========================================================================
  // 3. 데이터 요약 & 차트 렌더링
  // =========================================================================
  async function loadSummaryAndChart() {
    try {
      const [summary, dataList] = await Promise.all([
        window.ApiClient.getDataSummary(),
        window.ApiClient.getDataList()
      ]);

      currentDataList = dataList;

      // 요약 지표 반영
      summaryPeriod.textContent = summary.period || "-";
      metricCount.textContent = `${summary.count.toLocaleString()}개`;
      metricAverage.textContent = `${summary.metrics.average.toLocaleString()}`;
      metricMax.textContent = `${summary.metrics.max.toLocaleString()}`;
      metricTotal.textContent = `${summary.metrics.total.toLocaleString()}`;
      trendText.textContent = summary.trend || "데이터 분석 완료";

      // 트렌드 아이콘/색상 동적 조정
      const trendBadgeBox = document.getElementById("trendBadgeBox");
      if (summary.trend.includes("상승")) {
        trendBadgeBox.style.borderLeft = "4px solid var(--badge-trend-up)";
      } else if (summary.trend.includes("하강")) {
        trendBadgeBox.style.borderLeft = "4px solid var(--badge-trend-down)";
      } else {
        trendBadgeBox.style.borderLeft = "4px solid var(--badge-trend-neutral)";
      }

      // 시계열 차트 갱신
      if (chartInstance) {
        chartInstance.setData(dataList);
      }
    } catch (error) {
      showToast("데이터 요약을 불러오는 중 오류가 발생했습니다.", "error");
    }
  }

  // =========================================================================
  // 4. 데이터 CRUD 테이블
  // =========================================================================
  async function loadDataTable() {
    try {
      const list = await window.ApiClient.getDataList(null, "desc");
      renderDataTable(list);
    } catch (e) {
      console.error(e);
    }
  }

  function renderDataTable(list) {
    dataTableBody.innerHTML = "";
    if (!list || list.length === 0) {
      dataTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:1.5rem;">등록된 데이터가 없습니다.</td></tr>`;
      return;
    }

    list.slice(0, 50).forEach((item) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${escapeHtml(item.date)}</strong></td>
        <td><span style="font-weight:700; color:var(--accent-primary);">${Number(item.value).toLocaleString()}</span></td>
        <td><span class="chip-btn" style="padding:0.15rem 0.5rem; font-size:0.7rem;">${escapeHtml(item.category || "일반")}</span></td>
        <td>${escapeHtml(item.memo || "-")}</td>
        <td class="table-actions">
          <button class="btn-table-action" onclick="window.editDataItem('${item.id}')">수정</button>
          <button class="btn-table-action delete" onclick="window.deleteDataItem('${item.id}')">삭제</button>
        </td>
      `;
      dataTableBody.appendChild(tr);
    });
  }

  // 데이터 추가 모달 열기
  openAddModalBtn.addEventListener("click", () => {
    editingDataId = null;
    dataModalTitle.textContent = "새 데이터 추가";
    dataForm.reset();
    inputDate.value = new Date().toISOString().split("T")[0];
    dataModal.classList.add("active");
  });

  // 데이터 수정 모달 열기 (전역 바인딩)
  window.editDataItem = async (id) => {
    const item = currentDataList.find((d) => d.id === id);
    if (!item) return;

    editingDataId = id;
    dataModalTitle.textContent = "데이터 수정";
    inputDate.value = item.date;
    inputValue.value = item.value;
    inputMemo.value = item.memo || "";
    inputCategory.value = item.category || "개발";
    dataModal.classList.add("active");
  };

  // 데이터 삭제 (전역 바인딩)
  window.deleteDataItem = async (id) => {
    if (!confirm("정말 이 데이터를 삭제하시겠습니까?")) return;
    try {
      await window.ApiClient.deleteData(id);
      showToast("데이터가 성공적으로 삭제되었습니다.");
      await Promise.all([loadSummaryAndChart(), loadDataTable()]);
    } catch (e) {
      showToast(`삭제 실패: ${e.message}`, "error");
    }
  };

  // 모달 닫기
  function closeModal() {
    dataModal.classList.remove("active");
    editingDataId = null;
  }
  closeModalBtn.addEventListener("click", closeModal);
  cancelModalBtn.addEventListener("click", closeModal);

  // 데이터 폼 제출 (추가 또는 수정)
  dataForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      date: inputDate.value,
      value: parseFloat(inputValue.value),
      memo: inputMemo.value,
      category: inputCategory.value
    };

    try {
      if (editingDataId) {
        await window.ApiClient.updateData(editingDataId, payload);
        showToast("데이터가 수정되었습니다.");
      } else {
        await window.ApiClient.createData(payload);
        showToast("새 데이터가 등록되었습니다.");
      }
      closeModal();
      await Promise.all([loadSummaryAndChart(), loadDataTable()]);
    } catch (err) {
      showToast(`저장 실패: ${err.message}`, "error");
    }
  });

  // =========================================================================
  // 5. AI 채팅 인터랙션
  // =========================================================================
  sendBtn.addEventListener("click", handleSendMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  // 추천 프롬프트 칩 클릭
  promptChips.addEventListener("click", (e) => {
    if (e.target.classList.contains("chip-btn")) {
      chatInput.value = e.target.textContent;
      handleSendMessage();
    }
  });

  // 새 대화 시작
  newChatBtn.addEventListener("click", () => {
    currentConversationId = null;
    chatMessages.innerHTML = "";
    appendAssistantMessage("안녕하세요! 데이터 분석 비서입니다. 궁금한 실적이나 추세에 대해 물어보세요! 😊");
    loadConversationList();
    showToast("새로운 대화 세션이 시작되었습니다.");
  });

  async function handleSendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = "";
    appendUserMessage(text);

    // 실시간 스트리밍을 위한 빈 어시스턴트 말풍선 생성
    const assistantBubble = document.createElement("div");
    assistantBubble.className = "message-bubble assistant";
    assistantBubble.innerHTML = `
      <div class="avatar">🤖</div>
      <div class="bubble-content"><span class="typing-cursor">▌</span></div>
    `;
    chatMessages.appendChild(assistantBubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const contentDiv = assistantBubble.querySelector(".bubble-content");
    let accumulatedText = "";

    try {
      await window.ApiClient.streamChatMessage(
        text,
        currentConversationId,
        [],
        // 1. 글자/청크 수신 시 즉시 렌더링
        (chunk) => {
          accumulatedText += chunk;
          contentDiv.innerHTML = `${formatMarkdown(accumulatedText)}<span class="typing-cursor">▌</span>`;
          chatMessages.scrollTop = chatMessages.scrollHeight;
        },
        // 2. 세션 메타데이터 수신 시
        (meta) => {
          if (meta.conversation_id) {
            currentConversationId = meta.conversation_id;
          }
        },
        // 3. 스트리밍 완료 시
        (done) => {
          if (done.conversation_id) {
            currentConversationId = done.conversation_id;
          }
          // 타이핑 커서 제거 및 최종 포맷 확정
          contentDiv.innerHTML = formatMarkdown(accumulatedText);
          loadConversationList();
        },
        // 4. 에러 발생 시
        (err) => {
          console.error("스트리밍 에러:", err);
          contentDiv.innerHTML = `⚠️ 오류가 발생했습니다: ${escapeHtml(err.message)}`;
        }
      );
    } catch (error) {
      contentDiv.innerHTML = `⚠️ 오류가 발생했습니다: ${escapeHtml(error.message)}`;
    }
  }

  function appendUserMessage(text) {
    const div = document.createElement("div");
    div.className = "message-bubble user";
    div.innerHTML = `
      <div class="avatar">👤</div>
      <div class="bubble-content"><p>${escapeHtml(text)}</p></div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendAssistantMessage(rawText) {
    const div = document.createElement("div");
    div.className = "message-bubble assistant";
    div.innerHTML = `
      <div class="avatar">🤖</div>
      <div class="bubble-content">${formatMarkdown(rawText)}</div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // =========================================================================
  // 6. 대화 세션 목록 및 불러오기
  // =========================================================================
  async function loadConversationList() {
    try {
      const convs = await window.ApiClient.getConversations();
      renderConversationList(convs);
    } catch (e) {
      console.error("대화 목록 로드 실패:", e);
    }
  }

  function renderConversationList(convs) {
    conversationList.innerHTML = "";
    if (!convs || convs.length === 0) {
      conversationList.innerHTML = `<div style="font-size:0.75rem; color:var(--text-muted); text-align:center; padding:1rem;">저장된 이전 대화가 없습니다.</div>`;
      return;
    }

    convs.forEach((c) => {
      const item = document.createElement("div");
      item.className = `conversation-item ${c.id === currentConversationId ? "active" : ""}`;
      item.innerHTML = `
        <div style="flex:1; cursor:pointer;" onclick="window.loadConversationDetail('${c.id}')">
          <div class="conv-title">${escapeHtml(c.title || "대화 세션")}</div>
          <div class="conv-date">${(c.updated_at || c.created_at || "").slice(0, 10)} (${c.message_count || 0}개)</div>
        </div>
        <button class="btn-delete-conv" title="삭제" onclick="window.deleteConversationItem(event, '${c.id}')">🗑️</button>
      `;
      conversationList.appendChild(item);
    });
  }

  // 대화 상세 불러오기 (전역 바인딩)
  window.loadConversationDetail = async (id) => {
    try {
      const conv = await window.ApiClient.getConversation(id);
      currentConversationId = conv.id;
      chatMessages.innerHTML = "";

      if (conv.messages && conv.messages.length > 0) {
        conv.messages.forEach((m) => {
          if (m.role === "user") appendUserMessage(m.content);
          else if (m.role === "assistant") appendAssistantMessage(m.content);
        });
      }
      loadConversationList();
      showToast("이전 대화를 불러왔습니다.");
    } catch (e) {
      showToast(`대화 불러오기 실패: ${e.message}`, "error");
    }
  };

  // 대화 삭제 (전역 바인딩)
  window.deleteConversationItem = async (e, id) => {
    e.stopPropagation();
    if (!confirm("이 대화 기록을 삭제하시겠습니까?")) return;
    try {
      await window.ApiClient.deleteConversation(id);
      if (currentConversationId === id) {
        currentConversationId = null;
        chatMessages.innerHTML = "";
        appendAssistantMessage("대화가 삭제되었습니다. 새 질문을 입력해 주세요!");
      }
      loadConversationList();
      showToast("대화가 삭제되었습니다.");
    } catch (err) {
      showToast(`삭제 실패: ${err.message}`, "error");
    }
  };

  // =========================================================================
  // 7. CSV / JSON 내보내기 (보너스 기능)
  // =========================================================================
  exportCsvBtn.addEventListener("click", () => {
    if (!currentDataList.length) return showToast("내보낼 데이터가 없습니다.", "error");
    let csv = "id,date,value,category,memo\n";
    currentDataList.forEach((d) => {
      csv += `"${d.id}","${d.date}",${d.value},"${d.category || ""}","${(d.memo || "").replace(/"/g, '""')}"\n`;
    });
    downloadFile(csv, `timeseries_data_${new Date().toISOString().slice(0, 10)}.csv`, "text/csv;charset=utf-8;");
    showToast("CSV 파일이 다운로드되었습니다.");
  });

  exportJsonBtn.addEventListener("click", () => {
    if (!currentDataList.length) return showToast("내보낼 데이터가 없습니다.", "error");
    const jsonStr = JSON.stringify(currentDataList, null, 2);
    downloadFile(jsonStr, `timeseries_data_${new Date().toISOString().slice(0, 10)}.json`, "application/json;charset=utf-8;");
    showToast("JSON 파일이 다운로드되었습니다.");
  });

  function downloadFile(content, fileName, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  }

  // =========================================================================
  // 8. 헬퍼 유틸리티
  // =========================================================================
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = "toast";
    if (type === "error") toast.style.borderLeftColor = "#ef4444";
    toast.innerHTML = `<span>${type === "error" ? "⚠️" : "✅"}</span><span>${escapeHtml(message)}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function formatMarkdown(text) {
    if (!text) return "";
    let html = escapeHtml(text);
    // 볼드
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    // 인라인 코드
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
    // 줄바꿈을 문단 및 br로
    const paragraphs = html.split("\n\n");
    return paragraphs.map((p) => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");
  }

  // 실행
  initApp();
});
