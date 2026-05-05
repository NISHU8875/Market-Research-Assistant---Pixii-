# Setup & Installation Guide

Complete step-by-step guide to set up the Research Assistant RAG Agent on your machine.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** (check: `python --version`)
- **pip** (Python package manager) - comes with Python
- **Git** (optional, for cloning)
- **Internet connection** (for API keys and package downloads)
- **4GB RAM minimum** (8GB+ recommended)

### System Compatibility
- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, etc.)

---

## 🚀 Quick Start (5 minutes)

### Step 1: Get Groq API Key (Free)
1. Go to https://console.groq.com/
2. Sign up (free account required)
3. Navigate to "Keys" section
4. Create new API key
5. **Copy and save your key** (you'll need it in Step 3)

### Step 2: Clone or Download Repository

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/NISHU8875/research-assistant-rag-agent.git
cd research-assistant-rag-agent
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the downloaded ZIP file
4. Open terminal/command prompt in extracted folder

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

**Troubleshooting**: If you get permission errors:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (see next section)
```

### Step 4: Configure Environment

Create `.env` file:

**On Windows (Command Prompt)**:
```bash
copy .env.example .env
# Then edit .env with notepad
```

**On macOS/Linux (Terminal)**:
```bash
cp .env.example .env
nano .env  # Edit the file
```

**Edit `.env`**:
```
GROQ_API_KEY=your_api_key_here
```
Replace `your_api_key_here` with the key from Step 1.

### Step 5: Run Application

```bash
streamlit run main.py
```

**Expected Output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser.

---

## 🐍 Recommended: Virtual Environment Setup

Virtual environments isolate project dependencies from system Python.

### Create Virtual Environment

**Windows**:
```bash
# Create
python -m venv venv

# Activate
venv\Scripts\activate
# (Command prompt should show: (venv) C:\path\>)

# Deactivate later with
deactivate
```

**macOS/Linux**:
```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate
# (Terminal should show: (venv) $)

# Deactivate later with
deactivate
```

### Install Dependencies in Virtual Environment

```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### Benefits of Virtual Environment
- ✅ Isolated dependencies per project
- ✅ No conflicts with system packages
- ✅ Easy to manage multiple projects
- ✅ Industry standard practice

---

## 🔧 Detailed Installation Steps

### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# Should show: Python 3.8.0 or higher

# Check pip
pip --version
# Should show: pip X.X.X from ...
```

If commands not found:
- **Windows**: Add Python to PATH during installation
- **macOS**: Install from https://www.python.org/ or use `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### Step 2: Get API Key (Detailed)

1. **Create Groq Account**
   - Visit: https://console.groq.com/
   - Click "Sign Up"
   - Enter email, password
   - Verify email

2. **Generate API Key**
   - Login to console
   - Click "API Keys" in left menu
   - Click "Create New API Key"
   - Name it "ResearchAssistant"
   - Copy the key (starts with `gsk_`)

3. **Save API Key Securely**
   - Store in `.env` file (don't share!)
   - Don't commit `.env` to Git
   - Check `.gitignore` includes `.env`

### Step 3: Download Repository

**Using Git** (Recommended):
```bash
# Navigate to where you want to store the project
cd ~/projects  # or your preferred folder

# Clone repository
git clone https://github.com/NISHU8875/research-assistant-rag-agent.git

# Enter project folder
cd research-assistant-rag-agent
```

**Using ZIP Download**:
1. Visit: https://github.com/NISHU8875/research-assistant-rag-agent
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Rename folder (optional): `research-assistant-rag-agent`
5. Open terminal in that folder

### Step 4: Setup Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify activation (should show (venv) in terminal)
which python
# Output should contain /venv/ or \venv\
```

### Step 5: Install Dependencies

```bash
# Make sure you're in project folder
cd path/to/research-assistant-rag-agent

# Install all required packages
pip install -r requirements.txt

# This will install:
# - langchain-community
# - langchain-chroma
# - langchain-groq
# - streamlit
# - duckduckgo-search
# - And more...
```

**Progress Display**:
```
Collecting langchain-community...
Downloading langchain-community-0.4.1.tar.gz (...)
Installing collected packages: beautifulsoup4, duckduckgo-search, ...
Successfully installed ...
```

### Step 6: Create .env File

Create a new file named `.env` in your project root:

**Windows (Notepad)**:
```bash
# Create the file
echo. > .env

# Open in notepad
notepad .env
```

**macOS/Linux (Terminal)**:
```bash
# Create and edit
nano .env
```

**File Contents**:
```
GROQ_API_KEY=gsk_your_actual_key_here_1234567890
```

**Save the file** (don't include quotes around the key)

### Step 7: Verify Installation

```bash
# Test Python can import required modules
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "import langchain; print('✓ LangChain OK')"
python -c "import chromadb; print('✓ ChromaDB OK')"

# Expected output:
# ✓ Streamlit OK
# ✓ LangChain OK
# ✓ ChromaDB OK
```

### Step 8: Run Application

```bash
# Make sure you're in project folder
cd research-assistant-rag-agent

# Make sure virtual environment is activated (if using)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start the application
streamlit run main.py
```

### Step 9: Access Application

- **Local**: Open http://localhost:8501 in your browser
- **Remote**: Use the Network URL shown in terminal
- **Expected**: Streamlit app loads with "Research Assistant RAG Agent" title

---

## 🎓 First Run Guide

1. **Paste a URL**
   - Enter a research article URL in the sidebar
   - Example: https://news.example.com/article

2. **Process URL**
   - Click "🚀 Process URLs"
   - Wait for status: "✅ Chunks stored"

3. **Select Response Style**
   - Choose a prompt template for your use case
   - Default: "General"

4. **Ask a Question**
   - Type your question in the chat box
   - Press Enter

5. **Get Answer**
   - Receive AI-powered response
   - See source attribution
   - Optional: Enable web search for supplementary info

---

## ⚙️ Configuration

### Environment Variables (.env)

**Required**:
```
GROQ_API_KEY=your_key_here
```

**Optional**:
```
# LLM Settings
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=700

# Embedding Settings
EMBEDDING_MODEL=Alibaba-NLP/gte-base-en-v1.5
CHUNK_SIZE=1000
```

### Streamlit Configuration

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#0d47a1"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
```

---

## 🐛 Troubleshooting Installation

### Issue: "Command not found: python"

**Solution**:
```bash
# Try python3 instead
python3 --version
python3 -m venv venv
```

Or add Python to PATH:
- **Windows**: Reinstall Python, check "Add Python to PATH"
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### Issue: "Module not found" errors

**Solution**:
```bash
# Ensure all dependencies installed
pip install -r requirements.txt --upgrade

# Or install individually
pip install streamlit langchain langchain-community langchain-chroma langchain-groq
```

### Issue: "GROQ_API_KEY not found"

**Solution**:
1. Verify `.env` exists in project root
2. Verify format: `GROQ_API_KEY=your_key` (no quotes)
3. Verify file is not `.env.txt` (must be `.env`)
4. Restart application: Stop and run `streamlit run main.py` again

### Issue: Port 8501 already in use

**Solution**:
```bash
# Use different port
streamlit run main.py --server.port 8502

# Or kill process using port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

### Issue: "SSL Certificate Verify Failed"

**Solution**:
```bash
# On Windows, run:
pip install --upgrade certifi

# Or disable SSL verification (not recommended for production):
pip install --trusted-host pypi.python.org -r requirements.txt
```

### Issue: Out of Memory

**Solution**:
- Close other applications
- Reduce CHUNK_SIZE in rag.py
- Process fewer URLs at once
- Upgrade system RAM

### Issue: Streamlit not starting

**Solution**:
```bash
# Verify streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install --upgrade streamlit

# Try running with explicit Python module
python -m streamlit run main.py
```

---

## 📦 Dependency Details

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.4.1+ | RAG framework |
| streamlit | 1.46.0+ | Web UI |
| langchain-chroma | 1.0.0 | Vector database |
| langchain-groq | 1.1.0 | LLM integration |
| langchain-huggingface | 1.1.0 | Embeddings |
| sentence-transformers | 5.1.2 | Transformer models |
| beautifulsoup4 | 4.13.3 | HTML parsing |
| duckduckgo-search | 3.9.10 | Web search |
| python-dotenv | 1.1.0 | Environment config |

---

## 🔐 Security Setup

### Protect Your API Key

1. **Never Share `.env` File**
   - It contains your API key
   - Verify `.gitignore` includes `.env`

2. **Regenerate if Compromised**
   - Go to https://console.groq.com/
   - Delete old key
   - Create new key

3. **Use Environment Variables in Production**
   - Deploy on Streamlit Cloud with secrets
   - Use environment variables on servers
   - Never hardcode keys in code

### .gitignore Verification

```bash
# Check that .env is ignored
git check-ignore .env
# Output: .env (means it's ignored - good!)

# Verify you didn't commit .env
git log --full-history -- .env
# Should show nothing (good!)
```

---

## 🚀 Deployment (Optional)

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select GitHub repo
   - Select main.py

3. **Add Secrets**
   - Go to app settings
   - Add secret: `GROQ_API_KEY=your_key`

### Deploy to Other Platforms

**Heroku, AWS, GCP, DigitalOcean**: Similar process with environment variables

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned/downloaded
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with GROQ_API_KEY
- [ ] API key is valid (test at console.groq.com)
- [ ] No syntax errors in Python files
- [ ] Streamlit runs without errors
- [ ] Browser opens to http://localhost:8501
- [ ] Can enter URL and process
- [ ] Can ask questions and get responses

---

## 📞 Getting Help

If you encounter issues:

1. **Check Troubleshooting Section** above
2. **Check GitHub Issues**: https://github.com/NISHU8875/research-assistant-rag-agent/issues
3. **Read FEATURES.md** for detailed feature documentation
4. **Check Groq Docs**: https://console.groq.com/docs
5. **Check LangChain Docs**: https://python.langchain.com/

---

## 📝 Next Steps

After successful setup:
1. Read [README.md](README.md) for overview
2. Read [FEATURES.md](FEATURES.md) for detailed features
3. Try different prompt templates
4. Enable web search for advanced queries
5. Process your own documents

---

**Last Updated**: May 2026  
**Version**: 2.0.0  
**Status**: Tested and Ready
