import { faRotateRight } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import axios from 'axios';
import type { NextPage } from 'next';
import React from 'react';
import { HeadDefault } from '../components/HeadDefault';
import { InputForm } from '../components/InputForm';
import { MessageHistory } from '../components/MessageHistory';
import { backendRootUrl, QueryFullAnswer, QueryPassageAnswer } from '../components/Utils';

async function postQuery(
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

const PromptPage: NextPage = () => {
  const [answers, setAnswers] = React.useState<QueryPassageAnswer[]>([]);
  const [waiting, setWaiting] = React.useState(false);
  // const [userInput, setUserInput] = React.useState('');

  const handleNewUserPrompt = async (content: string) => {
    setWaiting(true);
    const serverResponseMsg = await postQuery(content, axiosCatchAll);
    console.log('Received response...', serverResponseMsg);
    if (serverResponseMsg) {
      setAnswers(serverResponseMsg.results);
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

        {(answers.length > 0 || waiting) && (
          <>
            <div className="flex place-content-center w-full">
              <button
                onClick={resetMessages}
                className="bg-slate-400 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded focus:outline-slate-400 disabled:bg-slate-200 shadow mx-1">
                <FontAwesomeIcon icon={faRotateRight} className="fa-fw" />
                Reset
              </button>
            </div>

            <MessageHistory messages={answers} waiting={waiting} />
          </>
        )}
      </main>
    </>
  );
};

export default PromptPage;
