import { AnimatedGridPattern } from "../ui/grid-patterns";
import { cn } from "@/lib/utils";
import { Navbar } from "./Navbar";

export default function LandingPage() {
  return (
    <div className="w-full h-screen flex flex-col">
      <Navbar />

      <div className="hero w-full h-screen flex flex-col items-center">
        <div className="w-full h-[90%] flex items-center">
          <div className="w-1/2 flex flex-col items-center">
            <h1>Minerva</h1>
          </div>

          <div className="w-1/2 h-full"></div>
        </div>
      </div>
      <AnimatedGridPattern
        numSquares={30}
        maxOpacity={0.1}
        duration={3}
        repeatDelay={1}
        className={cn(
          "[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]",
          "inset-x-0 inset-y-[-30%] h-[200%] skew-y-12"
        )}
      />
    </div>
  );
}
