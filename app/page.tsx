"use client"

import { useState } from "react"
import { Dashboard } from "@/components/dashboard"
import { Chatbot } from "@/components/chatbot"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { User, Sparkles, Zap, ArrowRight, Shield, Cpu, Headphones } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-slate-200/50 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)] pointer-events-none" />

      <div className="relative flex items-center justify-center min-h-screen p-4">
        <div className="max-w-6xl w-full grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
          {/* Left Side - Branding & Features */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-8 text-center lg:text-left"
          >
            <div className="space-y-4">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="inline-flex items-center justify-center lg:justify-start"
              >
                <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/20">
                  <Zap className="h-7 w-7 text-white" />
                </div>
              </motion.div>

              <div>
                <h1 className="text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 via-cyan-600 to-blue-600 bg-clip-text text-transparent mb-3">
                  POWERGRID
                </h1>
                <p className="text-xl text-muted-foreground font-medium">
                  AI-Powered IT Support System
                </p>
              </div>

              <p className="text-base text-muted-foreground max-w-md mx-auto lg:mx-0">
                Experience instant IT support with intelligent ticket management, automated resolutions, and 24/7 AI assistance.
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                { icon: Cpu, label: "AI-Powered", desc: "Smart automation" },
                { icon: Shield, label: "Secure", desc: "Enterprise grade" },
                { icon: Headphones, label: "24/7 Support", desc: "Always available" },
              ].map((feature, i) => (
                <motion.div
                  key={feature.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="flex flex-col items-center lg:items-start gap-2 p-4 rounded-xl bg-white/50 backdrop-blur-sm border border-border/50 hover:shadow-md transition-shadow"
                >
                  <feature.icon className="h-5 w-5 text-primary" />
                  <div>
                    <p className="font-semibold text-sm text-foreground">{feature.label}</p>
                    <p className="text-xs text-muted-foreground">{feature.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Right Side - Login Card */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="w-full max-w-md mx-auto"
          >
            <Card className="border-border/50 shadow-2xl bg-white/90 backdrop-blur-sm">
              <CardHeader className="space-y-2 pb-6">
                <CardTitle className="text-2xl font-bold">Welcome Back</CardTitle>
                <CardDescription className="text-base">
                  Enter your employee ID to access your dashboard
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Employee ID</label>
                  <div className="relative group">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
                    <Input
                      placeholder="e.g., EMP12345"
                      value={employee}
                      onChange={(e) => setEmployee(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && handleLogin()}
                      className="pl-10 h-12 border-border focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                      autoFocus
                    />
                  </div>
                </div>

                <Button
                  onClick={handleLogin}
                  disabled={!employee.trim()}
                  className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold h-12 shadow-lg hover:shadow-xl transition-all duration-200 group"
                >
                  <span>Access Dashboard</span>
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>

                <div className="pt-4 space-y-3">
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t border-border" />
                    </div>
                    <div className="relative flex justify-center text-xs">
                      <span className="bg-white px-2 text-muted-foreground">Trusted by employees</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-center gap-6 text-xs text-muted-foreground">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                      <span>System Online</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Shield className="h-3 w-3" />
                      <span>Secure Connection</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Help Text */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="text-center text-sm text-muted-foreground mt-6"
            >
              Need help? Contact IT Support at{" "}
              <span className="text-primary font-medium">ext. 2222</span>
            </motion.p>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
