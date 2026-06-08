import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CognitionOS — Behavioral Intelligence Portal",
  description: "Advanced AI Behavioral Intelligence System tracking cognitive load, digital drift, and emotional stability.",
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased bg-bg-darkest text-gray-100 min-h-screen relative">
        {/* Abstract Glow Assets for Aesthetics */}
        <div className="glow-blur bg-state-cognitive w-[400px] h-[400px] top-10 left-10 rounded-full"></div>
        <div className="glow-blur bg-state-recovery w-[500px] h-[500px] bottom-10 right-10 rounded-full"></div>
        
        {children}
      </body>
    </html>
  );
}
