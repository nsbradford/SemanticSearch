import styles from '../styles/Home.module.scss';
import { QueryPassageAnswer, TypingIndicator } from './Utils';


// https://github.com/react-syntax-highlighter/react-syntax-highlighter/issues/230
// https://github.com/react-syntax-highlighter/react-syntax-highlighter/issues/440
// function formatMessageContent(message: Message, language: string = 'text'): JSX.Element {
//   // TODO showing line numbers breaks word wrapping :(
//   const showLineNumbers = false; //message.messageType == MessageType.GPT3;
//   const wrapLongLines = true;
//   const typeAnnotation = `Submitted ${message.workflow_type}: '${message.contents}'`;
//   const inner = message.workflow_type ? typeAnnotation : message.contents;

//   console.log('message.debug', message.debug);

//   return (
//     <>
//       <SyntaxHighlighter
//         language={language}
//         className="rounded-xl p-0 m-0"
//         style={vscDarkPlus}
//         showLineNumbers={showLineNumbers}
//         wrapLongLines={wrapLongLines}>
//         {inner}
//       </SyntaxHighlighter>
//       {JSON.stringify(message.debug)}
//       {/* <ul className="flex flex-col">{debug}</ul> */}
//     </>
//   );
// }

export function MessageHistory({
  messages,
  waiting,
}: {
  messages: QueryPassageAnswer[];
  waiting: boolean;
}) {
  const renderedMessages = messages.map((message: QueryPassageAnswer, i: number) => {
    return (
      <li key={i} className="">
        <div className="outline outline-2 outline-slate-200 rounded-lg m-6">
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
