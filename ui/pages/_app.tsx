import type { AppProps } from 'next/app';
import '../styles/globals.css';

// https://stackoverflow.com/questions/66539699/fontawesome-icons-not-working-properly-in-react-next-app
import '@fortawesome/fontawesome-svg-core/styles.css';

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default MyApp;
