import { QueryPassageAnswer } from "../components/Utils";


export function buildSummarizationPrompt(answers: QueryPassageAnswer[]) {
  const prompt = answers.map((answer) => {
    return `Document name: ${answer.document_name}
Passage: ${answer.passage_text}`;
  }).join('\n\n');
  return [{role: 'system' as const, content: `Please summarize the following passages, as CONCISELY as possible:\n\n${prompt}`}];
}