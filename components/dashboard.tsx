"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Ticket, TrendingUp, Clock, CircleCheck as CheckCircle2, CircleAlert as AlertCircle, Search, RefreshCw, Plus, Users, Zap } from "lucide-react"
import { api, type Ticket as TicketType } from "@/lib/api"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"

interface DashboardProps {
  employee: string
}

export function Dashboard({ employee }: DashboardProps) {
  const [tickets, setTickets] = useState<TicketType[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    status: "all",
    category: "all",
    search: ""
  })

  // Stats data
  const stats = {
    total: tickets.length,
    open: tickets.filter(t => t.status === 'open').length,
    inProgress: tickets.filter(t => t.status === 'in_progress').length,
    resolved: tickets.filter(t => t.status === 'resolved').length,
  }

  const fetchTickets = async () => {
    setLoading(true)
    try {
      const data = await api.getTickets({ employee })
      setTickets(data)
    } catch (error) {
      console.error("Failed to fetch tickets:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTickets()
  }, [employee])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800'
      case 'low': return 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800'
      default: return 'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800'
      case 'in_progress': return 'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/20 dark:text-orange-300 dark:border-orange-800'
      case 'resolved': return 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800'
      default: return 'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'
    }
  }

  // Filter tickets based on current filters
  const filteredTickets = tickets.filter(ticket => {
    const matchesStatus = filters.status === "all" || ticket.status === filters.status
    const matchesCategory = filters.category === "all" || ticket.category === filters.category
    const matchesSearch = filters.search === "" || 
      ticket.subject.toLowerCase().includes(filters.search.toLowerCase()) ||
      ticket.description.toLowerCase().includes(filters.search.toLowerCase())
    
    return matchesStatus && matchesCategory && matchesSearch
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 p-6">
      <div className="container-safe max-w-7xl space-y-6">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between flex-wrap gap-4"
        >
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              POWERGRID IT Support
            </h1>
            <p className="text-muted-foreground mt-2 font-medium">Welcome back, <span className="text-foreground">{employee}</span></p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={fetchTickets}
              variant="outline"
              className="hover:bg-primary/5 hover:border-primary/50 transition-all"
            >
              <RefreshCw className={cn("h-4 w-4 mr-2", loading && "animate-spin")} />
              Refresh
            </Button>
            <Button className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white shadow-md hover:shadow-lg transition-all">
              <Plus className="h-4 w-4 mr-2" />
              New Ticket
            </Button>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {[
            { title: "Total Tickets", value: stats.total, icon: Ticket, color: "blue", bgColor: "bg-blue-500", change: "+12%" },
            { title: "Open", value: stats.open, icon: AlertCircle, color: "red", bgColor: "bg-red-500", change: "+3%" },
            { title: "In Progress", value: stats.inProgress, icon: Clock, color: "amber", bgColor: "bg-amber-500", change: "+8%" },
            { title: "Resolved", value: stats.resolved, icon: CheckCircle2, color: "emerald", bgColor: "bg-emerald-500", change: "+15%" },
          ].map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <Card className="relative overflow-hidden border-border/50 shadow-md hover:shadow-xl transition-all duration-300 bg-white/90 backdrop-blur-sm group cursor-pointer">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">{stat.title}</p>
                      <p className="text-4xl font-bold text-foreground">{stat.value}</p>
                      <div className="flex items-center gap-1">
                        <div className="flex items-center text-emerald-600 text-sm font-semibold">
                          <TrendingUp className="h-3.5 w-3.5 mr-1" />
                          {stat.change}
                        </div>
                        <span className="text-xs text-muted-foreground">vs last week</span>
                      </div>
                    </div>
                    <div className={cn("p-3 rounded-xl group-hover:scale-110 transition-transform shadow-lg", stat.bgColor)}>
                      <stat.icon className="h-6 w-6 text-white" />
                    </div>
                  </div>
                </CardContent>
                <div className={cn("absolute bottom-0 left-0 right-0 h-1", stat.bgColor)} />
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="border-border/50 shadow-md bg-white/90 backdrop-blur-sm">
            <CardContent className="p-5">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search tickets..."
                    className="pl-10 h-11 border-border focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                    value={filters.search}
                    onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                  />
                </div>
                <Select
                  value={filters.status}
                  onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}
                >
                  <SelectTrigger className="w-full md:w-[180px] h-11">
                    <SelectValue placeholder="All Statuses" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Statuses</SelectItem>
                    <SelectItem value="open">Open</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="resolved">Resolved</SelectItem>
                  </SelectContent>
                </Select>
                <Select
                  value={filters.category}
                  onValueChange={(value) => setFilters(prev => ({ ...prev, category: value }))}
                >
                  <SelectTrigger className="w-full md:w-[180px] h-11">
                    <SelectValue placeholder="All Categories" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="network">Network</SelectItem>
                    <SelectItem value="hardware">Hardware</SelectItem>
                    <SelectItem value="software">Software</SelectItem>
                    <SelectItem value="access">Access</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Tickets List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="border-border/50 shadow-md bg-white/90 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Ticket className="h-5 w-5" />
                Recent Tickets
                <Badge variant="secondary" className="ml-2">
                  {filteredTickets.length}
                </Badge>
              </CardTitle>
              <CardDescription>
                Track and manage your support requests
              </CardDescription>
            </CardHeader>
            <CardContent className="p-0">
              <div className="space-y-0">
                <AnimatePresence>
                  {filteredTickets.length === 0 ? (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="p-12 text-center text-muted-foreground"
                    >
                      <Ticket className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p className="text-lg font-medium mb-2">No tickets found</p>
                      <p className="text-sm">Try adjusting your filters or create a new ticket</p>
                    </motion.div>
                  ) : (
                    filteredTickets.slice(0, 10).map((ticket, index) => (
                      <motion.div
                        key={ticket.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        transition={{ delay: index * 0.04 }}
                        className="p-5 border-b border-border last:border-b-0 hover:bg-slate-50/50 transition-colors cursor-pointer"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="font-semibold line-clamp-1">
                                {ticket.subject}
                              </h3>
                              <Badge variant="outline" className={cn("text-xs", getPriorityColor(ticket.priority))}>
                                {ticket.priority}
                              </Badge>
                              <Badge variant="outline" className={cn("text-xs", getStatusColor(ticket.status))}>
                                {ticket.status.replace('_', ' ')}
                              </Badge>
                            </div>
                            <p className="text-sm text-muted-foreground line-clamp-2 mb-2">
                              {ticket.description}
                            </p>
                            <div className="flex items-center gap-4 text-xs text-muted-foreground">
                              <span>#{ticket.id.slice(0, 8)}</span>
                              <span className="capitalize">{ticket.category}</span>
                              <span>{new Date(ticket.created_at).toLocaleDateString()}</span>
                            </div>
                          </div>
                          <div className="ml-4">
                            <Button variant="ghost" size="sm" className="hover:bg-primary/10 hover:text-primary transition-colors">
                              View Details
                            </Button>
                          </div>
                        </div>
                      </motion.div>
                    ))
                  )}
                </AnimatePresence>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}