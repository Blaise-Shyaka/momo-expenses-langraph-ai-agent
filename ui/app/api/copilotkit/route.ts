import {
  CopilotRuntime,
  GoogleGenerativeAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
  LangGraphAgent
} from '@copilotkit/runtime';
import { NextRequest } from 'next/server';

const serviceAdapter = new GoogleGenerativeAIAdapter({ model: 'gemini-2.0-flash' });
const runtime = new CopilotRuntime({
  agents: { 
    'chat': new LangGraphAgent({
      deploymentUrl: "http://localhost:8123",
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
