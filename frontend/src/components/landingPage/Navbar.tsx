import Link from "next/link";
import { Button } from "../ui/button";
import Theme from "./Theme";
import Logo from "./Logo";

const LINKS = [
  { title: "Home", href: "#home" },
  { title: "Features", href: "#features" },
  { title: "Use Cases", href: "#use-cases" },
  { title: "Pricing", href: "#pricing" },
];

export function Navbar() {
  return (
    <header
      className="w-full flex items-center justify-between px-12 py-3 border-b-[1px] sticky top-0"
      style={{ backdropFilter: "blur(15px)" }}
    >
      {/* border-[#f6f6f6] */}
      <div className="flex items-center gap-8">
        <Link href="/">
          <Logo />
        </Link>
        <nav className="flex items-center gap-8">
          {LINKS.map((link, index) => (
            <Link
              href={link.href}
              key={index}
              className="font-medium text-muted-foreground hover:text-primary transition-all duration-300"
              //   text-[#6d6d6d] hover:text-[#121212]
            >
              {link.title}
            </Link>
          ))}
        </nav>
      </div>

      <div className="flex gap-8">
        <Theme />
        <Button className="rounded-full">Get Started</Button>
      </div>
    </header>
  );
}
