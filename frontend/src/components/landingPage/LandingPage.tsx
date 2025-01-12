import Link from "next/link";
import Image from "next/image";
import { AnimatedGridPattern } from "../ui/grid-patterns";
import { cn } from "@/lib/utils";
import { Navbar } from "./Navbar";
import { Button } from "../ui/button";
// import { ContainerScroll } from "../ui/container-scroll-animation";
import ScrollAnimatedContainer from "../ui/scroll-animated-container";

export default function LandingPage() {
  return (
      <div className="landing-page w-full min-h-screen flex flex-col">
        <Navbar/>

        <section
            id="home"
            className="hero w-full h-[60vh] flex flex-col items-center"
        >
          <div className="w-full h-full flex flex-col items-center justify-center gap-20">
            <div className="flex flex-col">
              <h1 className="text-[5rem] font-semibold">Learning your way.</h1>
              <h2 className="text-xl text-center text-muted-foreground">
                Learn through the scientifically proven methods with the help of
                AI
              </h2>
            </div>
            <div className="flex gap-6">
              <Link
                  href="#features"
                  className="text-xl rounded-full px-6 py-2 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground transition-all duration-300"
              >
                See features
              </Link>
              <Button className="text-xl rounded-full px-6 py-6">
                Get Started
              </Button>
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
          </div>
        </section>
        <section
            id="features"
            className="w-full min-h-screen flex flex-col items-center pt-20" // Added min-height and padding
        >
          <ScrollAnimatedContainer>
            <Image
                src={`/window.png`}
                alt="hero"
                width={1600}
                height={781}
                className="mx-auto rounded-2xl object-contain h-full object-left-top"
                priority // Added priority loading
                draggable={false}
            />
          </ScrollAnimatedContainer>
        </section>
      </div>
  );
}
