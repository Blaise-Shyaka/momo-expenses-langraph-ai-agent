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
          title: "Expenses Tracker",
          initial: "Hi! 👋 I'm Reddington. I can help you log your expenses, categorize them by category type, and get reports.",
        }}
      />
      <div>Hi</div>
    </CopilotKit> 
  );
}
