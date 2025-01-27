import { STEPS } from "./data";

export default function GettingStarted() {
  return (
    <>
      <h1 className="text-[2.5rem] font-semibold">Getting Started</h1>
      <p className=" text-muted-foreground">by following just 3 simple steps</p>
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
    </>
  );
}
