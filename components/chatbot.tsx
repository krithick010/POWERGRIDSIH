"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Send, Bot, User, Sparkles } from "lucide-react"
import { api, type KBArticle } from "@/lib/api"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  ticketId?: string
  kbSuggestions?: KBArticle[]
  autoResolved?: boolean
}

interface ChatbotProps {
  employee: string
}

export function Chatbot({ employee }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: `Hello! I'm the POWERGRID IT Support Assistant. I can help you with IT issues, answer questions, and create support tickets. How can I assist you today?`,
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await api.sendChatMessage(input, employee)

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        ticketId: response.ticket_id,
        kbSuggestions: response.kb_suggestions,
        autoResolved: response.auto_resolved,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again or contact IT support at ext. 2222.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            {message.role === "assistant" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                <Bot className="w-5 h-5 text-primary" />
              </div>
            )}

            <div className={`flex flex-col gap-2 max-w-[80%]`}>
              <Card className={`p-3 ${message.role === "user" ? "bg-primary text-primary-foreground" : "bg-card"}`}>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
              </Card>

              {message.autoResolved && (
                <Badge variant="secondary" className="w-fit">
                  <Sparkles className="w-3 h-3 mr-1" />
                  Auto-resolved
                </Badge>
              )}

              {message.ticketId && (
                <Badge variant="outline" className="w-fit">
                  Ticket ID: {message.ticketId.slice(0, 8)}
                </Badge>
              )}

              {message.kbSuggestions && message.kbSuggestions.length > 0 && (
                <div className="space-y-2 mt-2">
                  <p className="text-xs text-muted-foreground">Related articles:</p>
                  {message.kbSuggestions.map((article) => (
                    <Card
                      key={article.id}
                      className="p-3 bg-secondary/50 hover:bg-secondary cursor-pointer transition-colors"
                    >
                      <p className="text-sm font-medium">{article.title}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {article.category}
                        {article.relevance_score && (
                          <span className="ml-2">• {Math.round(article.relevance_score * 100)}% match</span>
                        )}
                      </p>
                    </Card>
                  ))}
                </div>
              )}
            </div>

            {message.role === "user" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-secondary flex items-center justify-center">
                <User className="w-5 h-5 text-foreground" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary animate-pulse" />
            </div>
            <Card className="p-3 bg-card">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:0.4s]" />
              </div>
            </Card>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-border p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe your IT issue..."
            disabled={isLoading}
            className="flex-1 bg-input"
          />
          <Button onClick={handleSend} disabled={!input.trim() || isLoading} size="icon">
            <Send className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-xs text-muted-foreground mt-2">Press Enter to send • Shift+Enter for new line</p>
      </div>
    </div>
  )
}
