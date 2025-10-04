"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, Clock, CheckCircle2, AlertCircle, Check } from "lucide-react"
import { api, type Ticket } from "@/lib/api"

interface TicketDashboardProps {
  employee: string
}

export function TicketDashboard({ employee }: TicketDashboardProps) {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [categoryFilter, setCategoryFilter] = useState<string>("all")
  const [resolvingTickets, setResolvingTickets] = useState<Set<string>>(new Set())

  useEffect(() => {
    loadTickets()
  }, [statusFilter, categoryFilter])

  const loadTickets = async () => {
    setIsLoading(true)
    try {
      const filters: any = { employee }
      if (statusFilter !== "all") filters.status = statusFilter
      if (categoryFilter !== "all") filters.category = categoryFilter

      const data = await api.getTickets(filters)
      setTickets(data)
    } catch (error) {
      console.error("Failed to load tickets:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const filteredTickets = tickets.filter(
    (ticket) =>
      ticket.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ticket.description.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-destructive text-destructive-foreground"
      case "medium":
        return "bg-chart-2 text-foreground"
      case "low":
        return "bg-muted text-muted-foreground"
      default:
        return "bg-secondary text-secondary-foreground"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "resolved":
        return <CheckCircle2 className="w-4 h-4 text-chart-3" />
      case "in_progress":
        return <Clock className="w-4 h-4 text-chart-2" />
      case "open":
        return <AlertCircle className="w-4 h-4 text-chart-1" />
      default:
        return null
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date)
  }

  const handleResolveTicket = async (ticketId: string) => {
    setResolvingTickets(prev => new Set([...prev, ticketId]))
    try {
      await api.updateTicketStatus(ticketId, "resolved")
      // Refresh tickets to show updated status
      await loadTickets()
    } catch (error) {
      console.error("Failed to resolve ticket:", error)
      // You could add a toast notification here if you have one set up
    } finally {
      setResolvingTickets(prev => {
        const newSet = new Set(prev)
        newSet.delete(ticketId)
        return newSet
      })
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-border space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search tickets..."
            className="pl-9 bg-input"
          />
        </div>

        <div className="flex gap-2">
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-[180px] bg-input">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="open">Open</SelectItem>
              <SelectItem value="in_progress">In Progress</SelectItem>
              <SelectItem value="resolved">Resolved</SelectItem>
            </SelectContent>
          </Select>

          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="w-[180px] bg-input">
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="network">Network</SelectItem>
              <SelectItem value="access">Access</SelectItem>
              <SelectItem value="hardware">Hardware</SelectItem>
              <SelectItem value="software">Software</SelectItem>
              <SelectItem value="other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-muted-foreground">Loading tickets...</div>
          </div>
        ) : filteredTickets.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <p className="text-muted-foreground">No tickets found</p>
              <p className="text-sm text-muted-foreground mt-1">Try adjusting your filters or search query</p>
            </div>
          </div>
        ) : (
          filteredTickets.map((ticket) => (
            <Card key={ticket.id} className="p-4 hover:bg-secondary/50 transition-colors">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    {getStatusIcon(ticket.status)}
                    <h3 className="font-medium text-sm truncate">{ticket.subject}</h3>
                  </div>

                  <p className="text-sm text-muted-foreground line-clamp-2 mb-3">{ticket.description}</p>

                  <div className="flex flex-wrap gap-2 mb-3">
                    <Badge className={getPriorityColor(ticket.priority)}>{ticket.priority}</Badge>
                    <Badge variant="outline">{ticket.category}</Badge>
                    <Badge variant="secondary">{ticket.status.replace("_", " ")}</Badge>
                  </div>

                  {ticket.status !== "resolved" && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleResolveTicket(ticket.id)
                      }}
                      disabled={resolvingTickets.has(ticket.id)}
                      className="text-xs"
                    >
                      {resolvingTickets.has(ticket.id) ? (
                        "Resolving..."
                      ) : (
                        <>
                          <Check className="w-3 h-3 mr-1" />
                          Mark as Resolved
                        </>
                      )}
                    </Button>
                  )}
                </div>

                <div className="text-right flex-shrink-0">
                  <p className="text-xs text-muted-foreground mb-1">{ticket.assigned_team}</p>
                  <p className="text-xs text-muted-foreground">{formatDate(ticket.created_at)}</p>
                  <p className="text-xs text-muted-foreground mt-1 font-mono">#{ticket.id.slice(0, 8)}</p>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
