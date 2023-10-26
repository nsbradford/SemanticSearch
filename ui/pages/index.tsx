import { faRotateRight } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import type { NextPage } from 'next';
import React from 'react';
import { HeadDefault } from '../components/HeadDefault';
import { InputForm } from '../components/InputForm';
import { MessageHistory } from '../components/MessageHistory';
import { QueryPassageAnswer, TypingIndicator } from '../components/Utils';
import { postQuery, sendLLMRequest } from '../shared/api';
import { getSessionId } from '../shared/utils';
import { buildSummarizationPrompt } from '../shared/prompts';

const PromptPage: NextPage = () => {
  const sessionId = getSessionId();
  const [answers, setAnswers] = React.useState<QueryPassageAnswer[]>([]);
  const [waiting, setWaiting] = React.useState(false);
  const [answerSummary, setAnswerSummary] = React.useState<string | null>(null);

  const handleNewUserPrompt = async (content: string) => {
    setWaiting(true);
    const serverResponseMsg = await postQuery(content, axiosCatchAll);
    console.log('Received response...', serverResponseMsg);
    if (serverResponseMsg) {
      setAnswers(serverResponseMsg.results);
      const llmSummary = await sendLLMRequest({ model: 'gpt-3.5-turbo', messages: buildSummarizationPrompt(content, serverResponseMsg.results), sessionId: sessionId })
      console.log('Received LLM response...', llmSummary);
      if (llmSummary) {
        setAnswerSummary(llmSummary);
      }

    }
    setWaiting(false);
  };

  const axiosCatchAll = async (error: any) => {
    console.log('axiosCatchAll', error);
    window.alert('Internal server error :( our engineers were alerted.');
    setWaiting(false);
  };

  const resetMessages = () => {
    setAnswers([]);
    setAnswerSummary(null);
    setWaiting(false);
  };

  return (
    <>
      <HeadDefault />

      <main>
        <div className="text-center">
          <h1 className="text-4xl m-5 mt-12">
            Semantic <span className="text-violet-400">Search</span>
          </h1>
        </div>

        <InputForm handleSubmit={handleNewUserPrompt} waiting={waiting} />

        {waiting && <TypingIndicator />}
        {answerSummary &&
          <div className="flex place-content-center w-full px-8">
            <div className="w-full lg:w-3/4 2xl:w-2/5 bg-gray-100 p-4 my-4 mx-auto rounded-lg shadow-lg">
              {"Summary: " + answerSummary}
            </div>
          </div>
        }


        {(answers.length > 0) && (
          <>
            <div className="flex place-content-center w-full mt-6">
              <button
                onClick={resetMessages}
                className="bg-slate-400 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded focus:outline-slate-400 disabled:bg-slate-200 shadow mx-1">
                <FontAwesomeIcon icon={faRotateRight} className="fa-fw" />
                Reset
              </button>
            </div>

            <MessageHistory messages={answers} /* waiting={waiting} */ />
          </>
        )}
      </main>
    </>
  );
};

export default PromptPage;
