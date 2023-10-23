// frontend/src/pages/index.tsx
import { useSession } from 'next-auth/client';
import { sendLLMRequest } from '../api/api';

export default function Home() {
  const [session, loading] = useSession();

  useEffect(() => {
    if (!loading && session) {
      sendLLMRequest({ sessionId: session.id });
    }
  }, [loading, session]);

  // Rest of the component
};
```

```typescript
// frontend/src/api/api.ts
import axios from 'axios';

export const sendLLMRequest = async (sessionId: string) => {
  const response = await axios.post('/api/llm', { sessionId });
  return response.data;
};
```

```python
# backend/main.py
from fastapi import FastAPI
from . import llm

app = FastAPI()

@app.post("/llm")
async def llm_endpoint(sessionId: str):
    return llm.handle_request(sessionId)
```

```python
# backend/llm.py
def handle_request(sessionId: str):
    # Handle the request using the session ID
