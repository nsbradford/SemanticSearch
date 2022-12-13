import typingIndicatorStyles from '../styles/TypingIndicator.module.scss';

// export const backendRootUrl = process.env.NEXT_PUBLIC_ROUTE_ROOT_URL;
export const isDevEnvironment = !process.env.NODE_ENV || process.env.NODE_ENV === 'development';
export const backendRootUrl = 'http://localhost:8000';

// export interface Message {
//   index: number;
//   message_type: MessageType;
//   contents: string;
//   workflow_type?: WorkflowType;
//   debug?: any[];
// }

export interface QueryPassageAnswer {
  before_text: string;
  passage_text: string;
  after_text: string;
  document_name: string;
}

export interface QueryFullAnswer {
  results: QueryPassageAnswer[];
}

// https://loading.io/css/
export function TypingIndicator() {
  return (
    <div className="flex place-content-center">
      <div className={`${typingIndicatorStyles.ldsdualring} m-1`}></div>
    </div>
  );
}

export function TextArea({
  userInput,
  setUserInput,
}: {
  userInput: string;
  setUserInput: (s: string) => void;
}) {
  return (
    <div>
      <div className="mt-1">
        <textarea
          rows={10}
          name="comment"
          id="comment"
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm"
          defaultValue={userInput}
          onChange={e => setUserInput(e.target.value)}
        />
      </div>
    </div>
  );
}
