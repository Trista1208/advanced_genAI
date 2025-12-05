# Pipeline Overview - Visual Guide

## 🔄 Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT DATA                                  │
├─────────────────────────────────────────────────────────────────────┤
│  • HTML files (ETH Zurich content)                                 │
│  • Benchmark PDF (Q&A pairs)                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 1: DATA PROCESSING                          │
│                     (Local, No API Cost)                            │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────┐
    │  Step 1.1: HTML Parsing (step_1_hybrid.py)              │
    ├──────────────────────────────────────────────────────────┤
    │  • BeautifulSoup: Remove HTML boilerplate               │
    │  • Docling: Extract text content                         │
    │  • Output: doc_id, filename, raw_text, paragraphs       │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌──────────────────────────────────────────────────────────┐
    │  Step 1.2: Advanced Cleaning & Metadata                 │
    │  (step_1_2_advanced_cleaning_and_metadata.py)           │
    ├──────────────────────────────────────────────────────────┤
    │  • Remove 70+ boilerplate patterns                      │
    │  • Filter repeated paragraphs                            │
    │  • Language detection (EN/DE/FR/IT)                     │
    │  • Named Entity Recognition (spaCy)                     │
    │  • Keyword extraction (YAKE)                             │
    │  • Auto-summarization                                    │
    │  • Date extraction from paths                            │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌──────────────────────────────────────────────────────────┐
    │  Step 1.3: Validation (step_1_3_validation_filter.py)   │
    ├──────────────────────────────────────────────────────────┤
    │  • Filter out empty documents                            │
    │  • Keep only valid paragraphs_cleaned                   │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌──────────────────────────────────────────────────────────┐
    │  Step 1.4: Benchmark Extraction                          │
    │  (step_1_4_benchmark_extraction.py)                      │
    ├──────────────────────────────────────────────────────────┤
    │  • Extract Q&A from PDF                                  │
    │  • Fix OCR errors                                        │
    │  • Structure: id, question, answer, notes               │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
                    [YOUR CHUNKING STEP]
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 2: LLM ENHANCEMENT                          │
│                  (OpenAI API, ~$0.03-0.05/chunk)                   │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────┐
    │  Step 2.1: Metadata Extraction                           │
    │  (2_1_llm_metadataextraction.py)                        │
    ├──────────────────────────────────────────────────────────┤
    │  Model: GPT-4o-mini                                      │
    │  Output: Structured metadata per chunk                   │
    │    • chunk_summary (30 words)                           │
    │    • entities (person, org, location)                   │
    │    • topic_tags                                          │
    │    • event_dates                                         │
    │    • role_annotations                                    │
    │    • numeric_facts                                       │
    │    • department, initiative, grant_type                 │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌──────────────────────────────────────────────────────────┐
    │  Step 2.2: Relevance Scoring                             │
    │  (2_1_2_relevance_score.py)                             │
    ├──────────────────────────────────────────────────────────┤
    │  Model: GPT-4o-mini                                      │
    │  For each chunk:                                         │
    │    • Score vs. 25 benchmark questions                   │
    │    • Relevance: 0.0 (unrelated) to 1.0 (exact)         │
    │    • Reasoning for each score                            │
    └──────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FINAL OUTPUT                                  │
├─────────────────────────────────────────────────────────────────────┤
│  • Clean, structured documents                                     │
│  • Rich metadata per chunk                                         │
│  • Relevance scores for retrieval                                  │
│  • Ready for RAG/semantic search                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 📊 Data Transformation Example

### Input (HTML)
```html
<html>
  <nav>Navigation</nav>
  <script>...</script>
  <div>
    Margrit Leuthold has been the Executive Director...
  </div>
  <footer>Newsletter abonnieren</footer>
</html>
```

### After Step 1.1
```json
{
  "doc_id": "9b7f034dc9cd5fd1b...",
  "filename": "example.html",
  "raw_text": "Navigation\nMargrit Leuthold has...\nNewsletter abonnieren",
  "paragraphs": ["Navigation", "Margrit Leuthold has...", "Newsletter abonnieren"]
}
```

### After Step 1.2
```json
{
  "doc_id": "9b7f034dc9cd5fd1b...",
  "filename": "example.html",
  "language": "de",
  "main_content": "Margrit Leuthold has been the Executive Director...",
  "paragraphs_cleaned": ["Margrit Leuthold has been the Executive Director..."],
  "named_entities": [
    {"text": "Margrit Leuthold", "label": "PERSON"},
    {"text": "ETH Zurich", "label": "ORG"}
  ],
  "keywords": ["Margrit Leuthold", "Executive Director", "Bangalore"],
  "summary": "Margrit Leuthold has been the Executive Director...",
  "text_stats": {"char_count": 864, "word_count": 128}
}
```

### After Step 2.1 (Metadata)
```json
{
  "id": "chunk_001",
  "chunk_summary": "Article about Margrit Leuthold's role as Executive Director",
  "entities": {
    "person": ["margrit leuthold"],
    "org": ["eth zurich"],
    "location": ["bangalore"]
  },
  "topic_tags": ["leadership", "administration"],
  "role_annotations": [{
    "person": "margrit leuthold",
    "role": "executive director",
    "from": 2020
  }],
  "department": ["administration"]
}
```

### After Step 2.2 (Scoring)
```json
{
  "1": {
    "relevance_score": 0.0,
    "relevance_reason": "Question about research, chunk about administration"
  },
  "5": {
    "relevance_score": 0.8,
    "relevance_reason": "Chunk directly mentions the person's role"
  }
}
```

## 🎯 Key Features by Stage

### Stage 1 Features
| Feature | Tool | Output |
|---------|------|--------|
| HTML parsing | BeautifulSoup + Docling | Clean text |
| Boilerplate removal | Regex (70+ patterns) | Focused content |
| Language detection | Lingua | EN/DE/FR/IT |
| Entity extraction | spaCy | Persons, orgs, locations |
| Keywords | YAKE | Top keywords |
| Summarization | spaCy + heuristics | Brief summary |
| Deduplication | Frequency counting | Unique paragraphs |

### Stage 2 Features
| Feature | Model | Output |
|---------|-------|--------|
| Metadata extraction | GPT-4o-mini | Structured JSON |
| Topic tagging | GPT-4o-mini | Topic labels |
| Event extraction | GPT-4o-mini | Temporal events |
| Role detection | GPT-4o-mini | Person-role pairs |
| Relevance scoring | GPT-4o-mini | 0.0-1.0 scores |

## 📈 Performance & Cost

### Stage 1 (Local)
- **Speed**: ~1-5 seconds per document
- **Cost**: $0 (runs locally)
- **Bottleneck**: Docling conversion
- **Scalability**: CPU-bound, parallelizable

### Stage 2 (API)
- **Speed**: ~2-10 seconds per chunk
- **Cost**: ~$0.03-0.05 per chunk
- **Bottleneck**: API rate limits
- **Scalability**: Network-bound, batch-friendly

### Example: 1000 Documents
- **Stage 1**: ~1-2 hours, $0
- **Stage 2**: ~3-5 hours, $30-50
- **Total**: ~4-7 hours, $30-50

## 🔧 Customization Points

1. **Boilerplate Patterns** (`step_1_2_*.py`, line 93)
   - Add domain-specific patterns
   - Adjust for different websites

2. **Repetition Threshold** (CLI flag `--threshold`)
   - Default: 5 occurrences
   - Increase for larger corpora

3. **Language Detection** (`step_1_2_*.py`, line 81)
   - Currently: EN/DE/FR/IT
   - Add more languages

4. **Entity Labels** (`step_1_2_*.py`, line 240)
   - Currently: All spaCy entities
   - Filter specific types

5. **LLM Parameters** (`2_1_*.py`)
   - Model: GPT-4o-mini
   - Can switch to GPT-4 for better quality

6. **Scoring Rubric** (`2_1_2_*.py`, line 37)
   - Adjust score thresholds
   - Modify criteria

## 🚦 Quality Checks

After each stage, verify:

### Stage 1.1
```bash
# Check output exists
ls data_cleaned/minimal_hybrid/*.json | wc -l

# Inspect sample
jq '.raw_text' data_cleaned/minimal_hybrid/sample.json
```

### Stage 1.2
```bash
# Check cleaning worked
jq '.paragraphs_cleaned | length' data_cleaned/advanced/*.json | sort -n

# Check metadata
jq '.language, .keywords[0:3]' data_cleaned/advanced/sample.json
```

### Stage 1.3
```bash
# Verify only valid docs remain
jq -r 'select(.paragraphs_cleaned | length == 0) | .doc_id' \
    data_cleaned/advanced_validated/*.json
# Should output nothing
```

### Stage 2.1
```bash
# Check metadata extracted
jq '.entities, .topic_tags[0:3]' benchmark/metadata/semantic/chunk_001.json
```

### Stage 2.2
```bash
# Check scores
jq 'to_entries | map(.value.relevance_score) | add / length' \
    benchmark/score/semantic/chunk_001.json
# Should output average score
```

## 💡 Pro Tips

1. **Incremental Processing**: Scripts skip processed files automatically
2. **Resume Anywhere**: Interrupted? Just re-run the same command
3. **Test First**: Start with 10 files before processing thousands
4. **Monitor Logs**: Set `logging.DEBUG` for detailed output
5. **Backup Regularly**: Keep copies at each stage
6. **Version Data**: Name output dirs with dates (`data_cleaned_2024_12_05/`)

---

**Ready to start?** Run `python verify_setup.py` to check everything is ready! 🚀

