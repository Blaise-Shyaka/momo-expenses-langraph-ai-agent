"use client";

import { useEffect, useRef } from "react";
import { useSession } from "next-auth/react";

/**
 * Schedules a single refresh right before the access token expires, instead
 * of waiting for a request to notice it's already stale. auth.ts's jwt
 * callback has its own buffer and does the actual refresh decision — this
 * just makes sure something proactively asks, so a real user-facing request
 * essentially never has to.
 *
 * Deliberately single-tab only for now: this timer is per-tab, and multiple
 * tabs each running their own can still race each other. That's a known,
 * separate problem (needs cross-tab coordination, e.g. the Web Locks API) —
 * not solved here.
 */
export function SessionRefresh() {
  const { data: session, status, update } = useSession();
  const accessTokenExpires = session?.accessTokenExpires;
  const hasCheckedOnMount = useRef(false);

  // update()'s identity changes on every session/loading change (next-auth
  // internals) — depending on it directly re-arms these effects in a loop.
  const updateRef = useRef(update);
  useEffect(() => {
    updateRef.current = update;
  });

  // The scheduled timer below dies if the tab was closed past expiry —
  // check once on (re)visit instead of only trusting the carried-in session.
  useEffect(() => {
    if (status !== "authenticated" || hasCheckedOnMount.current) return;
    hasCheckedOnMount.current = true;
    updateRef.current();
  }, [status]);

  useEffect(() => {
    if (!accessTokenExpires) return;

    const REFRESH_MARGIN_MS = 60 * 1000;
    const delay = Math.max(0, accessTokenExpires - Date.now() - REFRESH_MARGIN_MS);

    const timer = setTimeout(() => {
      updateRef.current();
    }, delay);

    return () => clearTimeout(timer);
  }, [accessTokenExpires]);

  return null;
}
