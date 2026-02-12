**Food Establishments Inspection Analysis**

Analyzed 1.9M+ food safety inspection records across Chicago and Dallas to identify violation patterns, risk factors, and operational insights for public health departments.

**Problem Statement:** Public health departments struggle to prioritize inspections and allocate resources effectively due to:
- High volume of establishments requiring routine inspections
- Inconsistent violation tracking across jurisdictions
- Lack of visibility into recurring violation patterns
- Manual processes for risk assessment and resource allocation

**Business Impact:** Inefficient inspection scheduling leads to delayed identification of high-risk establishments, putting public health at risk and wasting limited health department resources.

**Proposed Solution:** A dimensional data warehouse integrating food inspection data from multiple cities, enabling:
- Standardized violation tracking and analysis
- Risk-based inspection prioritization
- Comparative analysis across jurisdictions
- Automated reporting for health department leadership

**Key Findings:**

**Chicago (267,866 inspections analyzed):**
- **27.4% of records missing violation data** - data quality issue requiring investigation
- **196,048 high-risk establishments** (Risk Category 1 & 2) requiring priority inspections
- **73,445 violations documented** across 166K+ unique violation types
- **Top violation categories:** Food temperature control, sanitation, pest management

**Dallas (78,400 inspections analyzed):**
- **72.2% missing data across violation fields** - systematic data collection issue
- **42 duplicate inspection records** identified and removed
- **25 violation categories** consolidated into standardized format
- **Average inspection score:** 85/100 (passing threshold: 70)

**Cross-City Insights:**
- Violation patterns differ significantly between cities (coding standards inconsistent)
- Chicago has more granular violation tracking (better data quality)
- Dallas uses numeric scoring system (more quantitative assessment)
- Need for standardized national food safety violation taxonomy

**Dataset Overview:**

**Chicago Food Inspections:**
- **Source:** City of Chicago Open Data Portal
- **Records:** 267,866 inspections (2010-2024)
- **Establishments:** 32,165 unique food businesses
- **Variables:** 17 columns (Inspection ID, License, DBA Name, Address, Risk, Results, Violations, etc.)

**Dallas Restaurant Inspections:**
- **Source:** Dallas Open Data Portal
- **Records:** 78,400 inspections (2019-2024)
- **Establishments:** 9,101 unique restaurants
- **Variables:** 114 columns (25 violation slots, scores, addresses, etc.)

**Data Quality Challenges:**
- Missing values (1.8% Chicago, 72.2% Dallas)
- Inconsistent violation formats (free text vs structured codes)
- Duplicate records (Dallas: 42 duplicates)
- Non-standardized risk classifications

**Tech Stack:**
- **ETL:** Talend Open Studio (integration), Python (pandas)
- **Database:** Microsoft SQL Server
- **Data Modeling:** ER/Studio (dimensional design)
- **Visualization:** Tableau
- **Data Profiling:** ydata-profiling, Alteryx

## Project Structure
```
Food-Establishments-Inspection/
├── README.md
├── Datasets/
│   ├── Raw/
│   │   ├── Chicago.tsv                 # Chicago food inspections (268K records)
│   │   └── Dallas.tsv                  # Dallas restaurant inspections (78K records)
│   └── Processed/
│       ├── Chicago - Cleaned.csv       # Normalized violation data
│       └── Dallas - Cleaned.csv        # Standardized format
├── Python/
│   └── Staged.py                       # Python cleaning script
├── ETL/
│   ├── Chicago/                        # Chicago ETL workflows
│   ├── Dallas/                         # Dallas ETL workflows
│   ├── Dimension/                      # Dimension table workflows
│   ├── Facts/                          # Fact table workflows
│   └── ETL_Workflow.docx               # Talend workflow documentation
├── Profiling/
│   ├── Chicago_Profiling.yxmd          # Alteryx data profiling workflow
│   ├── Dallas_Profiling.yxmd           # Alteryx data profiling workflow
│   └── Profiling_Workflows.docx        # Profiling process documentation
├── Model/
│   ├── Dimensional_Model.png           # Star schema diagram
│   └── Model_Script.docx               # DDL documentation
└── 
```

**Database Schema:** Star Schema Design

**Fact Tables (2):**
- `Fact_Inspection` - Core inspection events with scores and results
- `Fact_Violation` - Individual violations linked to inspections

**Dimension Tables (7):**
- `Dim_Business_License` - Establishment details (name, address, license)
- `Dim_Date` - Date hierarchy (year, quarter, month, week)
- `Dim_Facility_Type` - Restaurant, grocery, school cafeteria, etc.
- `Dim_Inspection_Type` - Routine, complaint-driven, license, reinspection
- `Dim_Risk_Category` - Risk levels (High, Medium, Low)
- `Dim_Food_Inspections_Results` - Pass, Fail, Pass with Conditions
- `Dim_Violation` - Violation codes, descriptions, comments

**Key Relationships:**
```
Dim_Business_License ──┐
Dim_Date ──────────────┤
Dim_Facility_Type ─────┤
Dim_Inspection_Type ───┼──> Fact_Inspection ──> Fact_Violation
Dim_Risk_Category ─────┤                              │
Dim_Results ───────────┘                              │
                                                      │
Dim_Violation ────────────────────────────────────────┘
```

**Total Records in Warehouse:**
- 346,266 inspections
- 1.2M+ violation records (after normalization)
- 40K+ unique establishments

**Technical Implementation:**

**ETL Pipeline:**

**Phase 1: Data Extraction:**
- Downloaded TSV files from city open data portals
- Initial profiling with ydata-profiling and Alteryx

**Phase 2: Data Quality Assessment:**
Identified issues:
- Missing violation data (27% Chicago, 72% Dallas)
- Inconsistent violation formats (text blocks vs structured fields)
- Duplicate records
- Invalid date formats
- Truncated text fields

**Phase 3: Data Transformation:**

**Chicago Processing:**
- Normalized violations column (split pipe-delimited text into separate rows)
- Extracted violation code, description, comment using regex
- Added DI metadata (Process ID, Current Date, Workflow name)
- Calculated risk scores and violation points

**Dallas Processing:**
- Consolidated 25 violation columns into single normalized structure
- Mapped violation points to standardized scale
- Standardized facility types
- Created default risk categories

**Phase 4: Data Loading:**
- Loaded staged data into SQL Server
- Populated dimensional model using Talend
- Applied surrogate keys and SCD Type 1 logic
- Validated referential integrity

**Data Profiling Results:**

**Chicago Data Quality:**
- 17 variables, 267,866 observations
- 84,184 missing cells (1.8%)
- 0 duplicates
- Key issues: Violations column missing in 27% of records

**Dallas Data Quality:**
- 114 variables, 78,400 observations
- 6.4M missing cells (72.2% - sparse violation matrix)
- 42 duplicate records removed
- Key issues: 99%+ missing in violation detail fields 11-25

**SQL Capabilities Demonstrated:**
- **Dimensional Modeling:** Star schema with 7 dimensions, 2 facts  
- **DDL Design:** Foreign keys, constraints, indexes  
- **Data Validation:** Integrity checks, duplicate detection  
- **ETL Logic:** Staging → integration → dimensional model  
- **Data Quality:** Profiling, missing value handling, normalization  

**Visualizations:**

**Tableau Dashboards:**
1. **Executive Overview** - Total inspections, pass/fail rates, trend analysis
2. **Violation Analysis** - Top violations by frequency and severity
3. **Geographic Distribution** - Heat map of high-risk establishments by neighborhood
4. **Comparative Analysis** - Chicago vs Dallas metrics side-by-side

**For dashboard previews, see [Tableau folder](tableau/)**

**Installation & Reproducibility:**

 Prerequisites:
- Python 3.8+ (pandas, re, datetime)
- Microsoft SQL Server
- Tableau Desktop (for .twb file) or Tableau Public

 Setup Instructions:

**1. Clone repository:**
```bash
git clone https://github.com/lakshmi14k/Food-Establishments-Inspection.git
```

**2. Run Python cleaning script:**
```bash
cd data/raw
python ../../python/clean_data.py
```
Output: `Chicago - Cleaned.csv`, `Dallas - Cleaned.csv` in `data/processed/`

**3. Create database and load schema:**
```sql
-- Run in SQL Server Management Studio
CREATE DATABASE FoodInspections;
GO

-- Execute DDL script
USE FoodInspections;
GO
-- Run sql/DDL_Script.sql
```

**4. Load data using ETL tool (Talend):**
- Original implementation: Talend Open Studio (workflows in `etl/` folder)
- Alternative: Use Python pandas to load CSVs directly to SQL Server

**5. Run validation checks:**
```sql
-- Execute sql/Validation_Script.sql
```

**6. Open Tableau dashboards:**
- Connect to SQL Server database OR
- Use processed CSV files from `data/processed/`

**Results:**

**Data Pipeline:**
- 346K+ inspection records integrated
- 1.2M+ violation records normalized
- 40K+ unique establishments profiled
- 9 dimensional/fact tables populated

**Insights Delivered:**
- Identified systematic data quality issues (72% missing Dallas data)
- Documented top 10 violation categories per city
- Mapped high-risk establishment concentrations
- Enabled trend analysis (inspection frequency, pass rates over time)

**Business Value:**
- Prioritized inspection scheduling based on risk scores
- Identified establishments requiring follow-up (failed inspections)
- Enabled resource allocation optimization
- Provided comparative benchmarking across cities

**Key Technical Achievements**
- **ETL Pipeline:** Multi-source integration (2 cities, different schemas)  
- **Data Quality:** Handled 72% missing data without losing analytical value  
- **Normalization:** Transformed wide format (114 columns) to normalized structure  
- **Dimensional Modeling:** Star schema with proper grain and relationships  
- **Data Profiling:** Comprehensive quality assessment before transformation  
- **Regex Parsing:** Extracted structured data from unstructured text fields  

 Built with _SQL Server, Python, Alteryx, Talend, and Tableau_

