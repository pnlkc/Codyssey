/**
 * AI Agent Assistant - API Client
 * 백엔드 REST API 통신 및 콜드스타트 감지
 */

const API_BASE = (window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1"))
  ? "" // 로컬 환경에서는 동일 호스트
  : (window.API_BASE_URL || "https://codyssey-m1-2.onrender.com"); // 프로덕션 배포 시 Render 백엔드 연결

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

  // --- AI Chat API ---
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
}

window.ApiClient = ApiClient;
