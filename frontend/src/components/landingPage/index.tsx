import { Navbar } from "./navbar";
import { ACTIONS, STEPS, PRICES } from "./data";
import Introduction from "./introduction";
import { HeroSection } from "./hero";
import Features from "./features";
import { Button } from "../ui";
// import { MovingLogos } from "../ui";

export default function LandingPage() {
  return (
    <div className="landing-page w-full min-h-screen flex flex-col pb-20">
      <Navbar />

      <HeroSection
        title="AI that works for you."
        subtitle="Transform your workflow with intelligent automation. Simple, powerful, reliable."
        actions={ACTIONS}
        titleClassName="text-5xl md:text-6xl font-extrabold"
        subtitleClassName="text-lg md:text-xl max-w-[600px]"
        actionsClassName="mt-16"
      />
      <section
        id="features"
        className="w-full flex flex-col pt-20 pb-12 items-center"
      >
        {/* Introduction */}
        <Introduction />
        <Features />
      </section>

      <section
        id="getting-started"
        className="w-full flex flex-col items-center pt-20"
      >
        <h1 className="text-[2.5rem] font-semibold">Getting Started</h1>
        <p className=" text-muted-foreground">
          by following just 3 simple steps
        </p>
        <div className="w-[70%] grid grid-cols-3 gap-6 mt-12">
          {STEPS.map((step, idx) => (
            <div
              key={idx}
              className="1/3 flex flex-col px-8 py-10 bg-muted border-2 border-border rounded-2xl space-y-3"
            >
              <h2 className="text-xl font-medium">{step.title}</h2>
              <p className="text-muted-foreground">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="pricing" className="w-full flex flex-col items-center pt-20">
        <h1 className="text-[2.5rem] font-semibold">
          Save hours, learn smarter.
        </h1>
        <p className=" text-muted-foreground">
          Enjoy endless content uploads, chats, recorded lectures, and more.
        </p>
        <div className="w-[50%] flex justify-center gap-6 mt-12">
          {PRICES.map((price, idx) => (
            <div
              key={idx}
              className={`1/3 my-auto flex flex-col px-8 py-10 ${
                price.isPrimary ? "bg-foreground text-background" : "bg-muted"
              } border-2 border-border rounded-3xl space-y-3`}
            >
              <p>{price.title}</p>
              <p>
                <span className="text-[3rem] font-semibold">
                  &#8377;&nbsp;{price.price}
                </span>
                /month
              </p>
              <p className="text-muted-foreground">{price.desc}</p>
              <ul
                className={`border-t-2 mt-2 py-4 space-y-2 ${
                  price.isPrimary
                    ? "border-muted-foreground text-muted-foreground"
                    : "border-border text-"
                }`}
              >
                {price.features.map((feature, idx) => (
                  <li key={idx}>{feature}</li>
                ))}
              </ul>
              <Button
                variant={"default"}
                className={`rounded-full py-6 text-lg font-medium ${
                  price.isPrimary
                    ? "bg-background text-foreground hover:bg-muted"
                    : ""
                }`}
              >
                {price.button}
              </Button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
