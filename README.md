Wealth Advisor Assistant

What it does

1. The Orchestrator: This is the manager. It decides who needs to run and when.
2. Data Fetcher: Grabs the client info and transaction history (right now, this just reads from some JSON mock files).
3. Analyzer: Looks at the transactions and tries to spot anything weird, like massive withdrawals or unusual spending patterns. 
4. Report Generator: Takes everything and writes up a final summary.

Getting Started

To run this on your own machine, you'll need two terminal windows open.

1. Start the Backend
First, we need to get the Python API running. Open a terminal in the root folder(not backend folder the main where all folders are) and run:
a.  pip install -r backend/requirements.txt
b.  python -m backend.main

This will start the server on http://localhost:8000.

2. Start the Frontend
In a second terminal, let's get the web dashboard up. Navigate to the frontend folder:
cd frontend
npm install
npm run dev

Once it's ready, just head over to http://localhost:3000 



<img width="1635" height="791" alt="Screenshot 2026-05-28 212905" src="https://github.com/user-attachments/assets/1d2f9375-6d41-4572-b767-3c4158b541d0" />

