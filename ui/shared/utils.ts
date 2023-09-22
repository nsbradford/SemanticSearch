import { v4 as uuidv4 } from 'uuid';

// Function to get or create session ID
export const getSessionId = (): string | null => {
  if (typeof window === 'undefined') return null;  // add this line
  let sessionId = localStorage.getItem('sessionId');
  
  if (!sessionId) {
    sessionId = uuidv4();
    localStorage.setItem('sessionId', sessionId);
  }
  
  return sessionId;
};
