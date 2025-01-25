import { HeroSection, ScrollAnimatedContainer } from "@/components/ui";
import { Navbar } from "./Navbar";
import { ACTIONS } from "./data";

export default function LandingPage() {
  return (
    <div className="landing-page w-full min-h-screen flex flex-col">
      <Navbar />

      <HeroSection
        title="AI that works for you."
        subtitle="Transform your workflow with intelligent automation. Simple, powerful, reliable."
        actions={ACTIONS}
        titleClassName="text-5xl md:text-6xl font-extrabold"
        subtitleClassName="text-lg md:text-xl max-w-[600px]"
        actionsClassName="mt-8"
      />
      <section
        id="features"
        className="w-full flex flex-col items-center py-20"
      >
        <ScrollAnimatedContainer>
          <video autoPlay={true} loop muted className="roundex-3xl">
            <source src="./product-demo.mp4" type="video/mp4" />
          </video>
        </ScrollAnimatedContainer>
      </section>
    </div>
  );
}
