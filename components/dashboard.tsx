"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Ticket, TrendingUp, Clock, CircleCheck as CheckCircle2, CircleAlert as AlertCircle, Search, RefreshCw, Plus, Users, Zap, ChartBar as BarChart3, Filter, ArrowUpRight } from "lucide-react"
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 relative">
      <div className="absolute inset-0 bg-grid-slate-200/30 [mask-image:radial-gradient(ellipse_at_top,transparent_10%,black)] pointer-events-none" />

      <div className="relative container-safe max-w-7xl space-y-6 p-6">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between flex-wrap gap-4 bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-border/50 shadow-sm"
        >
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl lg:text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                Support Dashboard
              </h1>
              <p className="text-sm text-muted-foreground mt-1">Welcome back, <span className="text-foreground font-medium">{employee}</span></p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={fetchTickets}
              variant="outline"
              size="sm"
              className="hover:bg-primary/5 hover:border-primary/50 transition-all"
            >
              <RefreshCw className={cn("h-4 w-4 mr-2", loading && "animate-spin")} />
              Refresh
            </Button>
            <Button size="sm" className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white shadow-md hover:shadow-lg transition-all">
              <Plus className="h-4 w-4 mr-2" />
              New Ticket
            </Button>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {[
            { title: "Total Tickets", value: stats.total, icon: Ticket, bgGradient: "from-blue-500 to-blue-600", bgSolid: "bg-blue-500", change: "+12%", changeColor: "text-emerald-600" },
            { title: "Open", value: stats.open, icon: AlertCircle, bgGradient: "from-red-500 to-red-600", bgSolid: "bg-red-500", change: "+3%", changeColor: "text-amber-600" },
            { title: "In Progress", value: stats.inProgress, icon: Clock, bgGradient: "from-amber-500 to-orange-600", bgSolid: "bg-amber-500", change: "+8%", changeColor: "text-emerald-600" },
            { title: "Resolved", value: stats.resolved, icon: CheckCircle2, bgGradient: "from-emerald-500 to-green-600", bgSolid: "bg-emerald-500", change: "+15%", changeColor: "text-emerald-600" },
          ].map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.06, type: "spring", stiffness: 100 }}
            >
              <Card className="relative overflow-hidden border-border/50 shadow-lg hover:shadow-2xl transition-all duration-300 bg-white/95 backdrop-blur-sm group cursor-pointer">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between mb-4">
                    <div className={cn("p-3 rounded-xl shadow-md group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 bg-gradient-to-br", stat.bgGradient)}>
                      <stat.icon className="h-5 w-5 text-white" />
                    </div>
                    <ArrowUpRight className="h-4 w-4 text-muted-foreground/50 group-hover:text-primary group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-muted-foreground uppercase tracking-wider">{stat.title}</p>
                    <p className="text-3xl font-black text-foreground">{stat.value}</p>
                    <div className="flex items-center gap-1.5 pt-1">
                      <TrendingUp className={cn("h-3.5 w-3.5", stat.changeColor)} />
                      <span className={cn("text-sm font-bold", stat.changeColor)}>{stat.change}</span>
                      <span className="text-xs text-muted-foreground">from last week</span>
                    </div>
                  </div>
                </CardContent>
                <div className={cn("absolute bottom-0 left-0 right-0 h-1 opacity-75 group-hover:opacity-100 transition-opacity", stat.bgSolid)} />
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.24 }}
        >
          <Card className="border-border/50 shadow-lg bg-white/95 backdrop-blur-sm">
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
          transition={{ delay: 0.3 }}
        >
          <Card className="border-border/50 shadow-lg bg-white/95 backdrop-blur-sm">
            <CardHeader className="border-b border-border/50 bg-slate-50/50">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center shadow-md">
                    <Ticket className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="flex items-center gap-2 text-xl">
                      Recent Tickets
                      <Badge variant="secondary" className="font-semibold">
                        {filteredTickets.length}
                      </Badge>
                    </CardTitle>
                    <CardDescription className="mt-1">
                      Track and manage your support requests
                    </CardDescription>
                  </div>
                </div>
                <Button variant="outline" size="sm" className="gap-2">
                  <BarChart3 className="h-4 w-4" />
                  View Analytics
                </Button>
              </div>
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
                        transition={{ delay: index * 0.03 }}
                        className="p-5 border-b border-border last:border-b-0 hover:bg-gradient-to-r hover:from-blue-50/50 hover:to-cyan-50/30 transition-all cursor-pointer group"
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
                            <Button variant="ghost" size="sm" className="hover:bg-primary/10 hover:text-primary transition-colors group-hover:translate-x-1 transition-transform">
                              View
                              <ArrowUpRight className="h-3 w-3 ml-1" />
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