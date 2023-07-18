import { Metadata } from 'next';
import Head from 'next/head';
export const metadata: Metadata = {
  title: `Semantic Search`,
  icons: {
    icon: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
  themeColor: [
    {
      color: '#ffffff',
    },
  ],
};

export function HeadDefault() {
  return (
    <Head>
      {/* title was removed */}
      {/* link was removed */}
      {/* link was removed */}
      {/* link was removed */}
      {/* link was removed */}
      {/* link was removed */}
      <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
      <meta name="msapplication-TileColor" content="#da532c" />
      {/* meta was removed */}
    </Head>
  );
}
