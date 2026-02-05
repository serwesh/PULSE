# PULSE Version 2 - Project Organization

## 📁 Folder Structure

```
PULSE_Version2/
├── 📂 apps/                      # Streamlit UI application
│   ├── app.py                    # Main Streamlit app
│   ├── styles.py                 # UI styling
│   └── ...
│
├── 📂 data_generators/           # Data generation scripts
│   ├── generate_enhanced_data.py # Main generator (1.4-4.5 GHz, 7 emitters)
│   └── generate_xband_data.py    # X-band generator (7-8 GHz)
│
├── 📂 generated_datasets/        # Generated data files
│   ├── generated_data_60k_enhanced.csv    # Enhanced dataset (CSV)
│   ├── generated_data_60k_enhanced.xlsx   # Enhanced dataset (Excel)
│   ├── generated_xband_data.csv           # X-band dataset (CSV)
│   └── generated_xband_data.xlsx          # X-band dataset (Excel)
│
├── 📂 analysis_scripts/          # Data analysis and comparison scripts
│   ├── analyze_excel.py          # Analyze original Excel data
│   ├── compare_datasets.py       # Compare datasets
│   ├── compare_enhanced_data.py  # Enhanced data comparison
│   ├── compare_final_vs_improved.py
│   ├── compare_with_plots.py
│   └── comprehensive_analysis.py
│
├── 📂 documentation/             # All documentation files
│   ├── COMPLETE_SUMMARY.md       # Complete implementation summary
│   ├── DATA_GENERATION_GUIDE.md  # Data generation guide
│   ├── XBAND_DATA_DOCUMENTATION.md # X-band data docs
│   ├── UI_IMPROVEMENTS.md        # UI enhancements
│   ├── TWO_WORKFLOWS_EXPLAINED.md # Workflow explanation
│   ├── QUICK_REFERENCE.md        # Quick reference
│   └── ... (all other .md files)
│
├── 📂 archived/                  # Archived/old files
│   ├── generate_similar_data.py  # Old generators
│   ├── generate_improved_data.py
│   ├── generate_final_optimized_data.py
│   └── generated_data_60k*.csv/xlsx # Old datasets
│
├── 📂 src/                       # Source code
│   ├── pdw_simulator/            # PDW simulation modules
│   ├── radar/                    # Radar models
│   ├── antenna/                  # Antenna patterns
│   └── ...
│
├── 📂 config/                    # Configuration files
│   ├── tomlconfig.yaml           # Base configuration
│   └── ...
│
├── 📂 output/                    # Simulation outputs
├── 📂 comparison_plots/          # Comparison plots
├── 📂 enhanced_comparison_plots/ # Enhanced comparison plots
├── 📂 tests/                     # Unit tests
├── 📂 docs/                      # Additional documentation
│
├── 📄 DS_EtfRecordS6.xlsx        # Original dataset
├── 📄 README.md                  # Main README
├── 📄 PROJECT_STRUCTURE.md       # This file
├── 📄 CONTRIBUTING.md            # Contribution guidelines
├── 📄 CONTRIBUTORS.md            # Contributors list
├── 📄 LICENSE                    # License file
├── 📄 requirements.txt           # Python dependencies
├── 📄 setup.py                   # Setup script
└── 📄 pyproject.toml             # Project configuration
```

---

## 🎯 Quick Navigation

### For Data Generation
→ Go to `data_generators/`
- `generate_enhanced_data.py` - Main generator (1.4-4.5 GHz)
- `generate_xband_data.py` - X-band generator (7-8 GHz)

### For Generated Data
→ Go to `generated_datasets/`
- Latest enhanced dataset
- X-band dataset

### For Analysis
→ Go to `analysis_scripts/`
- Various comparison and analysis tools

### For Documentation
→ Go to `documentation/`
- All guides and summaries
- Quick references

### For UI
→ Go to `apps/`
- Streamlit application

---

## 🚀 Quick Start

### 1. Generate Data
```bash
cd data_generators
conda activate us_ml

# Enhanced dataset (1.4-4.5 GHz)
python generate_enhanced_data.py --rows 60000 --emitters 7

# X-band dataset (7-8 GHz)
python generate_xband_data.py --rows 60000 --emitters 7
```

### 2. Run UI
```bash
cd ..
streamlit run apps/app.py
```

### 3. Analyze Data
```bash
cd analysis_scripts
python compare_enhanced_data.py
```

---

## 📚 Documentation Index

### Getting Started
- `README.md` - Project overview
- `documentation/QUICK_REFERENCE.md` - Quick commands
- `documentation/QUICK_START_GUIDE.md` - Detailed guide

### Data Generation
- `documentation/DATA_GENERATION_GUIDE.md` - Complete generation guide
- `documentation/XBAND_DATA_DOCUMENTATION.md` - X-band specifics
- `documentation/TWO_WORKFLOWS_EXPLAINED.md` - Workflow comparison

### Implementation Details
- `documentation/COMPLETE_SUMMARY.md` - Full implementation
- `documentation/ENHANCEMENTS_SUMMARY.md` - Enhancement details
- `documentation/ELEVATION_FIX_SUMMARY.md` - Elevation column fix

### UI Documentation
- `documentation/UI_IMPROVEMENTS.md` - UI enhancements
- `documentation/CONFLICT_RESOLUTION.md` - Workflow clarification

---

## 🔧 Main Components

### 1. Data Generators (`data_generators/`)
**Purpose**: Generate realistic radar pulse data

**Files**:
- `generate_enhanced_data.py` - Enhanced generator with TOD, FreqType, PriType
- `generate_xband_data.py` - X-band specific generator (7-8 GHz)

**Usage**:
```bash
python generate_enhanced_data.py --rows 60000 --emitters 7
python generate_xband_data.py --rows 60000 --emitters 7
```

### 2. Streamlit UI (`apps/`)
**Purpose**: Interactive visualization and analysis

**Features**:
- 4 tabs: Visualizations, TOD Analysis, Data Analysis, Raw Data
- Interactive Plotly charts
- TOD timeline and interval analysis
- Emitter activity tracking

**Usage**:
```bash
streamlit run apps/app.py
```

### 3. Analysis Scripts (`analysis_scripts/`)
**Purpose**: Data comparison and validation

**Files**:
- `analyze_excel.py` - Analyze original data
- `compare_enhanced_data.py` - Compare generated vs original
- Various comparison tools

### 4. Generated Datasets (`generated_datasets/`)
**Purpose**: Store generated data files

**Current Files**:
- `generated_data_60k_enhanced.csv/xlsx` - Enhanced dataset
- `generated_xband_data.csv/xlsx` - X-band dataset

---

## 📊 Dataset Information

### Enhanced Dataset (1.4-4.5 GHz)
- **Frequency Range**: 1362-4545 MHz (L/S-band)
- **Emitters**: 7 (S1, T, J, S4, F, S3, S2)
- **Rows**: 60,000
- **Columns**: 10 (including TOD, FreqType, PriType)
- **File**: `generated_datasets/generated_data_60k_enhanced.csv`

### X-Band Dataset (7-8 GHz)
- **Frequency Range**: 7000-8000 MHz (X-band)
- **Emitters**: 7 (XR1-XR7)
- **Rows**: 60,000
- **Columns**: 10 (including TOD, FreqType, PriType)
- **File**: `generated_datasets/generated_xband_data.csv`

---

## 🗂️ Archived Files

Old/deprecated files are in `archived/`:
- Old generator versions
- Previous dataset versions
- Superseded by current implementations

---

## 📝 Notes

### File Organization Principles
1. **Separation of Concerns**: Generators, data, analysis, docs separated
2. **Clear Naming**: Descriptive folder and file names
3. **Easy Navigation**: Logical structure for quick access
4. **Archive Old Files**: Keep history without clutter

### Maintenance
- Keep `generated_datasets/` for latest data only
- Archive old datasets to `archived/`
- Update documentation in `documentation/`
- Keep root directory clean

---

## 🔗 Related Files

- `README.md` - Main project README
- `CONTRIBUTING.md` - How to contribute
- `CONTRIBUTORS.md` - List of contributors
- `LICENSE` - Project license

---

## 📞 Support

For questions or issues:
1. Check `documentation/` for guides
2. Review `documentation/QUICK_REFERENCE.md`
3. See `documentation/TWO_WORKFLOWS_EXPLAINED.md` for workflow help

---

**Last Updated**: 2026-01-19
**Organization**: Complete ✅
