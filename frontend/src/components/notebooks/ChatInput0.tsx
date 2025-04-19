"use client";

import { useState } from "react";
import { ChatInput } from "@/components/ui/chat-input";
import { Button } from "@/components/ui/button";
import { Paperclip, Mic, CornerDownLeft } from "lucide-react";

export function AIChatInput() {
  const [value, setValue] = useState("");
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect?.(file);
    }
  };

  return (
    <div className="max-w-3xl min-w-[600px] p-4 flex flex-col items-center space-y-12 text-2xl font-semibold">
      <h2 className="text-center">Hi! How can I help you today?</h2>
      <form
        className="w-full relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1"
        onSubmit={(e) => {
          e.preventDefault();
          console.log("Submitted:", value);
        }}
      >
        <ChatInput
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Type your message here..."
          className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
        />
        <div className="flex items-center p-3 pt-0">
          <label className="cursor-pointer rounded-lg p-2 bg-black/5 dark:bg-white/5">
            <input type="file" className="hidden" onChange={handleFileChange} />
            <Paperclip className="size-4" />
          </label>
          {/* <Paperclip className="size-4" /> */}
          {/* <span className="sr-only">Attach file</span> */}

          <Button variant="ghost" size="icon" type="button">
            <Mic className="size-4" />
            <span className="sr-only">Use Microphone</span>
          </Button>

          <Button
            type="submit"
            variant="default"
            size="sm"
            className="ml-auto gap-1.5"
          >
            Send Message
            <CornerDownLeft className="size-3.5" />
          </Button>
        </div>
      </form>
    </div>
  );
}
