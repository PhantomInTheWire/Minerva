"use client";
import React, { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export default function ScrollAnimatedContainer({
  children,
}: {
  children: React.ReactNode;
}) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = containerRef.current;
    if (!element) return;

    // Initial state - make sure it's visible but scaled down
    gsap.set(element, {
      // scale: 0.8,
      opacity: 0.8,
      // translateZ: ,
      rotateX: 60,
      scale: 0.6,
    });

    // Create the animation
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: element,
        start: "top bottom", // Starts animation when top of element hits bottom of viewport
        end: "80% 80%", // Ends animation when center of element hits center of viewport
        scrub: 0.5,
        toggleActions: "play none none reverse",
        markers: true, // Enable for debugging
        onEnter: () => console.log("enter"),
        onLeave: () => console.log("leave"),
        onEnterBack: () => console.log("enter back"),
        onLeaveBack: () => console.log("leave back"),
      },
    });

    // Add animations to timeline
    tl.to(element, {
      scale: 1,
      rotateX: 0,
      opacity: 1,
      duration: 1,
      ease: "power2.out",
    });

    // Cleanup
    return () => {
      tl.kill();
    };
  }, []);

  return (
    <div
      className="w-4/5 max-w-7xl rounded-3xl"
      style={{
        margin: "0 auto", // Increased margin to ensure enough scroll space
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        willChange: "transform", // Optimize for animations
        perspective: "1000px",
      }}
    >
      <div
        ref={containerRef}
        style={{
          transformOrigin: "bottom",
          // transition: "transform 0.ease",
        }}
      >
        {children}
      </div>
    </div>
  );
}
