"use client"

import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function CTASection() {
  return (
    <section className="py-24 sm:py-40 relative overflow-hidden">
      <div className="absolute inset-0 gradient-subtle -z-10" />
      <div className="absolute top-20 left-10 w-1 h-1 bg-primary/30 rounded-full" />
      <div className="absolute bottom-20 right-16 w-1 h-1 bg-secondary/30 rounded-full" />

      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <h2 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold italic mb-6 text-foreground leading-tight">
          Ready to build <span className="text-secondary">better datasets?</span>
        </h2>
        <p className="text-base sm:text-lg text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
          Join 500+ computer vision teams creating production-ready datasets without expensive infrastructure or
          complexity.
        </p>

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            size="lg"
            className="rounded-md px-8 bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition"
          >
            Start for free
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="rounded-md px-8 border-border hover:border-primary hover:text-primary transition bg-transparent"
          >
            Schedule a demo
          </Button>
        </div>

        <p className="text-xs text-muted-foreground mt-8">
          No credit card required. Free tier includes 50,000 images per month.
        </p>
      </div>
    </section>
  )
}
