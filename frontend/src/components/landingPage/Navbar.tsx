import Image from "next/image";
import Link from "next/link";

const LINKS = [
  { title: "Home", href: "#home" },
  { title: "Features", href: "#features" },
  { title: "Use Cases", href: "#use-cases" },
  { title: "Pricing", href: "#pricing" },
];

export function Navbar() {
  return (
    <header className="w-full flex items-center justify-between px-12 py-3 border-b-2 border-[#f6f6f6]">
      <div className="flex items-center gap-8">
        <Link href="/">
          <figure>
            <Image src={"/logo.svg"} width={126} height={36} alt="Logo" />
          </figure>
        </Link>
        <nav className="flex items-center gap-8">
          {LINKS.map((link, index) => (
            <Link
              href={link.href}
              key={index}
              className="font-medium text-[#6d6d6d] hover:text-[#121212]"
            >
              {link.title}
            </Link>
          ))}
        </nav>
      </div>

      <button className="px-5 py-2 rounded-full text-[#f6f6f6] bg-[#121212] hover:bg-[#333333]">
        Get Started
      </button>
    </header>
  );
}
