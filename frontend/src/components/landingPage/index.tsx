import { Navbar } from "./navbar";
import { ACTIONS } from "./data";
import Introduction from "./introduction";
import { HeroSection } from "./hero";
// import { MovingLogos } from "../ui";

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
        actionsClassName="mt-16"
      />
      <section id="features" className="w-full flex flex-col items-center">
        {/* Introduction */}
        <Introduction />

        {/* Moving logos */}
        {/* <motion.div
          initial={{ opacity: 0 }}
          viewport={{ once: true }}
          transition={{ ease: "easeInOut", delay: 1.8, duration: 0.8 }}
          whileInView={{ opacity: 1 }}
          className="mt-10 rounded-md flex flex-col antialiase dark:bg-grid-white/[0.05] items-center justify-center relative overflow-hidden space-y-4"
        >
          <p className="text-muted-foreground">
            Loved by top students all over the world
          </p>
          <MovingLogos items={UNIVERSITIES} direction="left" speed="normal" />
        </motion.div> */}
      </section>
    </div>
  );
}
