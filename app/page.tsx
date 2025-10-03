"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { MessageSquare, LayoutDashboard, Zap } from "lucide-react"
import { Chatbot } from "@/components/chatbot"
import { TicketDashboard } from "@/components/ticket-dashboard"

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [employee, setEmployee] = useState("")
  const [employeeInput, setEmployeeInput] = useState("")

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (employeeInput.trim()) {
      setEmployee(employeeInput.trim())
      setIsLoggedIn(true)
    }
  }

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-md p-8">
          <div className="flex items-center gap-2 mb-6">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Zap className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold">POWERGRID</h1>
              <p className="text-sm text-muted-foreground">IT Support Portal</p>
            </div>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="employee">Employee ID or Name</Label>
              <Input
                id="employee"
                value={employeeInput}
                onChange={(e) => setEmployeeInput(e.target.value)}
                placeholder="e.g., Rajesh Kumar (PG12345)"
                className="bg-input"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" placeholder="Enter your password" className="bg-input" disabled />
              <p className="text-xs text-muted-foreground">
                SSO integration placeholder - authentication not implemented
              </p>
            </div>

            <Button type="submit" className="w-full">
              Sign In
            </Button>

            <p className="text-xs text-center text-muted-foreground">
              For demo purposes, just enter your name to continue
            </p>
          </form>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Zap className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-lg font-bold">POWERGRID IT Support</h1>
              <p className="text-xs text-muted-foreground">AI-Powered Ticketing System</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <p className="text-sm text-muted-foreground hidden sm:block">{employee}</p>
            <Button variant="outline" size="sm" onClick={() => setIsLoggedIn(false)}>
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 container mx-auto p-4">
        <Tabs defaultValue="chatbot" className="h-full">
          <TabsList className="grid w-full max-w-md grid-cols-2 mb-4">
            <TabsTrigger value="chatbot" className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              AI Assistant
            </TabsTrigger>
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <LayoutDashboard className="w-4 h-4" />
              My Tickets
            </TabsTrigger>
          </TabsList>

          <TabsContent value="chatbot" className="h-[calc(100vh-200px)]">
            <Card className="h-full flex flex-col">
              <Chatbot employee={employee} />
            </Card>
          </TabsContent>

          <TabsContent value="dashboard" className="h-[calc(100vh-200px)]">
            <Card className="h-full">
              <TicketDashboard employee={employee} />
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
