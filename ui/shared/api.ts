import axios from "axios";
import { QueryFullAnswer, backendRootUrl } from "../components/Utils";
import { ChatCompletionRequestMessage } from "openai";

export async function postQuery(
  userinput: string,
  catchFn: (error: any) => void
): Promise<QueryFullAnswer | undefined> {
  console.log('postQuery');
  try {
    const payload = { query: userinput };
    const url = backendRootUrl + '/query';
    console.log(`posting payload to "${url}`, payload);
    const response = await axios.post<QueryFullAnswer>(url, payload);
    const data = response.data;
    console.log(`Response:`, data);
    return data;
  } catch (error) {
    catchFn(error);
  }
}

export interface LLMChatCompletionRequest {
  model: string;
  messages: ChatCompletionRequestMessage[];
}


export async function sendLLMRequest(data: LLMChatCompletionRequest): Promise<string> {
  const response = await axios.post<{text: string}>(`${backendRootUrl}/llm/`, data);
  return response.data.text;
}