"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-sm supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <span className="special-display text-2xl font-bold text-primary">pico</span>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="#features" className="text-sm font-medium text-foreground hover:text-primary transition">
              Features
            </Link>
            <Link href="#use-cases" className="text-sm font-medium text-foreground hover:text-primary transition">
              Use Cases
            </Link>
            <Link href="#" className="text-sm font-medium text-foreground hover:text-primary transition">
              Pricing
            </Link>
            <Link href="#" className="text-sm font-medium text-foreground hover:text-primary transition">
              Docs
            </Link>
          </nav>

          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" className="text-foreground hover:text-primary">
              Sign in
            </Button>
            <Button
              size="sm"
              className="rounded-full px-6 bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition"
            >
              Start free
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
