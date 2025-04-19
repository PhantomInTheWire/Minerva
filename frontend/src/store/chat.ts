import { create } from "zustand";

type Sender = "user" | "ai" | "system";
type MessageParam = {
  content: string;
  sender: Sender;
  files: File[];
};
interface Message extends MessageParam {
  id: number;
}

// type TempChatStore = {
//   message: MessageParam;
//   isExecuted: boolean;
//   updateMessage: (newMessage: MessageParam) => void;
//   toggleExecuted: () => void;
// };
// const useTempChatStore = create<TempChatStore>((set) => ({
//   message: {
//     content: "",
//     sender: "system",
//     files: [],
//   },
//   isExecuted: false,
//   updateMessage: (newMessage: MessageParam) =>
//     set({
//       message: newMessage,
//     }),
//     toggleExecuted: () => set(state => ({
//         isExecuted: !state.isExecuted
//     }))
// }));

type ChatStore = {
  messages: Message[];
  addMessage: (newMessage: MessageParam) => void;
  isExecuted: boolean;
};
const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isExecuted: false,
  addMessage: (newMessage: MessageParam) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          id: state.messages.length + 1,
          ...newMessage,
        },
      ],
    })),
}));

export { useChatStore };
