import Link from "next/link";
import { AnimatedGridPattern } from "../ui/grid-patterns";
import { cn } from "@/lib/utils";
import { Navbar } from "./Navbar";
import { Button } from "../ui/button";
import ScrollAnimatedContainer from "../ui/scroll-animated-container";
// import AvatarCircles from "../ui/avatar-circles";
import { PEOPLE, WORDS } from "./data";
import { TypewriterEffect } from "../ui/typewriter-effect";
import { AnimatedTooltip } from "../ui/animated-tooltip";
import TypingAnimation from "../ui/typing-animation";

export default function LandingPage() {
  return (
    <div className="landing-page w-full min-h-screen flex flex-col">
      <Navbar />

      <section
        id="home"
        className="hero w-full h-[70vh] flex flex-col items-center"
      >
        <div className="w-full h-full flex flex-col items-center justify-end gap-20">
          <div className="flex flex-col items-center">
            {/* <TypewriterEffect words={WORDS} /> */}
            <TypingAnimation className="h-20 text-[3.5rem]">
              Learning your way with AI.
            </TypingAnimation>
            <h2 className="text-xl text-center text-muted-foreground">
              Learn through the scientifically proven methods with the help of
              AI
            </h2>
          </div>
          <div className="flex gap-6">
            <Link
              href="#features"
              className="nav-link text-xl rounded-full px-6 py-2 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground transition-all duration-300"
            >
              See features
            </Link>
            <Button className="text-xl rounded-full px-6 py-6">
              Get Started
            </Button>
          </div>

          <div className="flex flex-col items-center gap-2">
            {/* <AvatarCircles numPeople={999} avatarUrls={AVATARS} /> */}
            <AnimatedTooltip items={PEOPLE} />
            <p className="text-muted-foreground">Loved by 999+ learners</p>
          </div>
        </div>
        <AnimatedGridPattern
          numSquares={30}
          maxOpacity={0.1}
          duration={3}
          repeatDelay={1}
          className={cn(
            "[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]",
            "inset-x-0 inset-y-[-40%] h-[200%] skew-y-12 -z-10"
          )}
        />
      </section>
      <section
        id="features"
        className="w-full flex flex-col items-center pt-20"
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
