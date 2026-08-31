/**
 * AI Agent Assistant - API Client
 * 백엔드 REST API 통신 및 콜드스타트 감지
 */

const API_BASE = (() => {
  if (window.API_BASE_URL) return window.API_BASE_URL;
  const isLocal = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1");
  if (isLocal) {
    // 8000번 포트(백엔드 통합 서빙)인 경우 상대경로, 별도 프론트엔드 포트(Live Server 등)인 경우 localhost:8000 백엔드로 연결
    return window.location.port === "8000" ? "" : "http://localhost:8000";
  }
  // Vercel 등 프로덕션 배포 시 Render 백엔드 기본 URL
  return "https://codyssey-m1-2.onrender.com";
})();

class ApiClient {
  /** 공통 fetch 래퍼 */
  static async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultHeaders = {
      "Content-Type": "application/json",
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        let errorMsg = `HTTP Error ${response.status}`;
        try {
          const errData = await response.json();
          errorMsg = errData.detail || errorMsg;
        } catch (_) {}
        throw new Error(errorMsg);
      }
      return await response.json();
    } catch (error) {
      console.error(`[API Error] ${endpoint}:`, error);
      throw error;
    }
  }

  // --- Health Check ---
  static async checkHealth() {
    return this.request("/api/health");
  }

  // --- Data APIs ---
  static async getDataSummary() {
    return this.request("/api/data/summary");
  }

  static async getDataList(limit = null, order = "asc") {
    const query = new URLSearchParams();
    if (limit) query.append("limit", limit);
    if (order) query.append("order", order);
    return this.request(`/api/data?${query.toString()}`);
  }

  static async createData(payload) {
    return this.request("/api/data", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  static async updateData(id, payload) {
    return this.request(`/api/data/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  }

  static async deleteData(id) {
    return this.request(`/api/data/${id}`, {
      method: "DELETE",
    });
  }

  static async reseedData() {
    return this.request("/api/data/reset-seed", {
      method: "POST",
    });
  }

  // --- Conversation APIs ---
  static async getConversations() {
    return this.request("/api/conversations");
  }

  static async getConversation(id) {
    return this.request(`/api/conversations/${id}`);
  }

  static async deleteConversation(id) {
    return this.request(`/api/conversations/${id}`, {
      method: "DELETE",
    });
  }

  // --- AI Chat API (단일 응답 & 실시간 SSE 스트리밍) ---
  static async sendChatMessage(message, conversationId = null, history = []) {
    return this.request("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        history,
      }),
    });
  }

  /** 실시간 SSE 글자/토큰 단위 스트리밍 호출 */
  static async streamChatMessage(message, conversationId = null, history = [], onChunk, onMeta, onDone, onError) {
    const url = `${API_BASE}/api/chat/stream`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
          history,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop(); // 아직 완료되지 않은 잔여 버퍼 보존

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith("data: ")) {
            try {
              const data = JSON.parse(trimmed.slice(6));
              if (data.type === "meta" && onMeta) {
                onMeta(data);
              } else if (data.type === "chunk" && onChunk) {
                onChunk(data.text);
              } else if (data.type === "done" && onDone) {
                onDone(data);
              }
            } catch (jsonErr) {
              // 파싱 실패 무시
            }
          }
        }
      }
    } catch (err) {
      if (onError) onError(err);
      else throw err;
    }
  }
}

window.ApiClient = ApiClient;
