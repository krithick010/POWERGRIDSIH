/**
 * API client for POWERGRID ticketing system
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface Ticket {
  id: string
  source: string
  employee: string
  subject: string
  description: string
  priority: "low" | "medium" | "high"
  category: "network" | "access" | "hardware" | "software" | "other"
  assigned_team: string | null
  status: "open" | "in_progress" | "resolved"
  created_at: string
  updated_at: string
}

export interface KBArticle {
  id: string
  title: string
  content: string
  category: string
  views?: number
  helpful_count?: number
  relevance_score?: number
}

export interface ChatbotResponse {
  response: string
  ticket_created: boolean
  ticket_id?: string
  kb_suggestions: KBArticle[]
  auto_resolved: boolean
}

export const api = {
  async sendChatMessage(message: string, employee: string): Promise<ChatbotResponse> {
    const response = await fetch(`${API_URL}/chatbot`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, employee }),
    })

    if (!response.ok) {
      throw new Error("Failed to send message")
    }

    return response.json()
  },

  async getTickets(filters?: {
    employee?: string
    status?: string
    category?: string
  }): Promise<Ticket[]> {
    const params = new URLSearchParams()
    if (filters?.employee) params.append("employee", filters.employee)
    if (filters?.status) params.append("status", filters.status)
    if (filters?.category) params.append("category", filters.category)

    const response = await fetch(`${API_URL}/tickets?${params}`)

    if (!response.ok) {
      throw new Error("Failed to fetch tickets")
    }

    return response.json()
  },

  async getTicket(id: string): Promise<Ticket> {
    const response = await fetch(`${API_URL}/tickets/${id}`)

    if (!response.ok) {
      throw new Error("Failed to fetch ticket")
    }

    return response.json()
  },

  async searchKB(query: string): Promise<KBArticle[]> {
    const params = new URLSearchParams({ query, limit: "3" })
    const response = await fetch(`${API_URL}/kb/search?${params}`)

    if (!response.ok) {
      throw new Error("Failed to search knowledge base")
    }

    return response.json()
  },

  async updateTicketStatus(ticketId: string, status: "open" | "in_progress" | "resolved"): Promise<Ticket> {
    const response = await fetch(`${API_URL}/tickets/${ticketId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    })

    if (!response.ok) {
      throw new Error("Failed to update ticket status")
    }

    return response.json()
  },
}
