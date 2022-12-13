import axios from 'axios'
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import { backendRootUrl, SemanticDoc, TypingIndicator } from '../../components/Utils'

const DocPage = () => {
  const router = useRouter()
  const { doc_id } = router.query
  const [document, setDocument] = useState<SemanticDoc>()

  useEffect(() => {
    async function fetchDoc() {
      console.log('fetchDoc', doc_id)
      const url = backendRootUrl + '/document/' + doc_id;
      const response = await axios.get(url);
      const data: SemanticDoc = response.data;
      console.log('data', data)
      // console.log(`setDoc, contents of length: ${data.contents.length}`, data)
      setDocument(data);
      console.log('finished')
    }
    fetchDoc();
  }, [doc_id])
    
  const body = (document
    ? <div className="p-4 place-content-center">
      <h1 className="text-center mb-4 text-4xl border-b-2">{document.name}</h1>
      <div className="flex place-content-center w-full p-10">
        <p className="whitespace-pre-line">{document.contents}</p>
      </div>
      </div>
    : <TypingIndicator />
  );

  return body;
}

export default DocPage