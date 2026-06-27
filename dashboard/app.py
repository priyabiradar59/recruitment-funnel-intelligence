# ============================================================================
# dashboard/app.py — Recruitment Funnel Intelligence Dashboard
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(
    page_title="Recruitment Funnel Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main .block-container { padding: 1rem 2rem; max-width: 100%; }
    .kpi-card {
        border-radius: 12px; padding: 1.2rem; text-align: center;
        color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 0.8rem;
    }
    .kpi-value { font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 700; margin: 0; }
    .kpi-label { font-size: clamp(0.75rem, 2vw, 0.9rem); opacity: 0.9; margin: 0; }
    .kpi-blue { background: linear-gradient(135deg, #3498db, #2980b9); }
    .kpi-green { background: linear-gradient(135deg, #2ecc71, #27ae60); }
    .kpi-orange { background: linear-gradient(135deg, #f39c12, #e67e22); }
    .kpi-red { background: linear-gradient(135deg, #e74c3c, #c0392b); }
    .kpi-purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
    .kpi-teal { background: linear-gradient(135deg, #1abc9c, #16a085); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap; }
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "raw" / "recruitment_funnel_data.csv"
    return pd.read_csv(path)

df = load_data()

# --- Sidebar Filters ---
with st.sidebar:
    st.title("🎯 Filters")
    st.markdown("---")
    dept_filter = st.selectbox("Department", ['All'] + sorted(df['Department'].unique().tolist()))
    source_filter = st.selectbox("Source", ['All'] + sorted(df['Source'].unique().tolist()))
    recruiter_filter = st.selectbox("Recruiter", ['All'] + sorted(df['Recruiter'].unique().tolist()))
    exp_filter = st.selectbox("Experience", ['All'] + sorted(df['ExperienceLevel'].unique().tolist()))
    quarter_filter = st.selectbox("Quarter", ['All'] + sorted(df['Quarter'].unique().tolist()))

# Apply filters
fdf = df.copy()
if dept_filter != 'All': fdf = fdf[fdf['Department'] == dept_filter]
if source_filter != 'All': fdf = fdf[fdf['Source'] == source_filter]
if recruiter_filter != 'All': fdf = fdf[fdf['Recruiter'] == recruiter_filter]
if exp_filter != 'All': fdf = fdf[fdf['ExperienceLevel'] == exp_filter]
if quarter_filter != 'All': fdf = fdf[fdf['Quarter'] == quarter_filter]

# --- Header ---
st.markdown("""
<h1 style='text-align:center; color:#2c3e50;'>🎯 Recruitment Funnel Intelligence</h1>
<p style='text-align:center; color:#7f8c8d;'>Hiring Pipeline Analytics — Source ROI • Funnel Optimization • Recruiter Performance</p>
""", unsafe_allow_html=True)

# --- KPI Cards ---
total = len(fdf)
hires = fdf['Hired'].sum()
conversion = hires / total * 100 if total > 0 else 0
avg_tth = fdf[fdf['Hired']==1]['TimeToHire'].mean() if hires > 0 else 0
offer_accept = fdf[fdf['Offered']==1]['Hired'].mean() * 100 if fdf['Offered'].sum() > 0 else 0
pipeline_velocity = fdf['Screened'].sum() / total * 100 if total > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.markdown(f'<div class="kpi-card kpi-blue"><p class="kpi-value">{total:,}</p><p class="kpi-label">Applications</p></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card kpi-green"><p class="kpi-value">{hires}</p><p class="kpi-label">Hires Made</p></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card kpi-purple"><p class="kpi-value">{conversion:.1f}%</p><p class="kpi-label">Conversion Rate</p></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card kpi-orange"><p class="kpi-value">{avg_tth:.0f} days</p><p class="kpi-label">Avg Time to Hire</p></div>', unsafe_allow_html=True)
c5.markdown(f'<div class="kpi-card kpi-teal"><p class="kpi-value">{offer_accept:.0f}%</p><p class="kpi-label">Offer Accept Rate</p></div>', unsafe_allow_html=True)
c6.markdown(f'<div class="kpi-card kpi-red"><p class="kpi-value">{pipeline_velocity:.0f}%</p><p class="kpi-label">Screen Rate</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔄 Funnel Analysis", "📊 Source ROI", "👤 Recruiter Performance",
    "📈 Trends & Time", "📋 Rejection Analysis", "🎯 Executive Summary"
])

# ===== TAB 1: FUNNEL =====
with tab1:
    st.subheader("Hiring Funnel — Stage by Stage Conversion")
    
    funnel_data = {
        'Stage': ['Applied', 'Screened', 'Interviewed', 'Offered', 'Hired'],
        'Count': [total, fdf['Screened'].sum(), fdf['Interviewed'].sum(), fdf['Offered'].sum(), hires],
    }
    funnel_df = pd.DataFrame(funnel_data)
    funnel_df['Conversion'] = (funnel_df['Count'] / total * 100).round(1)
    funnel_df['Drop_off'] = funnel_df['Count'].diff().fillna(0).astype(int)
    
    # Funnel chart
    fig = go.Figure(go.Funnel(
        y=funnel_df['Stage'],
        x=funnel_df['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c']),
        connector=dict(line=dict(color="gray", width=1))
    ))
    fig.update_layout(title='<b>Recruitment Funnel</b>', height=450)
    st.plotly_chart(fig, width="stretch")
    
    # Stage conversion rates
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Stage-to-Stage Conversion")
        stage_conv = pd.DataFrame({
            'Transition': ['Applied → Screened', 'Screened → Interviewed', 'Interviewed → Offered', 'Offered → Hired'],
            'Rate': [
                f"{fdf['Screened'].sum()/total*100:.1f}%" if total > 0 else "0%",
                f"{fdf['Interviewed'].sum()/fdf['Screened'].sum()*100:.1f}%" if fdf['Screened'].sum() > 0 else "0%",
                f"{fdf['Offered'].sum()/fdf['Interviewed'].sum()*100:.1f}%" if fdf['Interviewed'].sum() > 0 else "0%",
                f"{hires/fdf['Offered'].sum()*100:.1f}%" if fdf['Offered'].sum() > 0 else "0%",
            ],
            'Benchmark': ['25-30%', '40-50%', '20-25%', '75-85%']
        })
        st.dataframe(stage_conv, width="stretch", hide_index=True)
    
    with col2:
        # Department funnel comparison
        dept_funnel = fdf.groupby('Department').agg(
            Applied=('CandidateID', 'count'),
            Screened=('Screened', 'sum'),
            Interviewed=('Interviewed', 'sum'),
            Offered=('Offered', 'sum'),
            Hired=('Hired', 'sum')
        ).reset_index()
        dept_funnel['Conversion%'] = (dept_funnel['Hired'] / dept_funnel['Applied'] * 100).round(1)
        
        fig = px.bar(dept_funnel.sort_values('Conversion%', ascending=True),
                    x='Conversion%', y='Department', orientation='h',
                    title='<b>Overall Conversion by Department</b>',
                    color='Conversion%', color_continuous_scale='RdYlGn')
        fig.update_layout(height=300)
        st.plotly_chart(fig, width="stretch")

# ===== TAB 2: SOURCE ROI =====
with tab2:
    st.subheader("Source Channel Effectiveness — Where to Invest")
    
    source_data = fdf.groupby('Source').agg(
        Applied=('CandidateID', 'count'),
        Screened=('Screened', 'sum'),
        Interviewed=('Interviewed', 'sum'),
        Offered=('Offered', 'sum'),
        Hired=('Hired', 'sum'),
        Avg_TTH=('TimeToHire', lambda x: x[fdf.loc[x.index, 'Hired']==1].mean())
    ).reset_index()
    source_data['Hire_Rate%'] = (source_data['Hired'] / source_data['Applied'] * 100).round(2)
    source_data['Apps_per_Hire'] = (source_data['Applied'] / source_data['Hired'].replace(0, np.nan)).round(0)
    source_data = source_data.sort_values('Hire_Rate%', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(source_data, x='Source', y='Hire_Rate%',
                    title='<b>Hire Rate by Source (%)</b>',
                    color='Hire_Rate%', color_continuous_scale='Greens',
                    text='Hire_Rate%')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        fig = px.bar(source_data, x='Source', y='Apps_per_Hire',
                    title='<b>Applications Needed per Hire</b>',
                    color='Apps_per_Hire', color_continuous_scale='RdYlGn_r',
                    text='Apps_per_Hire')
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    st.dataframe(source_data[['Source','Applied','Hired','Hire_Rate%','Apps_per_Hire']],
                width="stretch", hide_index=True)
    
    st.info("💡 **Insight**: Employee Referrals have the highest hire rate but lowest volume. Recommendation: Increase referral bonus to drive more referral applications.")

# ===== TAB 3: RECRUITER PERFORMANCE =====
with tab3:
    st.subheader("Recruiter Scorecard")
    
    recruiter_data = fdf.groupby('Recruiter').agg(
        Candidates=('CandidateID', 'count'),
        Hires=('Hired', 'sum'),
        Offers_Made=('Offered', 'sum'),
        Avg_TTH=('TimeToHire', lambda x: x[fdf.loc[x.index, 'Hired']==1].mean())
    ).reset_index()
    recruiter_data['Conversion%'] = (recruiter_data['Hires'] / recruiter_data['Candidates'] * 100).round(1)
    recruiter_data['Offer_Accept%'] = (recruiter_data['Hires'] / recruiter_data['Offers_Made'].replace(0, np.nan) * 100).round(1)
    recruiter_data['Avg_TTH'] = recruiter_data['Avg_TTH'].round(0)
    recruiter_data = recruiter_data.sort_values('Hires', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(recruiter_data, x='Recruiter', y='Hires',
                    title='<b>Hires per Recruiter</b>',
                    color='Conversion%', color_continuous_scale='Greens',
                    text='Hires')
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        fig = px.scatter(recruiter_data, x='Avg_TTH', y='Conversion%',
                        size='Candidates', color='Recruiter',
                        title='<b>Speed vs Quality (Ideal: Top-Left)</b>',
                        labels={'Avg_TTH': 'Avg Time to Hire (days)', 'Conversion%': 'Conversion Rate (%)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    st.dataframe(recruiter_data, width="stretch", hide_index=True)

# ===== TAB 4: TRENDS =====
with tab4:
    st.subheader("Hiring Trends Over Time")
    
    monthly = fdf.groupby('Month').agg(
        Applications=('CandidateID', 'count'),
        Hires=('Hired', 'sum'),
        Avg_TTH=('TimeToHire', lambda x: x[fdf.loc[x.index, 'Hired']==1].mean())
    ).reset_index()
    monthly['Hire_Rate%'] = (monthly['Hires'] / monthly['Applications'] * 100).round(1)
    monthly['Cumulative_Hires'] = monthly['Hires'].cumsum()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly['Month'], y=monthly['Applications'],
                        name='Applications', marker_color='#3498db', opacity=0.6), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Cumulative_Hires'],
                            name='Cumulative Hires', line=dict(color='#e74c3c', width=3),
                            mode='lines+markers'), secondary_y=True)
    fig.update_layout(title='<b>Monthly Applications vs Cumulative Hires</b>', height=400)
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Applications", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Hires", secondary_y=True)
    st.plotly_chart(fig, width="stretch")
    
    # Time to hire distribution
    col1, col2 = st.columns(2)
    with col1:
        hired_df = fdf[fdf['Hired'] == 1]
        if len(hired_df) > 0:
            fig = px.histogram(hired_df, x='TimeToHire', nbins=20,
                              title='<b>Time to Hire Distribution (Days)</b>',
                              color_discrete_sequence=['#9b59b6'])
            fig.add_vline(x=hired_df['TimeToHire'].median(), line_dash="dash",
                         annotation_text=f"Median: {hired_df['TimeToHire'].median():.0f} days")
            fig.update_layout(height=350)
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        fig = px.box(fdf[fdf['Hired']==1], x='Department', y='TimeToHire',
                    title='<b>Time to Hire by Department</b>',
                    color='Department')
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, width="stretch")

# ===== TAB 5: REJECTIONS =====
with tab5:
    st.subheader("Where & Why Candidates Drop Off")
    
    rejected = fdf[fdf['Hired'] == 0].dropna(subset=['RejectionStage'])
    
    col1, col2 = st.columns(2)
    with col1:
        stage_counts = rejected['RejectionStage'].value_counts().reset_index()
        stage_counts.columns = ['Stage', 'Count']
        fig = px.pie(stage_counts, values='Count', names='Stage',
                    title='<b>Rejection by Stage</b>',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        reason_counts = rejected['RejectionReason'].value_counts().head(10).reset_index()
        reason_counts.columns = ['Reason', 'Count']
        fig = px.bar(reason_counts, x='Count', y='Reason', orientation='h',
                    title='<b>Top Rejection Reasons</b>',
                    color='Count', color_continuous_scale='Reds')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    # Offer decline deep dive
    st.markdown("#### 🚨 Offer Declines — Lost Candidates")
    offer_declines = fdf[(fdf['Offered']==1) & (fdf['Hired']==0)]
    if len(offer_declines) > 0:
        decline_by_dept = offer_declines.groupby('Department').agg(
            Declines=('CandidateID', 'count'),
            Avg_Expected_Salary=('ExpectedSalary_LPA', 'mean'),
            Avg_Offered_Salary=('OfferedSalary_LPA', 'mean')
        ).round(1).reset_index()
        decline_by_dept['Salary_Gap'] = (decline_by_dept['Avg_Expected_Salary'] - decline_by_dept['Avg_Offered_Salary']).round(1)
        st.dataframe(decline_by_dept, width="stretch", hide_index=True)
        st.warning("💡 **Finding**: Salary gap between expectation and offer is a key decline driver. Engineering has the widest gap.")

# ===== TAB 6: EXECUTIVE SUMMARY =====
with tab6:
    st.subheader("🎯 Executive Summary — Stakeholder View")
    st.markdown("*High-level insights for leadership — clear, actionable, visual.*")
    st.markdown("---")
    
    # --- Hiring Health Score (Gauge Chart) ---
    col1, col2, col3 = st.columns(3)
    
    # Calculate health metrics
    screen_rate_val = fdf['Screened'].sum() / len(fdf) * 100 if len(fdf) > 0 else 0
    offer_rate_val = fdf['Hired'].sum() / max(fdf['Offered'].sum(), 1) * 100
    speed_score = max(0, 100 - (avg_tth - 25))  # Lower TTH = better
    health_score = (conversion * 10 + offer_accept * 0.3 + speed_score * 0.3) / 3
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(conversion, 1),
            title={'text': "Overall Conversion %", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': "#2ecc71"},
                'steps': [
                    {'range': [0, 1.5], 'color': '#fadbd8'},
                    {'range': [1.5, 3], 'color': '#fef9e7'},
                    {'range': [3, 5], 'color': '#d5f5e3'}
                ],
                'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.8, 'value': 2.5}
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(offer_accept, 0),
            title={'text': "Offer Accept Rate %", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3498db"},
                'steps': [
                    {'range': [0, 60], 'color': '#fadbd8'},
                    {'range': [60, 80], 'color': '#fef9e7'},
                    {'range': [80, 100], 'color': '#d5f5e3'}
                ],
                'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.8, 'value': 75}
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    with col3:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(avg_tth, 0),
            delta={'reference': 35, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            title={'text': "Avg Time to Hire (days)", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 60]},
                'bar': {'color': "#9b59b6"},
                'steps': [
                    {'range': [0, 25], 'color': '#d5f5e3'},
                    {'range': [25, 40], 'color': '#fef9e7'},
                    {'range': [40, 60], 'color': '#fadbd8'}
                ],
                'threshold': {'line': {'color': "red", 'width': 3}, 'thickness': 0.8, 'value': 45}
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # --- Waterfall Chart: Where Candidates Drop Off ---
    st.markdown("#### 📉 Pipeline Leakage — Where We Lose Candidates")
    
    applied = len(fdf)
    screened = fdf['Screened'].sum()
    interviewed = fdf['Interviewed'].sum()
    offered = fdf['Offered'].sum()
    hired = fdf['Hired'].sum()
    
    fig = go.Figure(go.Waterfall(
        name="Pipeline",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Applied", "Lost at Screen", "Lost at Interview", "Lost at Offer", "Hired"],
        y=[applied, -(applied - screened), -(screened - interviewed), -(interviewed - hired), hired],
        text=[f"{applied:,}", f"-{applied-screened:,}", f"-{screened-interviewed:,}", f"-{interviewed-hired:,}", f"{hired}"],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        increasing={"marker": {"color": "#2ecc71"}},
        totals={"marker": {"color": "#3498db"}}
    ))
    fig.update_layout(title="<b>Candidate Pipeline Waterfall</b>", height=400,
                     margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # --- Source Efficiency Bubble Chart ---
    st.markdown("#### 💰 Source Investment Matrix — Volume vs Quality vs Speed")
    
    source_bubble = fdf.groupby('Source').agg(
        Applications=('CandidateID', 'count'),
        Hires=('Hired', 'sum'),
        Avg_TTH=('TimeToHire', lambda x: x[fdf.loc[x.index, 'Hired']==1].mean())
    ).reset_index()
    source_bubble['Hire_Rate'] = (source_bubble['Hires'] / source_bubble['Applications'] * 100).round(2)
    source_bubble['Avg_TTH'] = source_bubble['Avg_TTH'].fillna(40)
    
    fig = px.scatter(
        source_bubble, x='Applications', y='Hire_Rate',
        size='Hires', color='Source',
        hover_data=['Avg_TTH'],
        title='<b>Source Matrix: Volume (x) vs Quality (y) vs Hires (size)</b>',
        labels={'Applications': 'Total Applications', 'Hire_Rate': 'Hire Rate (%)'}
    )
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
    fig.update_traces(marker=dict(sizemin=10))
    st.plotly_chart(fig, width="stretch")
    
    st.info("""
    **🎯 How to read this chart:**
    - **Top-right** = High volume + High quality (ideal)
    - **Top-left** = Low volume but high quality (increase investment here)
    - **Bottom-right** = High volume but low quality (reduce spend or improve screening)
    - **Bubble size** = Total hires from that source
    """)
    
    st.markdown("---")
    
    # --- Department Heatmap: Multi-metric ---
    st.markdown("#### 🏢 Department Performance Heatmap")
    
    dept_heat = fdf.groupby('Department').agg(
        Screen_Rate=('Screened', 'mean'),
        Interview_Rate=('Interviewed', 'mean'),
        Offer_Rate=('Offered', 'mean'),
        Hire_Rate=('Hired', 'mean'),
    ).round(3) * 100
    
    fig = px.imshow(
        dept_heat.values,
        x=['Screen Rate %', 'Interview Rate %', 'Offer Rate %', 'Hire Rate %'],
        y=dept_heat.index.tolist(),
        text_auto='.1f',
        color_continuous_scale='RdYlGn',
        title='<b>Conversion Rates by Department (%) — Heatmap</b>',
        aspect='auto'
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # --- Experience Level Sunburst ---
    st.markdown("#### 🎓 Hiring Distribution — Department × Experience Level")
    
    hired_data = fdf[fdf['Hired'] == 1]
    if len(hired_data) > 0:
        fig = px.sunburst(
            hired_data, path=['Department', 'ExperienceLevel'],
            title='<b>Who Did We Hire? (Department → Experience Level)</b>',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=500, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # --- Key Takeaways Box ---
    st.markdown("#### 📋 Key Takeaways for Leadership")
    
    best_source = fdf.groupby('Source')['Hired'].mean().idxmax()
    worst_source = fdf.groupby('Source')['Hired'].mean().idxmin()
    fastest_dept = fdf[fdf['Hired']==1].groupby('Department')['TimeToHire'].mean().idxmin()
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"""
        **✅ What's Working:**
        - Best source: **{best_source}** (highest hire rate)
        - Fastest department: **{fastest_dept}**
        - Offer accept rate at **{offer_accept:.0f}%** (within benchmark)
        - Pipeline generating **{applied:,}** candidates
        """)
    with col2:
        st.error(f"""
        **🚨 Areas to Improve:**
        - **{applied - screened:,}** candidates lost at screening (70% drop)
        - Lowest source: **{worst_source}** (lowest ROI)
        - Time to hire at **{avg_tth:.0f} days** (target: <30)
        - **{int(fdf['Offered'].sum() - hires)}** offer declines (salary gap)
        """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#7f8c8d;'>
    <p>Built by <b>Priyanka S Biradar</b> | HR Analyst @ Goldman Sachs → Data Analyst</p>
    <p style='font-size:0.8rem;'>Powered by Python • SQL • Plotly • Streamlit</p>
</div>
""", unsafe_allow_html=True)
