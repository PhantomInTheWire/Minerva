import { AnimatedGridPattern } from "../ui/grid-patterns";
import { cn } from "@/lib/utils";
import { Navbar } from "./Navbar";
import { Button } from "../ui/button";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="w-full h-screen flex flex-col">
      <Navbar />

      <div
        id="home"
        className="hero w-full h-screen flex flex-col items-center"
      >
        <div className="w-full h-[90%] flex flex-col items-center justify-center gap-20">
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
      <div id="features" className="w-full flex flex-col items-center">
        Features
      </div>
    </div>
  );
}
