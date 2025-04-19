"use client";

import { useChatStore } from "@/store/chat";
import { useEffect } from "react";
import { useShallow } from "zustand/shallow";
// import { chat } from "@/lib/db";

export default function Notebook({ notebookId }: { notebookId: string }) {
  const [messages] = useChatStore(useShallow((state) => [state.messages]));
  useEffect(() => {
    // chat();
  }, []);
  return (
    <div className="w-full flex flex-col items-center mt-20">
      <h1 className="text-2xl font-semibold">Chats</h1>
    </div>
  );
}
