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

Once it's ready, just head over to http://localhost:3000 (or whatever port it gives you) in your browser.

A Few Notes on How It's Built

No heavy AI frameworks: I decided to just build the agent classes from scratch in Python rather than using something heavy like LangChain. It makes it much easier to debug and figure out what's actually happening under the hood.

Memory: Everything happening right now is stored in-memory while the workflow runs, but final reports and decisions are saved into a simple local SQLite file (memory.db).

Data: For now, the CRM and market data are just static JSON files in the backend/mock_data folder. 
