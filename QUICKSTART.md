# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup (One-Time)

```bash
# Clone or navigate to the repository
cd advanced_genAI-main

# Run automated setup (Linux/Mac)
chmod +x setup.sh
./setup.sh

# OR manual setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python setup_directories.py
```

### 2. Configure

```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Place your data
# - HTML files → data/
# - Benchmark PDF → benchmark/
```

### 3. Run Pipeline

#### Stage 1: Data Processing (No API cost)

```bash
# Activate environment
source venv/bin/activate

# Step 1.1: Extract text from HTML
python step_1_hybrid.py data data_cleaned/minimal_hybrid

# Step 1.2: Clean and extract metadata
python step_1_2_advanced_cleaning_and_metadata.py \
    data_cleaned/minimal_hybrid \
    data_cleaned/advanced \
    --threshold 5

# Step 1.3: Filter empty documents
python step_1_3_validation_filter.py \
    data_cleaned/advanced \
    data_cleaned/advanced_validated

# Step 1.4: Extract Q&A from PDF (optional)
python step_1_4_benchmark_extraction.py \
    benchmark/BenchmarkQuestionsAnswers.pdf \
    data_cleaned/benchmark_qa.json
```

#### Stage 2: LLM Enhancement (Costs money)

```bash
# Step 2.1: Extract metadata with GPT-4o-mini
python 2_1_llm_metadataextraction.py \
    --chunks subsample/semantic_chunk

# Step 2.2: Score relevance to benchmark questions
# First check what needs scoring
python 2_1_2_relevance_score.py --list-missing

# Then score missing chunks
python 2_1_2_relevance_score.py
```

## 📊 What You Get

### After Stage 1
✅ Clean, structured text from HTML  
✅ Language detection (EN/DE/FR/IT)  
✅ Named entities (persons, orgs, locations)  
✅ Keywords extracted  
✅ Automatic summaries  
✅ Boilerplate removed (70+ patterns)  
✅ Q&A pairs from PDF  

### After Stage 2
✅ Rich metadata per chunk  
✅ Topic tags  
✅ Event dates  
✅ Role annotations  
✅ Numeric facts  
✅ Relevance scores (0-1) for 25 questions  

## 🎯 Typical Workflow

```bash
# Morning: Start Stage 1 processing
python step_1_hybrid.py data data_cleaned/minimal_hybrid
python step_1_2_advanced_cleaning_and_metadata.py \
    data_cleaned/minimal_hybrid data_cleaned/advanced --threshold 5
python step_1_3_validation_filter.py \
    data_cleaned/advanced data_cleaned/advanced_validated

# Check quality
ls -lh data_cleaned/advanced_validated/
head -n 50 data_cleaned/advanced_validated/sample.json | jq .

# Afternoon: Chunk documents (your chunking script)
# [Your chunking step here]

# Evening: Run LLM steps (or overnight for large datasets)
python 2_1_llm_metadataextraction.py --chunks subsample/semantic_chunk
python 2_1_2_relevance_score.py

# Next day: Analyze results
python analyze_results.py  # Your analysis script
```

## 💰 Cost Estimation

**Stage 1**: Free (local processing)

**Stage 2** (OpenAI API with GPT-4o-mini):
- Metadata extraction: ~$0.0005-0.001 per chunk
- Relevance scoring: ~$0.001-0.002 per chunk
- **Total**: ~$0.0015-0.003 per chunk

For 1000 chunks: ~$1.50-$3.00

**Note**: Based on GPT-4o-mini pricing ($0.15/1M input tokens, ~$0.60/1M output tokens). Always test with a small batch first and monitor your actual usage.

## 🔍 Verify Output

```bash
# Check Stage 1 output
jq '.main_content, .language, .keywords' \
    data_cleaned/advanced_validated/sample.json

# Check Stage 2 metadata
jq '.entities, .topic_tags' \
    benchmark/metadata/semantic/chunk_001.json

# Check relevance scores
jq '."1", ."2", ."3"' \
    benchmark/score/semantic/chunk_001.json
```

## ⚠️ Common Issues

**"Module not found"**: Run `pip install -r requirements.txt`  
**"spaCy model not found"**: Run `python -m spacy download en_core_web_sm`  
**"OpenAI API error"**: Check your `.env` file has valid API key  
**Empty output**: Verify input files exist in correct directories  

## 📖 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [CHANGELOG.md](CHANGELOG.md) for recent updates
- Customize boilerplate patterns in `step_1_2_advanced_cleaning_and_metadata.py`
- Tune `--threshold` parameter based on your corpus size

## 🆘 Need Help?

1. Check the troubleshooting section in [README.md](README.md)
2. Review script logs for error messages
3. Test with small dataset first (5-10 files)
4. Verify all dependencies installed correctly

---

**Ready to process thousands of documents?** Start with 10 files first to test! 🎉

