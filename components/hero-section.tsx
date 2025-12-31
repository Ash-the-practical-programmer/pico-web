"use client"

import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function HeroSection() {
  return (
    <section className="relative py-32 sm:py-48 overflow-hidden">
      <div className="absolute inset-0 gradient-subtle -z-10" />
      <div className="absolute top-40 right-20 w-1 h-1 bg-primary/40 rounded-full" />
      <div className="absolute bottom-32 left-16 w-1.5 h-1.5 bg-secondary/30 rounded-full" />
      <div className="absolute top-1/3 right-1/4 w-0.5 h-0.5 bg-primary/20 rounded-full" />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="flex flex-col items-center text-center gap-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 border border-border rounded-full text-xs font-medium text-foreground bg-card/50 backdrop-blur-sm">
            <span className="text-secondary font-semibold">★</span>
            <span>Trusted by 500+ CV teams worldwide</span>
          </div>

          <div className="space-y-6 max-w-3xl">
            <h1 className="special-display font-serif text-5xl sm:text-6xl lg:text-7xl font-bold text-foreground leading-tight">
              Perfect datasets,
              <span className="text-secondary"> instantly</span>
            </h1>
            <p className="text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Generate high-quality labeled image datasets in minutes without expensive GPUs. CPU-first architecture
              means instant processing, lower costs, and production-ready results.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <Button
              size="lg"
              className="rounded-md px-8 bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition"
            >
              Start free
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="rounded-md px-8 border-border hover:border-primary hover:text-primary transition bg-transparent"
            >
              Watch demo
            </Button>
          </div>

          <div className="pt-16 border-t border-border w-full">
            <p className="text-xs sm:text-sm text-muted-foreground mb-8 font-medium">
              Trusted by leading computer vision teams
            </p>
            <div className="grid grid-cols-3 gap-8 sm:gap-12">
              <div className="flex flex-col items-center">
                <p className="text-2xl sm:text-3xl font-semibold text-primary">99.8%</p>
                <p className="text-xs sm:text-sm text-muted-foreground mt-2">Label Accuracy</p>
              </div>
              <div className="flex flex-col items-center">
                <p className="text-2xl sm:text-3xl font-semibold text-primary">100M+</p>
                <p className="text-xs sm:text-sm text-muted-foreground mt-2">Images Labeled</p>
              </div>
              <div className="flex flex-col items-center">
                <p className="text-2xl sm:text-3xl font-semibold text-primary">$0.99</p>
                <p className="text-xs sm:text-sm text-muted-foreground mt-2">Per 1K Images</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
