// "use client";
import { SparklesCore } from "@/components/ui/sparkles";
import Spline from "@splinetool/react-spline/next";
import { FloatingDockDemo } from "./navbar";

export default function Home() {
  return (
    <div className="w-full h-screen flex.flex-col">
      <SparklesCore
        id="tsparticlesfullpage"
        background="transparent"
        minSize={0.6}
        maxSize={1.4}
        particleDensity={100}
        className="w-full h-screen absolute -z-20"
        particleColor="#FFFFFF"
      />

      {/* Gradient */}
      <div className="fixed bottom-0 left-0 w-[700px] h-[1136px] -z-10">
        <div className="bg-[#622a9a] rounded-full filter blur-[224px] w-[569px] h-[569px] absolute -bottom-1/2 -left-1/2" />
        <div className="bg-[#602a9a] rounded-full filter blur-[735.3px] w-[1136px] h-[1136px] absolute -bottom-1/2 -left-1/2" />
      </div>

      <div className="hero w-full h-screen flex flex-col items-center">
        <div className="w-full h-[90%] flex items-center">
          <div className="w-1/2 flex flex-col items-center">
            <h1>Minerva</h1>

            <button className="bg-glow">Hello</button>
          </div>

          <div className="w-1/2 h-full">
            <Spline
              className="h-full"
              scene="https://prod.spline.design/TB8vmlwSl720CRd4/scene.splinecode"
            />
          </div>
        </div>
        <div className="">
          <FloatingDockDemo />
        </div>
      </div>
    </div>
  );
}
