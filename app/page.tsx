"use client"
import HeroSection from "@/components/hero-section"
import FeaturesSection from "@/components/features-section"
import UseCasesSection from "@/components/use-cases-section"
import CTASection from "@/components/cta-section"
import Header from "@/components/header"
import Footer from "@/components/footer"

export default function Page() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <UseCasesSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  )
}
