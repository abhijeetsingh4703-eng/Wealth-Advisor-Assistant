import './globals.css';

export const metadata = {
  title: 'Wealth Advisor Assistant | Agent Dashboard',
  description: 'Multi-agent AI system for wealth advisory decisions',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
