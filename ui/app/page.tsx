"use client";

import { CopilotKit, CopilotChat } from "@copilotkit/react-core/v2";
import { useSession } from "next-auth/react";
import { logout } from "@/lib/auth-client";

export default function Home() {
  const { data: session } = useSession();
  const runtimeUrl =
    typeof window !== "undefined"
      ? `${window.location.origin}/api/copilotkit`
      : "/api/copilotkit";

  return (
    <CopilotKit
      agent="chat"
      runtimeUrl={runtimeUrl}
      headers={
        session?.accessToken
          ? { Authorization: `Bearer ${session.accessToken}` }
          : {}
      }
    >
      <main
        className="flex justify-center items-center"
        style={{ height: "100dvh" }}
      >
        <CopilotChat
          labels={{
            welcomeMessageText:
              "Hi, I'm Reddington, an expense tracker. How can I help you today?",
          }}
          className="h-full rounded-2xl max-w-6xl mx-auto"
        >
          {({ scrollView, input }) => (
            <div
              style={{ display: "flex", flexDirection: "column", height: "100%" }}
            >
              <header
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "1rem",
                  borderBottom: "1px solid #e5e7eb",
                }}
              >
                <span
                  style={{
                    fontSize: "0.9375rem",
                    fontWeight: 500,
                    color: "#111827",
                    letterSpacing: "-0.01em",
                    fontFamily: "var(--font-geist-sans)",
                  }}
                >
                  ExpenseLog
                </span>
                <form action={logout}>
                  <button
                    type="submit"
                    style={{
                      padding: "0.375rem 0.75rem",
                      backgroundColor: "transparent",
                      border: "1px solid #d1d5db",
                      borderRadius: "6px",
                      color: "#6b7280",
                      fontSize: "0.75rem",
                      cursor: "pointer",
                      fontFamily: "var(--font-geist-sans)",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.border = "1px solid #9ca3af";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.border = "1px solid #d1d5db";
                    }}
                  >
                    Sign out
                  </button>
                </form>
              </header>
              {scrollView}
              {input}
            </div>
          )}
        </CopilotChat>
      </main>
    </CopilotKit>
  );
}
