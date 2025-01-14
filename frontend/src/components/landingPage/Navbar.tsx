import Link from "next/link";
import { Button } from "../ui/button";
import Theme from "./Theme";
import Logo from "./Logo";
import NavLinks from "./NavLinks";

export function Navbar() {
  return (
    <header className="w-full flex items-center justify-between px-12 py-3 border-b-[1px] sticky top-0 z-40 backdrop-blur-lg">
      {/* border-[#f6f6f6] */}
      <div className="flex items-center gap-8">
        <Link href="/">
          <Logo />
        </Link>
        <NavLinks />
      </div>

      <div className="flex gap-8">
        <Theme />
        <Button className="rounded-full">Get Started</Button>
      </div>
    </header>
  );
}
