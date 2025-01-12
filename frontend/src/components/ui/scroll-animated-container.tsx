"use client";
import React, { useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export default function ScrollAnimatedContainer({
  children,
}: {
  children: React.ReactNode;
}) {
  useEffect(() => {
    // GSAP animation
    gsap.from(".window", {
      scrollTrigger: {
        trigger: ".window",
        start: "center 80%",
        end: "bottom center",
        scrub: true,
      },
      scale: 0.8,
      rotateX: 40,
      ease: "power2.out",
      transformStyle: "preserve-3d",
      // skewZ: -60,
      // transformOrigin: "bottom",
    });
  }, []);
  return (
    <div
      className="window w-4/5 rounded-2xl"
      style={{
        // width: "500px",
        // height: "200px",
        margin: "50px auto",
        background: "lightblue",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontSize: "24px",
        textAlign: "center",
      }}
    >
      {children}
    </div>
  );
}
