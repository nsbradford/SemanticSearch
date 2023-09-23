import { QueryPassageAnswer } from "../components/Utils";


export function buildSummarizationPrompt(question: string, answers: QueryPassageAnswer[]) {
  const prompt = answers.map((answer) => {
    return `<passage>
Document name: ${answer.document_name}
Passage: ${answer.passage_text}
</passage>
`;

  }).join('\n\n');
  return [{
    role: 'system' as const, content: `Please try to answer the following question:
<question>
${question}
</question>

Use information ONLY from the following passages, as CONCISELY as possible:\n\n${prompt}`
  }];
}