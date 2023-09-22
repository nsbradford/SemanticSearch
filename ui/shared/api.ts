import axios from "axios";
import { QueryFullAnswer, backendRootUrl } from "../components/Utils";
import { ChatCompletionRequestMessage } from "openai";

export interface LLMGetRequest {
  model: string;
  messages: ChatCompletionRequestMessage[];
}

export async function postQuery(
  userinput: string,
  catchFn: (error: any) => void
): Promise<QueryFullAnswer | undefined> {
  console.log('postQuery');
  try {
    const payload = { query: userinput };
    const url = backendRootUrl + '/query';
    console.log(`posting payload to "${url}`, payload);
    const response = await axios.post(url, payload);
    const data: QueryFullAnswer = response.data;
    console.log(`Response:`, data);
    return data;
  } catch (error) {
    catchFn(error);
  }
}


export async function sendLLMRequest(data: LLMGetRequest): Promise<string> {
  try {
    const response = await axios.post<string>('http://localhost:8000/llm/', data);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to send LLM request: ${error}`);
  }
}