"use client"

import { useState } from "react"
import { Dashboard } from "@/components/dashboard"
import { Chatbot } from "@/components/chatbot"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { User, Sparkles, Zap } from "lucide-react"
import { motion } from "framer-motion"

export default function Home() {
  const [employee, setEmployee] = useState("")
  const [showDashboard, setShowDashboard] = useState(false)

  const handleLogin = () => {
    if (employee.trim()) {
      setShowDashboard(true)
    }
  }

  if (showDashboard) {
    return (
      <>
        <Dashboard employee={employee} />
        <Chatbot employee={employee} />
      </>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="max-w-md w-full"
      >
        <Card className="border-border/50 shadow-xl bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center space-y-4 pt-8 pb-6">
            <motion.div
              initial={{ y: -10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg"
            >
              <Zap className="h-8 w-8 text-white" />
            </motion.div>
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              POWERGRID
            </CardTitle>
            <p className="text-muted-foreground text-sm font-medium">AI-Powered IT Support System</p>
          </CardHeader>
          <CardContent className="space-y-5 pb-8">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Employee ID</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Enter your employee ID..."
                  value={employee}
                  onChange={(e) => setEmployee(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleLogin()}
                  className="pl-10 h-11 border-border focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                />
              </div>
            </div>

            <Button
              onClick={handleLogin}
              disabled={!employee.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold h-11 shadow-md hover:shadow-lg transition-all duration-200"
            >
              <Sparkles className="h-4 w-4 mr-2" />
              Enter Dashboard
            </Button>

            <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
              <div className="w-1.5 h-1.5 rounded-full bg-green-500"></div>
              <span>Secure • AI-Enhanced • Real-time Support</span>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
