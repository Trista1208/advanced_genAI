# 🚀 START HERE - Advanced GenAI Pipeline

Welcome! This is your entry point to the ETH Zurich document processing pipeline.

## ⚡ Quick Navigation

### 🆕 First Time User?
1. **Read**: [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
2. **Run**: `python verify_setup.py` - Check your environment
3. **Setup**: `./setup.sh` - Automated installation (or follow QUICKSTART.md)

### 📖 Need Detailed Info?
- **Complete Guide**: [README.md](README.md) - Full documentation
- **Visual Flow**: [PIPELINE_OVERVIEW.md](PIPELINE_OVERVIEW.md) - See how data flows
- **What Changed**: [CHANGELOG.md](CHANGELOG.md) - Recent improvements
- **Setup Status**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - What was configured

## 🎯 What This Pipeline Does

```
HTML Files → Clean Text → Metadata → Relevance Scores
   ↓            ↓           ↓              ↓
Stage 1.1   Stage 1.2   Stage 2.1     Stage 2.2
(Free)      (Free)      (~$0.001)     (~$0.002)
```

**Input**: Raw HTML documents (ETH Zurich content)  
**Output**: Structured JSON with metadata and relevance scores  
**Use Case**: RAG systems, semantic search, Q&A benchmarking

## 🏃 Quick Start (3 Commands)

```bash
# 1. Setup (one time)
./setup.sh

# 2. Verify
python verify_setup.py

# 3. Run pipeline
python step_1_hybrid.py data data_cleaned/minimal_hybrid
```

## 📂 Project Structure

```
advanced_genAI-main/
├── START_HERE.md              ← You are here
├── QUICKSTART.md              ← 5-minute guide
├── README.md                  ← Complete documentation
├── PIPELINE_OVERVIEW.md       ← Visual guide
├── requirements.txt           ← Dependencies
├── setup.sh                   ← Automated setup
├── verify_setup.py            ← Environment checker
│
├── step_1_*.py                ← Stage 1: Data processing
├── 2_1_*.py                   ← Stage 2: LLM enhancement
│
└── [data directories created by setup]
```

## ✅ Pre-Setup Checklist

Before running anything:
- [ ] Python 3.8+ installed
- [ ] OpenAI API key (for Stage 2 only)
- [ ] HTML files ready to process
- [ ] ~2 GB free disk space

## 🎓 Learning Path

### Beginner
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `verify_setup.py`
3. Process 5-10 test files
4. Inspect output JSON files

### Intermediate
1. Read [README.md](README.md) sections 1-3
2. Run full Stage 1 pipeline
3. Customize boilerplate patterns
4. Tune threshold parameter

### Advanced
1. Read [PIPELINE_OVERVIEW.md](PIPELINE_OVERVIEW.md)
2. Run Stage 2 with API
3. Integrate with your RAG system
4. Optimize for your use case

## 💡 Common Tasks

### "I want to process HTML files"
```bash
python step_1_hybrid.py data data_cleaned/minimal_hybrid
python step_1_2_advanced_cleaning_and_metadata.py \
    data_cleaned/minimal_hybrid data_cleaned/advanced --threshold 5
```

### "I want to extract Q&A from PDF"
```bash
python step_1_4_benchmark_extraction.py \
    benchmark/BenchmarkQuestionsAnswers.pdf \
    data_cleaned/benchmark_qa.json
```

### "I want to add metadata with AI"
```bash
# Requires OpenAI API key in .env
python 2_1_llm_metadataextraction.py --chunks subsample/semantic_chunk
```

### "I want to score relevance"
```bash
python 2_1_2_relevance_score.py --list-missing
python 2_1_2_relevance_score.py
```

## 🆘 Troubleshooting

### Setup Issues
```bash
python verify_setup.py  # Diagnose problems
```

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

### API Errors
```bash
cat .env  # Check API key is set
```

### Empty Output
- Check input files exist: `ls data/*.html`
- Review logs for errors
- Test with 1-2 files first

## 📊 What You Get

### Stage 1 Output (Free)
✅ Clean text (boilerplate removed)  
✅ Language detection  
✅ Named entities  
✅ Keywords  
✅ Summaries  

### Stage 2 Output (~$0.0015-0.003 per chunk, GPT-4o-mini)
✅ Structured metadata  
✅ Topic tags  
✅ Event dates  
✅ Role annotations  
✅ Relevance scores (0-1)  

## 🎯 Next Steps

1. **Setup**: Run `./setup.sh` or follow QUICKSTART.md
2. **Verify**: Run `python verify_setup.py`
3. **Test**: Process 5-10 files with Stage 1
4. **Scale**: Process full dataset
5. **Enhance**: Add Stage 2 if needed

## 📞 Need Help?

1. Check [README.md](README.md) troubleshooting section
2. Review error logs
3. Run `verify_setup.py` for diagnostics
4. Test with minimal data first

## 🎉 Ready?

**Start here**:
```bash
cat QUICKSTART.md
```

**Or jump right in**:
```bash
./setup.sh
python verify_setup.py
```

---

**Pro Tip**: Start with QUICKSTART.md, then refer to README.md for details! 🚀

**Last Updated**: December 2025

