"use client";

import { useCallback, type ComponentProps } from "react";
import { CopilotKit, CopilotChat } from "@copilotkit/react-core/v2";
import { useSession } from "next-auth/react";
import { logout } from "@/lib/auth-client";

// CopilotKit's onError has no dedicated auth code, so match the 401 our
// agent raises for an expired token via status or message text.
const EXPIRED_TOKEN_PATTERN = /\b401\b/;

type CopilotErrorHandler = NonNullable<
  ComponentProps<typeof CopilotKit>["onError"]
>;

export default function Home() {
  const { data: session, update } = useSession();
  const runtimeUrl =
    typeof window !== "undefined"
      ? `${window.location.origin}/api/copilotkit`
      : "/api/copilotkit";
  const timezone =
    typeof window !== "undefined"
      ? Intl.DateTimeFormat().resolvedOptions().timeZone
      : undefined;

  // Last-resort recovery: try a refresh now, force logout only if that fails.
  const handleCopilotError = useCallback<CopilotErrorHandler>(
    async (event) => {
      const status = event.context?.response?.status;
      const message =
        typeof event.error === "string" ? event.error : event.error?.message;
      const looksLikeExpiredToken =
        status === 401 || EXPIRED_TOKEN_PATTERN.test(message ?? "");
      if (!looksLikeExpiredToken) return;

      const refreshed = await update();
      if (!refreshed || refreshed.error === "RefreshAccessTokenError") {
        await logout();
      }
    },
    [update]
  );

  return (
    <CopilotKit
      agent="chat"
      runtimeUrl={runtimeUrl}
      headers={
        session?.accessToken
          ? { Authorization: `Bearer ${session.accessToken}` }
          : {}
      }
      properties={timezone ? { timezone } : {}}
      onError={handleCopilotError}
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
