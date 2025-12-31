"use client"

import Link from "next/link"

export default function Footer() {
  return (
    <footer className="relative border-t border-border bg-background">
      <div className="absolute inset-0 gradient-subtle -z-10" />

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="space-y-3">
            <span className="special-display text-lg font-bold text-primary">pico</span>
            <p className="text-xs text-muted-foreground leading-relaxed">
              CPU-first image dataset generation for computer vision.
            </p>
          </div>

          {/* Product */}
          <div className="space-y-3">
            <h4 className="font-semibold text-foreground text-sm">Product</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Features
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Pricing
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  API
                </Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div className="space-y-3">
            <h4 className="font-semibold text-foreground text-sm">Company</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  About
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Blog
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Careers
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div className="space-y-3">
            <h4 className="font-semibold text-foreground text-sm">Legal</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Privacy
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Terms
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Security
                </Link>
              </li>
              <li>
                <Link href="#" className="text-muted-foreground hover:text-primary transition">
                  Compliance
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border pt-8 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-muted-foreground">
          <p>&copy; 2025 Pico. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="#" className="hover:text-primary transition">
              Twitter
            </Link>
            <Link href="#" className="hover:text-primary transition">
              GitHub
            </Link>
            <Link href="#" className="hover:text-primary transition">
              LinkedIn
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
