"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Send, Bot, User, Sparkles, MessageCircle, Zap, CircleCheck as CheckCircle, CircleAlert as AlertCircle, Info, ExternalLink, ThumbsUp, ThumbsDown, Copy, Minimize2, Maximize2 } from "lucide-react"
import { api, type KBArticle } from "@/lib/api"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  ticketId?: string
  kbSuggestions?: KBArticle[]
  autoResolved?: boolean
  timestamp: Date
}

interface ChatbotProps {
  employee: string
}

export function Chatbot({ employee }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: `Hello! I'm ARIA, your AI-powered IT support assistant. I'm here to help you with technical issues, answer questions, and create support tickets when needed. What can I help you with today?`,
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

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
      timestamp: new Date(),
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
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again or contact IT support at ext. 2222.",
        timestamp: new Date(),
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

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {!isMinimized ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="w-96 h-[650px] bg-white border border-gray-200/80 rounded-2xl shadow-2xl flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 via-blue-600 to-cyan-600 p-5 text-white relative overflow-hidden">
              <div className="absolute inset-0 bg-grid-white/[0.05] pointer-events-none" />
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className="absolute inset-0 bg-white/20 rounded-full blur-lg" />
                    <div className="relative w-10 h-10 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center border border-white/30">
                      <Bot className="h-5 w-5" />
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-400 rounded-full animate-pulse border-2 border-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">ARIA</h3>
                    <p className="text-xs text-blue-100 font-medium">AI Support Assistant • Online</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsMinimized(true)}
                  className="relative text-white hover:bg-white/20 h-9 w-9 p-0 rounded-full transition-all"
                >
                  <Minimize2 className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-slate-50 to-white">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className={cn(
                      "flex gap-3",
                      message.role === "user" ? "justify-end" : "justify-start"
                    )}
                  >
                    {message.role === "assistant" && (
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center shadow-md">
                          <Bot className="h-4 w-4 text-white" />
                        </div>
                      </div>
                    )}

                    <div className={cn(
                      "max-w-[85%] rounded-2xl p-3.5",
                      message.role === "user"
                        ? "bg-gradient-to-br from-blue-600 to-cyan-600 text-white ml-auto shadow-lg shadow-blue-500/20"
                        : "bg-white border border-gray-200/80 shadow-md"
                    )}>
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </p>
                      
                      <div className="flex items-center justify-between mt-2">
                        <span className={cn(
                          "text-xs",
                          message.role === "user" ? "text-blue-100" : "text-gray-500"
                        )}>
                          {formatTimestamp(message.timestamp)}
                        </span>
                        
                        {message.role === "assistant" && (
                          <div className="flex gap-1">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => copyToClipboard(message.content)}
                              className="h-6 w-6 p-0 text-gray-400 hover:text-gray-600"
                            >
                              <Copy className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-6 w-6 p-0 text-gray-400 hover:text-green-600"
                            >
                              <ThumbsUp className="h-3 w-3" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-6 w-6 p-0 text-gray-400 hover:text-red-600"
                            >
                              <ThumbsDown className="h-3 w-3" />
                            </Button>
                          </div>
                        )}
                      </div>

                      {/* Ticket Created Badge */}
                      {message.ticketId && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="mt-3 p-3 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-xl shadow-sm"
                        >
                          <div className="flex items-center gap-2 text-sm font-semibold text-green-800">
                            <CheckCircle className="h-4 w-4" />
                            <span>Ticket Created: #{message.ticketId.slice(0, 8)}</span>
                          </div>
                        </motion.div>
                      )}

                      {/* KB Suggestions */}
                      {message.kbSuggestions && message.kbSuggestions.length > 0 && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="mt-3 space-y-2"
                        >
                          <p className="text-xs font-medium text-gray-600 flex items-center gap-1">
                            <Info className="h-3 w-3" />
                            Helpful Articles:
                          </p>
                          {message.kbSuggestions.slice(0, 2).map((article) => (
                            <div
                              key={article.id}
                              className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200 rounded-xl cursor-pointer hover:shadow-md hover:border-blue-300 transition-all group"
                            >
                              <div className="flex items-center justify-between gap-2">
                                <p className="text-xs font-semibold text-blue-900 line-clamp-2 flex-1">
                                  {article.title}
                                </p>
                                <ExternalLink className="h-3.5 w-3.5 text-blue-600 flex-shrink-0 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                              </div>
                            </div>
                          ))}
                        </motion.div>
                      )}
                    </div>

                    {message.role === "user" && (
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-gradient-to-br from-slate-500 to-slate-700 rounded-full flex items-center justify-center shadow-md">
                          <User className="h-4 w-4 text-white" />
                        </div>
                      </div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>

              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center shadow-md">
                    <Bot className="h-4 w-4 text-white" />
                  </div>
                  <div className="bg-white border border-gray-200 rounded-2xl p-3.5 shadow-sm">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-gradient-to-t from-slate-50 to-white border-t border-gray-200">
              <div className="flex gap-2.5">
                <div className="flex-1 relative">
                  <Input
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me anything..."
                    disabled={isLoading}
                    className="pr-12 h-11 border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all bg-white shadow-sm"
                  />
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <Sparkles className="h-4 w-4 text-gray-400" />
                  </div>
                </div>
                <Button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 h-11 w-11 p-0 rounded-xl"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              
              <div className="flex items-center justify-center mt-3 text-xs text-muted-foreground">
                <div className="flex items-center gap-1.5 bg-white rounded-full px-3 py-1.5 border border-gray-200/50">
                  <Zap className="h-3 w-3 text-primary" />
                  <span className="font-medium">Powered by AI • Secure & Private</span>
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            onClick={() => setIsMinimized(false)}
            className="relative w-16 h-16 bg-gradient-to-br from-blue-600 via-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 flex items-center justify-center group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-white/0 to-white/10 rounded-full" />
            <MessageCircle className="relative h-7 w-7 group-hover:scale-110 transition-transform" />
            <div className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center shadow-lg animate-pulse">
              <span className="text-[10px] font-bold text-white">1</span>
            </div>
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  )
}
