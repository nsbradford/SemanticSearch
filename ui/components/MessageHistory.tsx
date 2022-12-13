import { faLink } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { QueryPassageAnswer, TypingIndicator } from './Utils';

// for "meaning of life" query

// example link: #:~:text=in the first couple weeks of working on their own startup they seem to come to life, because finally they're working

export function MessageHistory({
  messages,
  waiting,
}: {
  messages: QueryPassageAnswer[];
  waiting: boolean;
}) {
  const renderedMessages = messages.map((message: QueryPassageAnswer, i: number) => {
    // sad, highlight not working
    const url = `/doc/${message.document_id}#:~:text=${message.passage_text}`
    // whitespace-pre-line
    return (
      <li key={i} className="mx-4 my-3">
        <a className="font-thin text-violet-400" target="_blank" href={url} rel="noreferrer">{message.document_name}
        &nbsp;
        <FontAwesomeIcon icon={faLink} className="fa-fw" />
        </a> 
        <div className="outline outline-2 outline-slate-200 rounded-lg p-3 mt-1">
          <span className="font-thin text-gray-300">{message.before_text}</span>
          <span className="font-bold">{message.passage_text}</span>
          <span className="font-thin text-gray-300">{message.after_text}</span>
        </div>
      </li>
    );
  });

  return (
    <div className="flex place-content-center w-full p-2">
      <div className="w-full lg:w-3/4 mx-auto mt-2 mb-2 py-3 outline outline-2 outline-slate-200 rounded-lg ">
        <ul className="flex flex-col">{renderedMessages}</ul>
        {waiting && <TypingIndicator />}
      </div>
    </div>
  );
}
