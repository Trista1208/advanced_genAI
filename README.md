# Advanced GenAI - ETH Zurich Document Processing Pipeline

A comprehensive multi-stage pipeline for processing HTML documents (ETH Zurich content), extracting metadata, and creating a Q&A benchmark system with AI-powered relevance scoring.

## 📋 Overview

This pipeline transforms raw HTML documents into structured, enriched data with metadata extraction and relevance scoring:

1. **Stage 1**: Data extraction, cleaning, validation, and benchmark creation
2. **Stage 2**: LLM-based metadata extraction and relevance scoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (for Stage 2)
- HTML documents for processing
- Benchmark PDF file (optional, for Q&A extraction)

### Installation

#### Option 1: Automated Setup (Linux/Mac)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Activate environment
source venv/bin/activate
```

#### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm

# Create directory structure
python setup_directories.py
```

### Configuration

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

2. Place your input data:
   - HTML files → `data/` directory
   - Benchmark PDF → `benchmark/` directory

## 📁 Project Structure

```
advanced_genAI-main/
├── data/                           # Input HTML files
├── data_cleaned/
│   ├── minimal_hybrid/            # Step 1.1 output
│   ├── advanced/                  # Step 1.2 output
│   └── advanced_validated/        # Step 1.3 output
├── benchmark/
│   ├── BenchmarkQuestionsAnswers.pdf
│   ├── metadata/                  # Step 2.1 output
│   └── score/                     # Step 2.2 output
├── subsample/
│   └── semantic_chunk/            # Chunked documents
├── step_1_hybrid.py               # Stage 1.1: HTML parsing
├── step_1_2_advanced_cleaning_and_metadata.py  # Stage 1.2
├── step_1_3_validation_filter.py  # Stage 1.3
├── step_1_4_benchmark_extraction.py  # Stage 1.4
├── 2_1_llm_metadataextraction.py  # Stage 2.1
├── 2_1_2_relevance_score.py       # Stage 2.2
└── requirements.txt
```

## 🔄 Pipeline Stages

### Stage 1: Data Extraction & Cleaning

#### Step 1.1: Hybrid HTML Parsing

Extract clean text from HTML using BeautifulSoup + Docling.

```bash
python step_1_hybrid.py data data_cleaned/minimal_hybrid
```

**Output**: JSON files with:
- `doc_id`: Unique SHA-1 identifier
- `filename`: Original filename
- `raw_text`: Cleaned text content
- `paragraphs`: List of paragraphs

#### Step 1.2: Advanced Cleaning & Metadata

Deep cleaning and metadata extraction with NLP.

```bash
python step_1_2_advanced_cleaning_and_metadata.py \
    data_cleaned/minimal_hybrid \
    data_cleaned/advanced \
    --threshold 5
```

**Features**:
- Removes boilerplate disclaimers and footers
- Filters repeated paragraphs (appearing in 5+ documents)
- Language detection (EN/DE/FR/IT)
- Date extraction from directory structure
- Named Entity Recognition (persons, organizations, locations)
- Keyword extraction (YAKE algorithm)
- Automatic summarization
- Text statistics

**Output**: Enriched JSON files with:
- `main_content`: Final cleaned text
- `paragraphs_cleaned`: Cleaned paragraphs
- `language`: Detected language code
- `named_entities`: List of entities with labels
- `keywords`: Extracted keywords
- `summary`: Text summary
- `text_stats`: Character, word, and paragraph counts
- `date`, `year`, `month`: Temporal metadata

#### Step 1.3: Validation & Filtering

Remove documents with empty content.

```bash
python step_1_3_validation_filter.py \
    data_cleaned/advanced \
    data_cleaned/advanced_validated
```

**Output**: Only documents with non-empty `paragraphs_cleaned`

#### Step 1.4: Benchmark Q&A Extraction

Extract structured Q&A pairs from PDF benchmark.

```bash
python step_1_4_benchmark_extraction.py \
    benchmark/BenchmarkQuestionsAnswers.pdf \
    data_cleaned/benchmark_qa.json
```

**Output**: JSON array with Q&A pairs:
- `id`: Question ID
- `question`: Question text
- `answer`: Answer text
- `notes`: Optional scoring notes

### Stage 2: LLM-Based Enhancement

⚠️ **Requires OpenAI API key and costs money per API call**

#### Step 2.1: Metadata Extraction

Extract structured metadata using GPT-4o-mini.

```bash
# With automatic output directory
python 2_1_llm_metadataextraction.py \
    --chunks subsample/semantic_chunk

# With custom output directory
python 2_1_llm_metadataextraction.py \
    --chunks subsample/semantic_chunk \
    --meta-dir benchmark/metadata/custom
```

**Features**:
- Structured extraction using Pydantic schemas
- Automatically skips already-processed chunks
- Normalizes all text to lowercase

**Output**: One JSON file per chunk with:
- `chunk_summary`: 30-word summary
- `entities`: Persons, organizations, locations
- `topic_tags`: Relevant topics
- `event_dates`: Temporal events
- `role_annotations`: Person-role relationships
- `numeric_facts`: Quantitative information
- `department`, `initiative`, `grant_type`: ETH-specific metadata

#### Step 2.2: Relevance Scoring

Score chunk relevance to 25 benchmark questions.

```bash
# List chunks missing scores
python 2_1_2_relevance_score.py --list-missing

# Score missing chunks (includes answers in prompt)
python 2_1_2_relevance_score.py

# Score without showing answers to model
python 2_1_2_relevance_score.py --no-answer

# Custom configuration
python 2_1_2_relevance_score.py \
    --chunks subsample/semantic_chunk \
    --qa-path benchmark/benchmark_qa_bilingual_with_semantic_chunks.json \
    --score-dir benchmark/score/custom
```

**Scoring Rubric**:
- 1.0: Exact answer in chunk
- 0.8: Answer stated verbatim
- 0.5: Partial/indirect answer
- 0.2: Tangentially related
- 0.0: Unrelated

**Output**: One JSON file per chunk with 25 question scores:
```json
{
  "1": {
    "relevance_score": 0.8,
    "relevance_reason": "Chunk directly mentions..."
  },
  ...
}
```

## 🛠️ Advanced Usage

### Processing Custom HTML Collections

```bash
# Process HTML from specific directory
python step_1_hybrid.py /path/to/html/files output/directory

# Adjust repeated paragraph threshold
python step_1_2_advanced_cleaning_and_metadata.py \
    input output --threshold 10
```

### Batch Processing Tips

1. **Incremental Processing**: All scripts skip already-processed files
2. **Resume After Interruption**: Simply re-run the same command
3. **Monitor API Costs**: Use `--list-missing` to check remaining work

### Customizing Boilerplate Removal

Edit `step_1_2_advanced_cleaning_and_metadata.py`, lines 94-188:

```python
BOILERPLATE_PATTERNS = [
    r"^YourPattern\s*$",
    # Add more patterns as needed
]
```

**Note**: Currently only 6 patterns are active. Uncomment additional patterns if you see residual boilerplate in output.

## 📊 Expected Outputs

### Stage 1 Complete
- ~N JSON files in `data_cleaned/advanced_validated/`
- 1 JSON file with Q&A pairs in `data_cleaned/`
- Each document with: cleaned text, entities, keywords, summary, metadata

### Stage 2 Complete  
- ~N metadata JSON files in `benchmark/metadata/`
- ~N score JSON files in `benchmark/score/`
- Full structured metadata and relevance scores for all chunks

## 🐛 Troubleshooting

### Common Issues

**Import Errors**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check spaCy models
python -m spacy validate
```

**OpenAI API Errors**:
```bash
# Verify API key
echo $OPENAI_API_KEY

# Check .env file
cat .env
```

**Empty Output**:
- Check that input files exist in correct directories
- Verify file permissions
- Review logs for error messages

**OCR Issues in PDF Extraction**:
- Edit `step_1_4_benchmark_extraction.py` to add custom OCR corrections
- Test extraction: `python step_1_4_benchmark_extraction.py <pdf> test_output.json`

### Logging

All scripts use Python logging. To increase verbosity, edit the script:

```python
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
```

## 💡 Tips & Best Practices

1. **Start Small**: Test with a small subset of HTML files first
2. **Monitor Costs**: Stage 2 costs ~$0.01-0.05 per chunk
3. **Backup Data**: Keep original HTML files separate
4. **Version Control**: Don't commit `data/` or `.env` to git
5. **Quality Check**: Review outputs after each stage
6. **Threshold Tuning**: Adjust `--threshold` based on your corpus size

## 🔐 Security Notes

- **Never commit `.env`** to version control
- `.gitignore` is pre-configured to exclude sensitive files
- API keys are loaded via environment variables only
- All API calls are logged (without exposing keys)

## 📖 Dependencies

Core libraries:
- **docling**: Advanced document parsing
- **BeautifulSoup4**: HTML parsing
- **spaCy**: Named entity recognition
- **YAKE**: Keyword extraction
- **Lingua**: Language detection
- **OpenAI**: GPT-4o-mini API access
- **Pydantic**: Schema validation
- **pdfplumber**: PDF text extraction

See `requirements.txt` for complete list with versions.

## 🤝 Contributing

When adding new features:
1. Test with small dataset first
2. Add logging for debugging
3. Update this README
4. Follow existing code style

## 📄 License

[Specify your license here]

## 📧 Contact

[Add contact information]

---

**Last Updated**: December 2025
