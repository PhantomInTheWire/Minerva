import { AIInputWithSearch } from "@/components/notebooks/ChatInput";
// import { AIChatInput } from "./ChatInput0";

export default function Notebooks() {
  return (
    <div className="w-full min-h-screen flex flex-col items-center py-16">
      {/* <AIChatInput /> */}
      <AIInputWithSearch
        title="Hi! How can I help you today?"
        className="space-y-8 py-16"
      />
    </div>
  );
}
