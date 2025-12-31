"use client"

import { Zap, Database, BarChart, Layers, Shield, Clock } from "lucide-react"

const features = [
  {
    icon: Zap,
    title: "Instant processing",
    description: "Generate labeled datasets in minutes with our optimized CPU-first architecture.",
  },
  {
    icon: Database,
    title: "Any image source",
    description: "Connect directly to your sources—S3, local uploads, URLs, or APIs.",
  },
  {
    icon: BarChart,
    title: "Real-time insights",
    description: "Monitor labeling progress and quality metrics in live dashboards.",
  },
  {
    icon: Layers,
    title: "Custom pipelines",
    description: "Build complex workflows with our intuitive no-code pipeline builder.",
  },
  {
    icon: Shield,
    title: "Enterprise security",
    description: "SOC 2 certified, end-to-end encryption, and granular access controls.",
  },
  {
    icon: Clock,
    title: "API-first design",
    description: "Integrate seamlessly via REST APIs and WebSocket for real-time updates.",
  },
]

export default function FeaturesSection() {
  return (
    <section id="features" className="py-24 sm:py-40 relative overflow-hidden">
      <div className="absolute inset-0 gradient-subtle -z-10" />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center space-y-4 mb-16">
          <h2 className="font-serif text-4xl sm:text-5xl font-bold italic text-foreground">Features for builders</h2>
          <p className="text-base text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Everything you need to create production-ready datasets without complexity.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div
                key={index}
                className="group rounded-lg border border-border bg-card p-6 hover:border-secondary hover:premium-shadow premium-hover"
              >
                <div className="w-10 h-10 rounded-md bg-secondary/10 flex items-center justify-center mb-4 group-hover:bg-secondary/20 transition">
                  <Icon className="w-5 h-5 text-secondary" />
                </div>
                <h3 className="text-lg font-semibold mb-2 text-foreground">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
