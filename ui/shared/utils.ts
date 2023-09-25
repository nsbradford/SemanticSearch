import { v4 as uuidv4 } from 'uuid';

// Function to get or create session ID
export const getSessionId = (): string => {
  if (typeof window === 'undefined') return 'ANONYMOUS';
  let sessionId = localStorage.getItem('sessionId');
  
  if (!sessionId) {
    sessionId = uuidv4();
    localStorage.setItem('sessionId', sessionId);
  }
  
  return sessionId;
};
