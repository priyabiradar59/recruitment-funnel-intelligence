# ============================================================================
# src/generate_data.py — Generate Realistic Recruitment Funnel Dataset
# ============================================================================
# PURPOSE: Create a synthetic but realistic hiring pipeline dataset.
#
# WHY SYNTHETIC:
#   - No public recruitment funnel datasets exist (companies keep this private)
#   - Generating our own shows we understand the DOMAIN deeply
#   - The patterns mirror real-world recruiting (based on industry benchmarks)
#
# DATASET STRUCTURE:
#   Each row = 1 candidate who entered the hiring pipeline
#   Columns track their journey: Applied → Screened → Interviewed → Offered → Hired
#
# INDUSTRY BENCHMARKS USED:
#   - Application to Screen: 20-30%
#   - Screen to Interview: 40-60%
#   - Interview to Offer: 15-25%
#   - Offer to Accept: 70-90%
#   - Overall: 2-5% of applicants get hired
#   - Average Time to Fill: 30-45 days
#   - Source effectiveness: Referrals > LinkedIn > Job Boards > Career Sites
# ============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)


def generate_recruitment_data(n_candidates=5000):
    """
    Generate a realistic recruitment funnel dataset.
    
    Simulates a tech company hiring across multiple departments, roles, 
    and sourcing channels over 12 months.
    """
    print("🏗️  Generating recruitment funnel dataset...")
    
    # --- Configuration (mirrors real company data) ---
    departments = {
        'Engineering': {'weight': 0.40, 'roles': ['Software Engineer', 'Data Engineer', 'DevOps Engineer', 'QA Engineer', 'Frontend Developer']},
        'Sales': {'weight': 0.25, 'roles': ['Account Executive', 'Sales Development Rep', 'Sales Manager', 'Solutions Architect']},
        'Marketing': {'weight': 0.15, 'roles': ['Marketing Manager', 'Content Specialist', 'Growth Analyst', 'SEO Specialist']},
        'HR': {'weight': 0.10, 'roles': ['HR Business Partner', 'Recruiter', 'Talent Acquisition Lead', 'People Analyst']},
        'Finance': {'weight': 0.10, 'roles': ['Financial Analyst', 'Accountant', 'FP&A Manager', 'Controller']}
    }
    
    sources = {
        'LinkedIn': {'weight': 0.30, 'screen_rate': 0.28, 'quality': 0.7},
        'Job Board': {'weight': 0.25, 'screen_rate': 0.18, 'quality': 0.5},
        'Employee Referral': {'weight': 0.15, 'screen_rate': 0.45, 'quality': 0.9},
        'Career Site': {'weight': 0.15, 'screen_rate': 0.22, 'quality': 0.6},
        'Recruitment Agency': {'weight': 0.10, 'screen_rate': 0.35, 'quality': 0.75},
        'Campus Hiring': {'weight': 0.05, 'screen_rate': 0.30, 'quality': 0.65}
    }
    
    locations = ['Bangalore', 'Mumbai', 'Hyderabad', 'Delhi NCR', 'Pune', 'Chennai']
    experience_levels = ['Fresher (0-1)', 'Junior (1-3)', 'Mid (3-5)', 'Senior (5-8)', 'Lead (8+)']
    
    recruiters = ['Priya S', 'Amit K', 'Neha R', 'Rahul M', 'Deepa J', 'Vijay P']
    
    # --- Generate candidates ---
    candidates = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(n_candidates):
        # Random application date within the year
        days_offset = random.randint(0, 364)
        apply_date = start_date + timedelta(days=days_offset)
        
        # Select department (weighted)
        dept = random.choices(
            list(departments.keys()),
            weights=[d['weight'] for d in departments.values()]
        )[0]
        
        # Select role within department
        role = random.choice(departments[dept]['roles'])
        
        # Select source (weighted)
        source = random.choices(
            list(sources.keys()),
            weights=[s['weight'] for s in sources.values()]
        )[0]
        
        source_config = sources[source]
        
        # Experience level (influences conversion rates)
        exp_level = random.choices(
            experience_levels,
            weights=[0.15, 0.30, 0.25, 0.20, 0.10]
        )[0]
        
        location = random.choice(locations)
        recruiter = random.choice(recruiters)
        
        # --- FUNNEL SIMULATION ---
        # Each stage has a pass/fail probability based on source quality
        
        # Stage 1: Application → Screening
        screen_rate = source_config['screen_rate']
        # Adjust by experience (seniors have higher screen rates)
        if 'Senior' in exp_level or 'Lead' in exp_level:
            screen_rate *= 1.3
        elif 'Fresher' in exp_level:
            screen_rate *= 0.7
        
        screened = random.random() < min(screen_rate, 0.95)
        screen_date = apply_date + timedelta(days=random.randint(1, 5)) if screened else None
        
        # Stage 2: Screening → Interview
        interviewed = False
        interview_date = None
        if screened:
            interview_rate = 0.50 * source_config['quality']
            if dept == 'Engineering':
                interview_rate *= 0.85  # Harder to pass tech screens
            interviewed = random.random() < interview_rate
            interview_date = screen_date + timedelta(days=random.randint(3, 10)) if interviewed else None
        
        # Stage 3: Interview → Offer
        offered = False
        offer_date = None
        if interviewed:
            offer_rate = 0.22
            if source == 'Employee Referral':
                offer_rate *= 1.5  # Referrals convert better
            elif source == 'Job Board':
                offer_rate *= 0.8
            # Experience matters
            if 'Mid' in exp_level or 'Senior' in exp_level:
                offer_rate *= 1.2
            offered = random.random() < min(offer_rate, 0.95)
            offer_date = interview_date + timedelta(days=random.randint(2, 7)) if offered else None
        
        # Stage 4: Offer → Acceptance
        accepted = False
        join_date = None
        if offered:
            accept_rate = 0.78
            if source == 'Employee Referral':
                accept_rate = 0.92
            elif dept == 'Engineering':
                accept_rate = 0.70  # Engineers get multiple offers
            accepted = random.random() < accept_rate
            join_date = offer_date + timedelta(days=random.randint(15, 45)) if accepted else None
        
        # Rejection reasons
        rejection_stage = None
        rejection_reason = None
        if not screened:
            rejection_stage = 'Screening'
            rejection_reason = random.choice(['Skills mismatch', 'Experience gap', 'Location mismatch', 'Salary expectations too high'])
        elif not interviewed:
            rejection_stage = 'Interview Scheduling'
            rejection_reason = random.choice(['No show', 'Withdrew application', 'Found another job', 'Failed phone screen'])
        elif not offered:
            rejection_stage = 'Interview'
            rejection_reason = random.choice(['Technical assessment failed', 'Culture fit concerns', 'Communication issues', 'Better candidate found', 'Panel feedback negative'])
        elif not accepted:
            rejection_stage = 'Offer'
            rejection_reason = random.choice(['Accepted competing offer', 'Salary not competitive', 'Counter-offered by current employer', 'Personal reasons', 'Relocation issues'])
        
        # Calculate time metrics
        time_to_screen = (screen_date - apply_date).days if screen_date else None
        time_to_interview = (interview_date - apply_date).days if interview_date else None
        time_to_offer = (offer_date - apply_date).days if offer_date else None
        time_to_hire = (join_date - apply_date).days if join_date else None
        
        # Current stage
        if accepted:
            current_stage = 'Hired'
        elif offered:
            current_stage = 'Offer Declined'
        elif interviewed:
            current_stage = 'Rejected Post-Interview'
        elif screened:
            current_stage = 'Rejected Post-Screen'
        else:
            current_stage = 'Rejected at Screening'
        
        candidates.append({
            'CandidateID': f'CAND-{i+1:04d}',
            'ApplicationDate': apply_date.strftime('%Y-%m-%d'),
            'Department': dept,
            'JobRole': role,
            'ExperienceLevel': exp_level,
            'Source': source,
            'Location': location,
            'Recruiter': recruiter,
            'Month': apply_date.strftime('%Y-%m'),
            'Quarter': f'Q{(apply_date.month - 1) // 3 + 1}',
            
            # Funnel stages (1=passed, 0=failed/not reached)
            'Screened': int(screened),
            'Interviewed': int(interviewed),
            'Offered': int(offered),
            'Hired': int(accepted),
            
            # Dates
            'ScreenDate': screen_date.strftime('%Y-%m-%d') if screen_date else None,
            'InterviewDate': interview_date.strftime('%Y-%m-%d') if interview_date else None,
            'OfferDate': offer_date.strftime('%Y-%m-%d') if offer_date else None,
            'JoinDate': join_date.strftime('%Y-%m-%d') if join_date else None,
            
            # Time metrics (days)
            'TimeToScreen': time_to_screen,
            'TimeToInterview': time_to_interview,
            'TimeToOffer': time_to_offer,
            'TimeToHire': time_to_hire,
            
            # Outcome
            'CurrentStage': current_stage,
            'RejectionStage': rejection_stage,
            'RejectionReason': rejection_reason,
            
            # Salary data
            'ExpectedSalary_LPA': round(random.uniform(3, 35) * (1 + experience_levels.index(exp_level) * 0.5), 1),
            'OfferedSalary_LPA': round(random.uniform(3, 30) * (1 + experience_levels.index(exp_level) * 0.5), 1) if offered else None
        })
    
    df = pd.DataFrame(candidates)
    
    # --- Summary ---
    print(f"   ✅ Generated {len(df):,} candidate records")
    print(f"   📊 Funnel summary:")
    print(f"      Applied:     {len(df):,} (100%)")
    print(f"      Screened:    {df['Screened'].sum():,} ({df['Screened'].mean()*100:.1f}%)")
    print(f"      Interviewed: {df['Interviewed'].sum():,} ({df['Interviewed'].mean()*100:.1f}%)")
    print(f"      Offered:     {df['Offered'].sum():,} ({df['Offered'].mean()*100:.1f}%)")
    print(f"      Hired:       {df['Hired'].sum():,} ({df['Hired'].mean()*100:.1f}%)")
    print(f"      Overall conversion: {df['Hired'].mean()*100:.1f}%")
    
    return df


if __name__ == "__main__":
    df = generate_recruitment_data(5000)
    
    output_path = 'data/raw/recruitment_funnel_data.csv'
    df.to_csv(output_path, index=False)
    print(f"\n   💾 Saved to: {output_path}")
    print(f"      Shape: {df.shape[0]} rows × {df.shape[1]} columns")
