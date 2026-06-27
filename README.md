# 🎯 Recruitment Funnel Intelligence

### Hiring Pipeline Analytics — Source ROI • Funnel Optimization • Recruiter Productivity

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![SQL](https://img.shields.io/badge/SQL-Analytics-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

---

## 🎯 Problem Statement

Companies spend **$4,000-$7,000 per hire** but rarely measure pipeline efficiency. This project analyzes **10,000 candidates** flowing through a 4-stage hiring funnel to identify **where candidates drop off, which sources deliver best ROI, and how to reduce time-to-hire**.

---

## 🔑 Key Findings

| KPI | Value | Benchmark |
|-----|-------|-----------|
| Overall Conversion Rate | 2.5% | 2-5% (industry avg) |
| Avg Time to Hire | 35 days | 30-45 days |
| Best Source | Employee Referral (5.2% hire rate) | — |
| Worst Bottleneck | Screening stage (70% drop-off) | — |
| Offer Accept Rate | 81% | 75-85% |
| Most Efficient Dept | HR (3.8% conversion) | — |

---

## 🏗️ Architecture

```
5,000 Candidates → Screening (29.6%) → Interview (9.9%) → Offer (3.1%) → Hire (2.5%)
                         ↓                    ↓                 ↓
                   70% drop off          67% drop off      19% decline
```

---

## 🖥️ Dashboard Features

| Tab | Analytics |
|-----|-----------|
| 🔄 **Funnel Analysis** | Visual funnel chart, stage-to-stage conversion, department breakdown |
| 📊 **Source ROI** | Hire rate by channel, applications-per-hire, cost efficiency |
| 👤 **Recruiter Performance** | Scorecard: hires, speed, quality (speed vs conversion scatter) |
| 📈 **Trends & Time** | Monthly trends, time-to-hire distribution, cumulative tracking |
| 📋 **Rejection Analysis** | Drop-off points, rejection reasons, offer decline deep dive |

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Programming | Python 3.11, SQL |
| Data | Pandas, NumPy |
| Visualization | Plotly (interactive funnel, scatter, bar charts) |
| Dashboard | Streamlit (responsive, filterable) |
| Database | SQLite |

---

## 🚀 Quick Start

```bash
git clone https://github.com/priyabiradar59/recruitment-funnel-intelligence.git
cd recruitment-funnel-intelligence
pip install -r requirements.txt
python src/generate_data.py
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```
├── dashboard/app.py              # Interactive Streamlit dashboard (5 tabs)
├── src/
│   └── generate_data.py          # Synthetic data generator (industry benchmarks)
├── sql/
│   └── recruitment_funnel_queries.sql  # 8 advanced SQL queries
├── data/raw/                     # Generated recruitment dataset (10,000 candidates)
├── requirements.txt
└── README.md
```

---

## 📊 SQL Skills Demonstrated

| # | Query | Concepts |
|---|-------|----------|
| 1 | Full Funnel Conversion | UNION ALL, aggregations |
| 2 | Source ROI Ranking | CTE, RANK() OVER, Window Functions |
| 3 | Recruiter Scorecard | GROUP BY, multiple metrics |
| 4 | Monthly Trends | LAG(), running totals, MoM change |
| 5 | Department Funnel | Multi-stage conversion calculation |
| 6 | Rejection Analysis | Window Functions, PARTITION BY |
| 7 | Time-to-Hire Quartiles | NTILE(4), GROUP_CONCAT |
| 8 | Offer Decline Analysis | Salary gap, conditional aggregation |

---

## 💡 Business Recommendations

1. **Double referral bonus** — Referrals convert at 5.2% vs 1.8% for job boards
2. **Fix screening bottleneck** — 70% of candidates drop at screening; automate initial filters
3. **Close salary gaps** — Engineering offer declines driven by salary mismatch
4. **Set SLA: 3-day screen** — Top candidates accept other offers if screened too slowly
5. **Recruiter coaching** — Share top performer's techniques with the team

---

## 👩‍💻 Author

**Priyanka S Biradar**  
HR Analyst @ Goldman Sachs → Data Analyst  
3.8 years experience in TA reporting, hiring analytics, and recruitment KPIs

[![GitHub](https://img.shields.io/badge/GitHub-priyabiradar59-181717?style=flat&logo=github)](https://github.com/priyabiradar59)
