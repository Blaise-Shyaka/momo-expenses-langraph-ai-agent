import {
  CopilotRuntime,
  GoogleGenerativeAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
  LangGraphAgent
} from '@copilotkit/runtime';
import { NextRequest } from 'next/server';

const serviceAdapter = new GoogleGenerativeAIAdapter({ model: 'gemini-2.0-flash' });
const deploymentUrl = process.env.AGENT_URL || ""
console.log('deploymentUrl', deploymentUrl)
const runtime = new CopilotRuntime({
  agents: { 
    'chat': new LangGraphAgent({
      deploymentUrl,
      graphId: 'chat',
    }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: '/api/copilotkit',
  });
  return handleRequest(req);
};
