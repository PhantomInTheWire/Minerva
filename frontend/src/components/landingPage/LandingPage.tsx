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
    </div>
  );
}
