"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui"; 

export default function Home() {
  return (
    <CopilotKit agent="chat" runtimeUrl="/api/copilotkit">
      <CopilotSidebar
        defaultOpen={true}
        clickOutsideToClose={false}
        labels={{
          title: "Travel Planner",
          initial: "Hi! 👋 I'm here to plan your trips. I can help you manage your trips, add places to them, or just generally work with you to plan a new one.",
        }}
      />
      <div>Hi</div>
    </CopilotKit> 
  );
}
