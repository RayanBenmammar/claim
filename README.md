# Claim - AI Healthcare Document Parser

An AI-powered document parsing system that automatically extracts structured data from healthcare documents (invoices, prescriptions, medical reports).

## Tech Stack

- **Frontend**: React
- **Backend**: Flask
- **Database**: PostgreSQL
- **AI**: OpenRouter (Mistral Small 3.1 24B)

## Features

- 📄 Upload and parse PDFs and images (JPG, PNG)
- ⚡ Process documents in ~10 seconds
- 📊 Extract structured data (invoices, prescriptions, reports)
- 📋 View extraction history and search past documents
- 🎯 Automatic document classification with confidence scoring
- 📦 Batch processing support

## Getting Started

See the [PRD](./prd.md) for detailed requirements and architecture.

### API

1. **Create a virtual environment**
   `py -3 -m venv .venv`

2. **Activate the virtual environment**
   `.venv\Scripts\activate`

3. **Install dependencies**
   `pip install -r .\requirements.txt`

4. **Run the API**
   `flask run --debug`

### Front

1. **Install dependencies**
   `npm install`

2. **Run the UI**
   `npm run dev`

## Project Structure

- `/api` - Flask backend
- `/front` - React frontend
