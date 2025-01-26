"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { FEATURES } from "@/components/landingPage/data";

gsap.registerPlugin(ScrollTrigger);

export default function Features() {
  const containerRef = useRef(null);

  useEffect(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: "figure",
        start: "top bottom",
        end: "top 60%",
        scrub: 1,
        // markers: true,
        toggleActions: "start pause reverse reset",
      },
    });
    tl.from("figure", { right: "-45%", bottom: "-45%" });
  }, []);
  return (
    <div ref={containerRef} className="w-full flex flex-col items-center">
      <h1 className="text-[2.5rem] font-semibold">
        Understand and learn at ease
      </h1>
      <p className=" text-muted-foreground">
        From key takeaways to specific questions, we’ve got you covered.
      </p>

      <div className="flex w-[70%] min-h-[40rem] py-8 mt-12 bg-muted border-2 border-border rounded-2xl overflow-hidden relative">
        <div className="w-2/5 px-6 space-y-4">
          <h2 className="font-medium text-xl">
            Chat, Summary, Chapters, and more.
          </h2>
          <p className="text-muted-foreground">
            Ask any question, grasp the key points, and receive specific notes.
          </p>
        </div>
        <figure className="w-full rounded-2xl overflow-hidden absolute right-[-40%] bottom-[-10%]">
          <Image src="/bg.png" alt="Product demo" width={2048} height={1024} />
        </figure>
      </div>

      <div className="w-[70%] grid grid-cols-3 gap-6">
        {FEATURES.map((feature, idx) => (
          <div
            key={idx}
            className="1/3 flex flex-col px-8 py-10 mt-6 bg-muted border-2 border-border rounded-2xl space-y-3"
          >
            <h2 className="text-xl font-medium">{feature.title}</h2>
            <p className="text-muted-foreground">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
