"use client"

import { CheckCircle2, TrendingUp } from "lucide-react"

const useCases = [
  {
    title: "Autonomous Vehicles",
    description: "Generate road scene datasets with precise labels for safer autonomous driving.",
    points: ["Object detection & tracking", "Lane segmentation", "Traffic sign classification"],
    impact: "3.2x faster dataset creation",
  },
  {
    title: "Medical Imaging",
    description: "Create annotated medical image datasets for pathology detection.",
    points: ["Lesion detection", "Anatomical segmentation", "Region classification"],
    impact: "99.9% accuracy maintained",
  },
  {
    title: "Retail & E-commerce",
    description: "Label product images for visual search, inventory, and quality control.",
    points: ["Product categorization", "Defect detection", "Visual attributes"],
    impact: "60% cost reduction",
  },
]

export default function UseCasesSection() {
  return (
    <section id="use-cases" className="py-24 sm:py-40 relative">
      <div className="absolute inset-0 gradient-subtle -z-10" />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center space-y-4 mb-16">
          <h2 className="font-serif text-4xl sm:text-5xl font-bold italic text-foreground">Built for real problems</h2>
          <p className="text-base text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Leading computer vision teams use Pico to accelerate their projects.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {useCases.map((useCase, index) => (
            <div
              key={index}
              className="rounded-lg border border-border bg-card p-6 hover:border-secondary hover:premium-shadow premium-hover group"
            >
              <div className="h-1 w-12 bg-secondary mb-6 group-hover:w-16 transition-all" />

              <h3 className="text-xl font-semibold mb-2 text-foreground">{useCase.title}</h3>
              <p className="text-sm text-muted-foreground mb-6 leading-relaxed">{useCase.description}</p>

              <div className="space-y-2 mb-6 pb-6 border-b border-border">
                {useCase.points.map((point, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-secondary flex-shrink-0 mt-0.5" />
                    <span className="text-sm font-medium text-foreground">{point}</span>
                  </div>
                ))}
              </div>

              <div className="flex items-start gap-2">
                <TrendingUp className="w-4 h-4 text-secondary flex-shrink-0 mt-0.5" />
                <span className="text-sm font-semibold text-primary">{useCase.impact}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
