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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full"
      >
        <Card className="glass border-white/20 shadow-2xl">
          <CardHeader className="text-center pb-8">
            <motion.div
              initial={{ y: -20 }}
              animate={{ y: 0 }}
              className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4"
            >
              <Zap className="h-8 w-8 text-white" />
            </motion.div>
            <CardTitle className="text-3xl font-bold text-white mb-2">
              POWERGRID
            </CardTitle>
            <p className="text-blue-100">AI-Powered IT Support System</p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white">Employee ID</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Enter your employee ID..."
                  value={employee}
                  onChange={(e) => setEmployee(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleLogin()}
                  className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-gray-300 focus:bg-white/20"
                />
              </div>
            </div>
            
            <Button
              onClick={handleLogin}
              disabled={!employee.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <Sparkles className="h-4 w-4 mr-2" />
              Enter Dashboard
            </Button>
            
            <div className="text-center text-xs text-blue-200">
              Secure • AI-Enhanced • Real-time Support
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
