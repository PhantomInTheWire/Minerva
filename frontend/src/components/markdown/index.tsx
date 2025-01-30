"use client";

import { useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneLight,
  oneDark,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import "./styles.css";

export default function MarkdownRenderer(props: { theme?: "light" | "dark" }) {
  const [markdownInput, setMarkdownInput] = useState<string>("");
  const theme = props.theme ?? "dark";

  return (
    <div
      className={`w-full h-screen flex bg-background text-foreground theme-${theme}`}
    >
      <div className="w-1/2 h-full flex flex-col items-center relative border-r-[1px] border-border">
        <textarea
          className="w-full h-full outline-none px-4 py-4"
          value={markdownInput}
          onChange={(e) => setMarkdownInput(e.target.value)}
          placeholder="Enter Markdown here..."
        />
      </div>
      <div className="md w-1/2 h-full p-4 overflow-y-scroll">
        <Markdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex]}
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || ""); // Extracts the language name
              return !inline && match ? (
                <SyntaxHighlighter
                  style={theme === "light" ? oneLight : oneDark}
                  language={match[1]}
                  {...props}
                >
                  {String(children).trim()}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {markdownInput}
        </Markdown>
      </div>
    </div>
  );
}
