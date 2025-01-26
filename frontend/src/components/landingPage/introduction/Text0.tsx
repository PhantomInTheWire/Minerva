"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import RotatingText from "@/components/ui/rotating-text";

gsap.registerPlugin(ScrollTrigger);

export default function Text() {
  const containerRef = useRef(null);

  useEffect(() => {
    const paragraphs = containerRef.current.querySelectorAll(".paragraph");

    paragraphs.forEach((paragraph: Element) => {
      // Fade-in animation
      gsap.fromTo(
        paragraph,
        { opacity: 0 },
        {
          opacity: 1,
          scrollTrigger: {
            trigger: paragraph,
            start: "top 50%",
            end: "top 30%",
            scrub: 1,
            markers: true,
          },
        }
      );

      // Fade-out animation
      gsap.fromTo(
        paragraph,
        { opacity: 1 },
        {
          opacity: 0,
          scrollTrigger: {
            trigger: paragraph,
            start: "top 25%",
            end: "top 5%",
            scrub: 1,
            markers: true,
          },
        }
      );
    });
  }, []);

  return (
    <div
      ref={containerRef}
      className="bg-orange-300"
      style={{
        height: "140vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "20rem",
        padding: "0",
      }}
    >
      <div className="paragraph text-[3rem] text-center opacity-0">
        <RotatingText
          text="Do you find your learning resources"
          titles={[
            "boring",
            "uninteractive",
            "generic",
            "unsatisfying",
            "incomplete",
          ]}
        />
      </div>
      <p className="paragraph text-[3rem] text-center opacity-0">
        We heard you!
      </p>
      <p className="paragraph text-[3rem] text-center opacity-0">Introducing</p>
    </div>
  );
}
