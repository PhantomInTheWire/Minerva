"use client";

import { useEffect } from "react";
import Link from "next/link";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const LINKS = [
  { title: "Home", href: "#home" },
  { title: "Features", href: "#features" },
  { title: "Use Cases", href: "#use-cases" },
  { title: "Pricing", href: "#pricing" },
];

export default function NavLinks() {
  useEffect(() => {
    const sections = document.querySelectorAll("section");
    const links = document.querySelectorAll(".nav-link");

    sections.forEach((section) => {
      ScrollTrigger.create({
        trigger: section,
        start: "top center",
        end: "bottom center",
        onEnter: () => setActiveLink(section.id),
        onEnterBack: () => setActiveLink(section.id),
        onLeave: () => setActiveLink(""), // Optional: Remove active class when out of view
      });
    });

    const setActiveLink = (id: string) => {
      links.forEach((link) => {
        if (link.getAttribute("href") === `#${id}`) {
          link.classList.add("text-foreground");
          link.classList.remove("text-muted-foreground");
        } else {
          link.classList.remove("text-foreground");
          link.classList.add("text-muted-foreground");
        }
      });
    };

    return () => {
      ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
    };
  }, []);

  return (
    <nav className="flex items-center gap-8">
      {LINKS.map((link, index) => (
        <Link
          href={link.href}
          key={index}
          className="nav-link font-medium text-muted-foreground hover:text-primary transition-all duration-300"
          //   text-[#6d6d6d] hover:text-[#121212]
        >
          {link.title}
        </Link>
      ))}
    </nav>
  );
}
