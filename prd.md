# PRD - AI-Powered Healthcare Document Parser
## v1.0 | March 2026

---

## 📋 Executive Summary

Build a minimum viable product (MVP) that automatically extracts structured data from healthcare documents (invoices, prescriptions, medical reports) using AI-powered parsing. The system combines a React frontend for document uploads, a Flask backend for processing, and an open-source LLM via OpenRouter for document understanding.

**Primary Goal**: Demonstrate ability to solve the document processing challenge Alan faces (2M+ documents/year) with modern AI infrastructure.

**Timeline**: 2-3 weeks  
**Tech Stack**: React | Flask | PostgreSQL | OpenRouter (Mistral Small 3.1 24B) | Python

---

## 🎯 Objectives

### Primary Goals
- [ ] Build a working document parser that extracts key healthcare data from PDFs/images
- [ ] Demonstrate understanding of Alan's core problem domain (document parsing at scale)
- [ ] Show technical competency across frontend, backend, and AI integration
- [ ] Deploy a live, demo-able application

### Secondary Goals
- [ ] Implement document classification (invoice vs prescription vs report)
- [ ] Build a simple search/history feature
- [ ] Add confidence scoring to extracted fields
- [ ] Create clear documentation and deployment instructions

---

## 📦 Product Features

### MVP (Weeks 1-2)
#### 1.1 Document Upload & Processing
- **User Story**: As a user, I want to upload a medical document and automatically extract key information
- **Acceptance Criteria**:
  - Support PDF and image uploads (JPG, PNG)
  - Process documents within 10 seconds
  - Return structured JSON output
  - Handle documents up to 10MB

#### 1.2 Extraction Fields (Core Data)
For invoices:
- Invoice number
- Date issued
- Patient/Member name
- Total amount
- Itemized services (description + cost)
- Provider name
- Dates of service

For prescriptions:
- Patient name
- Doctor name
- Medications (name, dosage, quantity, frequency)
- Prescription date
- Refills

For reports:
- Report type (lab, pathology, imaging, etc.)
- Patient name
- Test/Procedure name
- Results summary
- Date

#### 1.3 Simple Dashboard
- **Upload interface** with drag-and-drop
- **Results display** showing extracted data in structured table format
- **Processing status** (loading, success, error states)
- **Copy/export** extracted data as JSON

#### 1.4 History & Search
- **Local history** (store last 10 uploads in browser)
- **Basic search** by document type or date
- **Ability to re-view** past extractions

### MVP+ (Week 3 - if time permits)
#### 2.1 Document Classification
- Automatically detect document type (Invoice/Prescription/Report)
- Display confidence score
- Allow user to override classification

#### 2.2 Confidence Scoring
- Show confidence for each extracted field (e.g., "Invoice #: 12345 (98% confidence)")
- Highlight low-confidence fields for manual review

#### 2.3 Batch Processing
- Upload multiple documents at once
- Queue and process sequentially
- Download results as CSV/JSON

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Upload Page  │→ │ Results View │→ │   History    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (Flask + PostgreSQL)                   │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────────┐   │
│  │ Upload Handler│→ │ LLM Processor │→│ DB Persistence │  │
│  └───────────────┘  └──────────────┘  └───────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ API Call
                         ↓
┌─────────────────────────────────────────────────────────────┐
│    LLM API (OpenRouter → NVIDIA Nemotron 12B)             │
│  Structured extraction with JSON schema validation          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow
1. User uploads document (PDF/image)
2. Flask receives file → validates format/size
3. Convert PDF to images if needed (pdf2image)
4. Encode image as base64
5. Send to OpenRouter NVIDIA Nemotron with structured prompt
6. Parse LLM response → JSON
7. Validate extracted fields with Pydantic
8. Save to PostgreSQL
9. Return structured response to frontend
10. React displays results in table format

---

## 🔧 Technical Specifications

### Frontend (React)
**Stack**: React 18 + TypeScript + Tailwind CSS + React Query

**Key Components**:
```
src/
├── components/
│   ├── UploadZone.tsx       # Drag-drop upload
│   ├── ResultsDisplay.tsx   # Show parsed data
│   ├── DocumentHistory.tsx  # Past uploads list
│   └── LoadingSpinner.tsx   # Status indicator
├── pages/
│   ├── Home.tsx            # Main upload page
│   └── History.tsx         # Historical documents
├── services/
│   ├── api.ts              # Flask API calls
│   └── storage.ts          # LocalStorage helper
├── types/
│   └── document.ts         # TypeScript interfaces
└── App.tsx
```

**Dependencies**:
- `axios` - HTTP client
- `react-dropzone` - File upload
- `react-query` - Data fetching/caching
- `tailwindcss` - Styling

### Backend (Flask)
**Stack**: Flask + Pydantic + PostgreSQL + Flask-RESTful

**Key Endpoints**:
```
POST /api/documents/upload
  ├─ Input: File (PDF/image)
  ├─ Output: { id, status, extracted_data, confidence }
  └─ Status: 200/400/500

GET /api/documents/<id>
  ├─ Input: Document ID
  ├─ Output: Full document + extraction results
  └─ Status: 200/404

GET /api/documents
  ├─ Query: ?type=invoice&limit=10
  ├─ Output: List of documents
  └─ Supports pagination

POST /api/documents/<id>/refine
  ├─ Input: Corrected fields
  ├─ Output: Updated document
  └─ For user corrections
```

**File Structure**:
```
backend/
├── app.py               # Flask app + routes
├── models.py            # SQLAlchemy models & Pydantic schemas
├── llm_service.py       # OpenRouter integration
├── document_service.py  # Document processing logic
├── database.py          # SQLAlchemy + PostgreSQL setup
├── config.py            # Configuration (dev, prod, test)
├── requirements.txt
├── .env.example
└── wsgi.py              # For production deployment
```

**Key Dependencies**:
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.25
psycopg2-binary==2.9.9  # PostgreSQL driver
Werkzeug==3.0.1         # File upload handling
requests==2.31.0
pydantic==2.5.0
pdf2image==1.16.3       # Convert PDF → images
pillow==10.1.0          # Image processing
python-dotenv==1.0.0
gunicorn==21.2.0        # Production server
```

### Database (PostgreSQL)

**Schema**:
```sql
-- Documents table
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  filename VARCHAR(255),
  document_type VARCHAR(50),  -- 'invoice', 'prescription', 'report'
  raw_content BYTEA,          -- Uploaded file
  extraction_status VARCHAR(20),  -- 'pending', 'success', 'failed'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Extracted data
CREATE TABLE extractions (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  raw_response TEXT,          -- LLM response
  structured_data JSONB,      -- Parsed/validated JSON
  confidence_scores JSONB,    -- Field-level confidence
  created_at TIMESTAMP DEFAULT NOW()
);

-- User corrections (for refinement)
CREATE TABLE corrections (
  id UUID PRIMARY KEY,
  extraction_id UUID REFERENCES extractions(id),
  field_name VARCHAR(100),
  original_value TEXT,
  corrected_value TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### LLM Integration (OpenRouter + NVIDIA Nemotron)

**Model Selection**: 
- **Recommended**: `nvidia/nemotron-nano-12b-v2-vl:free` ⭐ **Specialized for document intelligence & OCR**
- **Backup**: `qwen/qwen2.5-vl-32b-instruct:free` (excellent for structured extraction)
- **Check**: https://openrouter.ai/collections/free-models for latest free options

**Why NVIDIA Nemotron for this project:**
- Specifically designed for document intelligence and optical character recognition (OCR)
- Multimodal support (images + text)
- Efficient inference with Transformer-Mamba hybrid architecture
- 128K context window (handles long documents)
- Free tier on OpenRouter

**Important**: Free models have rate limits (~20 req/min, ~200 req/day). Cache results in DB to avoid hitting limits during development.

**Prompt Strategy** (Structured Extraction):
```python
# System prompt
SYSTEM_PROMPT = """
You are a healthcare document parser. Extract structured data 
from medical documents with high accuracy. Always respond with 
valid JSON matching the provided schema.
"""

# User prompt (for invoice)
USER_PROMPT = """
Extract the following from this invoice document:
- invoice_number (string)
- invoice_date (YYYY-MM-DD)
- patient_name (string)
- provider_name (string)
- total_amount (float)
- services (array of {description, cost})

Document image: [base64_encoded_image]

Respond ONLY with valid JSON. If field is missing, set to null.
Include a "confidence" field (0-100) for each extracted field.
"""
```

**Flask Integration Example**:
```python
# llm_service.py
import requests
import json
from config import OPENROUTER_API_KEY

def parse_document(image_base64: str, extraction_type: str) -> dict:
    """
    Call OpenRouter NVIDIA Nemotron to extract data from document
    
    Args:
        image_base64: Base64 encoded image
        extraction_type: 'invoice' | 'prescription' | 'report'
    
    Returns:
        dict with extracted data and confidence scores
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourapp.com",
        "X-Title": "Medical Document Parser",
        "Content-Type": "application/json"
    }
    
    system_prompt = f"""You are a healthcare document parser.
Extract structured data from {extraction_type} documents.
Always respond with valid JSON only."""
    
    user_prompt = f"""Parse this {extraction_type} document and extract:
- All key fields visible in the document
- Confidence score (0-100) for each field
- Missing fields that should be present

Document image: [base64_image]

Respond ONLY with valid JSON."""
    
    payload = {
        "model": "nvidia/nemotron-nano-12b-v2-vl:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image",
                        "image": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        
        # Extract text from response
        extracted_text = result['choices'][0]['message']['content']
        
        # Parse JSON from response
        extracted_json = json.loads(extracted_text)
        
        return {
            "success": True,
            "data": extracted_json,
            "model": "nvidia/nemotron-nano-12b-v2-vl:free"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"OpenRouter API error: {str(e)}",
            "data": None
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse JSON response: {str(e)}",
            "data": None
        }


# app.py - Flask routes using llm_service
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import base64
import uuid
from llm_service import parse_document
from document_service import save_document_to_db

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    """
    Handle document upload and processing
    """
    
    # Validate request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    doc_type = request.form.get('type', 'invoice')  # invoice, prescription, report
    
    if not file.filename:
        return jsonify({"error": "No filename"}), 400
    
    # Validate file type
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"File type .{ext} not supported. Use PDF, JPG, or PNG"
        }), 400
    
    # Validate file size (max 10MB)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    if file_size > 10 * 1024 * 1024:
        return jsonify({"error": "File too large (max 10MB)"}), 400
    file.seek(0)  # Reset to start
    
    try:
        # Read file and convert to base64
        file_content = file.read()
        image_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Call LLM to parse document
        llm_result = parse_document(image_base64, doc_type)
        
        if not llm_result['success']:
            return jsonify({
                "error": llm_result['error'],
                "status": "failed"
            }), 500
        
        # Save to database
        doc_id = str(uuid.uuid4())
        saved = save_document_to_db(
            doc_id=doc_id,
            filename=secure_filename(file.filename),
            doc_type=doc_type,
            extracted_data=llm_result['data'],
            raw_file=file_content
        )
        
        if not saved:
            return jsonify({"error": "Database error"}), 500
        
        return jsonify({
            "success": True,
            "id": doc_id,
            "status": "success",
            "extracted_data": llm_result['data'],
            "model_used": llm_result['model']
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": f"Processing error: {str(e)}",
            "status": "error"
        }), 500


@app.route('/api/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """Retrieve a specific document and its extraction"""
    from document_service import get_document_from_db
    
    doc = get_document_from_db(doc_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404
    
    return jsonify({
        "id": doc['id'],
        "filename": doc['filename'],
        "type": doc['type'],
        "created_at": doc['created_at'],
        "extracted_data": doc['extracted_data'],
        "status": "success"
    }), 200


@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List documents with optional filters"""
    from document_service import list_documents_from_db
    
    doc_type = request.args.get('type', None)
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    docs = list_documents_from_db(doc_type=doc_type, limit=limit, offset=offset)
    
    return jsonify({
        "success": True,
        "documents": docs,
        "total": len(docs)
    }), 200
```

---

## 📅 Development Timeline

### Week 1: Foundation
- [ ] **Day 1-2**: Project setup + Docker setup
  - Flask project structure
  - React app scaffold (Vite)
  - PostgreSQL local instance
  - Environment configuration
  
- [ ] **Day 3-5**: Backend infrastructure
  - Flask routes skeleton
  - SQLAlchemy models
  - File upload handling (multipart)
  - PDF → image conversion pipeline

### Week 2: AI Integration + Core Features
- [ ] **Day 6-8**: LLM integration
  - OpenRouter API setup
  - Structured extraction prompt design
  - JSON validation with Pydantic
  - Error handling & retry logic
  
- [ ] **Day 9-10**: Frontend
  - Upload interface (drag-drop)
  - Results display table
  - Loading states
  - Basic styling (Tailwind)

### Week 3: Polish + MVP+ Features
- [ ] **Day 11-12**: History & refinement
  - localStorage for recent uploads
  - Document classification
  - Confidence score display
  - User corrections flow
  
- [ ] **Day 13-14**: Testing & deployment
  - Unit tests (pytest)
  - Component tests (React Testing Library)
  - Fix bugs from manual testing
  - Deploy to Vercel (frontend) + Railway/Render (backend)

---

## 🚀 Deployment Strategy

### Frontend
- **Vercel** (free tier, auto-deploys from GitHub)
- Environment: `VITE_API_URL=https://api.yourdomain.com`

### Backend
- **Railway** or **Render** (free tier with PostgreSQL)
- Environment variables:
  - `DATABASE_URL`
  - `OPENROUTER_API_KEY`
  - `CORS_ORIGINS`

### Database
- **PostgreSQL** on Railway/Render (included in free tier)
- Migrations: Use Alembic for schema versioning

---

## ✅ Definition of Done

A feature is complete when:
1. Code is written and tested locally
2. Follows project conventions (type hints, docstrings)
3. No console warnings/errors
4. Works in both Firefox and Chrome
5. Handles edge cases (large files, network errors, invalid documents)
6. Documentation is updated (README, API docs)
7. Deployed to staging environment
8. Tested end-to-end

---

## 🎬 Acceptance Criteria

### MVP Must-Haves
- [x] Upload a PDF/image of healthcare document
- [x] Automatic extraction of ~10-15 key fields
- [x] Display results in readable table format
- [x] Handle basic error cases (unsupported format, file too large)
- [x] Fast response time (<10 seconds average)
- [x] Live demo URL that works without login

### Code Quality
- [x] Type hints on all functions (Python)
- [x] TypeScript strict mode enabled (React)
- [x] README with setup instructions
- [x] .env.example file for configuration
- [x] Docstrings on all backend functions
- [x] Git history with clear, atomic commits

### Nice-to-Have (MVP+)
- [x] Document classification with confidence
- [x] Search/filter history
- [x] Batch upload capability
- [x] API documentation (Flask-RESTX for auto-generated Swagger)

---

## 📚 Resources & References

### AI/LLM Docs
- **OpenRouter**: https://openrouter.ai/docs
- **OpenRouter Free Models**: https://openrouter.ai/models (check latest)
- **Mistral Instruct**: Model specifically designed for structured tasks
- **Vision/Image Capabilities**: https://openrouter.ai/docs#vision

### Tech Stack Docs
- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **SQLAlchemy**: https://docs.sqlalchemy.org/

### Similar Projects (Reference)
- Docup.app (document intelligence)
- Invoice parser examples on GitHub
- Hugging Face Document Understanding models

---

## 🎨 UI/UX Notes

### Key User Flows

**Flow 1: New User Upload**
```
User lands on home → Sees upload zone (drag-drop) 
→ Selects document → Chooses type (invoice/prescription/report) 
→ Clicks "Parse" → Loading spinner → Results table appears 
→ Can copy data / export as JSON / see confidence scores
```

**Flow 2: Viewing History**
```
Click "History" tab → See list of past documents 
→ Click to re-view → Same results display as in Flow 1 
→ Can see original file preview thumbnail
```

### Design Principles
- **Clarity**: Show exactly what was extracted, highlight uncertain fields
- **Speed**: Minimize clicks, fast feedback (loading indicator)
- **Trust**: Show confidence scores so user knows what to trust
- **Accessibility**: Good color contrast, keyboard navigation

---

## ⚠️ Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| LLM accuracy low on medical docs | Medium | High | Start with simple invoices, test with real samples early |
| OpenRouter API rate limits | Low | Medium | Cache results, implement retry logic, use free tier wisely |
| PDF parsing issues | Medium | Medium | Fallback to image preprocessing, handle scanned PDFs |
| Deployment complexity | Low | Medium | Use Docker, test locally first, clear deployment docs |
| User confusion on features | Low | Low | Clear UI labels, tooltips, onboarding message |

---

## 📝 Notes for Implementation

1. **Start Simple**: Get basic upload + LLM call working before polishing UI
2. **Test Early**: Try parsing 5-10 real healthcare documents before finalizing prompts
3. **Handle Failures**: LLM might hallucinate → validate JSON strictly, set null for bad extracts
4. **Database Optimization**: Index document_type and created_at for fast queries
5. **Error Messages**: Show user-friendly errors ("File too large") not stack traces
6. **CORS Configuration**: Flask-CORS needs proper CORS headers for frontend
   ```python
   from flask_cors import CORS
   CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://yourdomain.com"]}})
   ```
7. **File Upload Security**: Use werkzeug.utils.secure_filename to prevent path traversal attacks
8. **Environment Variables**: Store OPENROUTER_API_KEY in .env, never commit to git

---

## 🔗 Success Metrics (for portfolio)

When applying to Alan, highlight:
- ✅ **Scale**: Processed X documents in 2 weeks
- ✅ **Accuracy**: Achieved X% extraction accuracy on test set
- ✅ **Speed**: 95th percentile response time < 10s
- ✅ **Code Quality**: Type-safe Flask, TypeScript frontend, tested
- ✅ **Shipped**: Live demo link in cover letter
- ✅ **AI Integration**: NVIDIA Nemotron integration via OpenRouter for document intelligence
- ✅ **Business Understanding**: Explain how this solves Alan's 2M documents/year problem
- ✅ **Production Ready**: Docker setup, error handling, rate limit awareness

---

**Version History**
- v1.0 | March 9, 2026 | Initial PRD
