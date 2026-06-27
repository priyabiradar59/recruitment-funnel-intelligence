-- ============================================================================
-- recruitment_funnel_queries.sql — Advanced Hiring Analytics SQL
-- ============================================================================
-- Demonstrates: Funnel analysis, conversion rates, window functions,
-- recruiter productivity, source ROI, time-to-hire optimization
-- ============================================================================


-- ============================================================================
-- 1. FULL FUNNEL CONVERSION ANALYSIS
-- ============================================================================
SELECT 
    'Applied' AS stage, COUNT(*) AS candidates, 
    100.0 AS cumulative_pct,
    NULL AS stage_conversion_pct
FROM candidates
UNION ALL
SELECT 'Screened', SUM(Screened),
    ROUND(SUM(Screened) * 100.0 / COUNT(*), 1),
    ROUND(SUM(Screened) * 100.0 / COUNT(*), 1)
FROM candidates
UNION ALL
SELECT 'Interviewed', SUM(Interviewed),
    ROUND(SUM(Interviewed) * 100.0 / COUNT(*), 1),
    ROUND(SUM(Interviewed) * 100.0 / SUM(Screened), 1)
FROM candidates
UNION ALL
SELECT 'Offered', SUM(Offered),
    ROUND(SUM(Offered) * 100.0 / COUNT(*), 1),
    ROUND(SUM(Offered) * 100.0 / SUM(Interviewed), 1)
FROM candidates
UNION ALL
SELECT 'Hired', SUM(Hired),
    ROUND(SUM(Hired) * 100.0 / COUNT(*), 1),
    ROUND(SUM(Hired) * 100.0 / SUM(Offered), 1)
FROM candidates;


-- ============================================================================
-- 2. SOURCE EFFECTIVENESS — ROI by Channel (Window Function + CTE)
-- ============================================================================
WITH source_metrics AS (
    SELECT 
        Source,
        COUNT(*) AS total_applied,
        SUM(Screened) AS screened,
        SUM(Interviewed) AS interviewed,
        SUM(Offered) AS offered,
        SUM(Hired) AS hired,
        ROUND(SUM(Hired) * 100.0 / COUNT(*), 2) AS hire_rate,
        ROUND(AVG(CASE WHEN Hired = 1 THEN TimeToHire END), 1) AS avg_time_to_hire
    FROM candidates
    GROUP BY Source
)
SELECT 
    Source,
    total_applied,
    hired,
    hire_rate,
    avg_time_to_hire,
    RANK() OVER (ORDER BY hire_rate DESC) AS efficiency_rank,
    ROUND(total_applied * 1.0 / NULLIF(hired, 0), 0) AS applications_per_hire
FROM source_metrics
ORDER BY hire_rate DESC;


-- ============================================================================
-- 3. RECRUITER PRODUCTIVITY SCORECARD (Multiple Metrics)
-- ============================================================================
SELECT 
    Recruiter,
    COUNT(*) AS candidates_managed,
    SUM(Hired) AS hires_made,
    ROUND(SUM(Hired) * 100.0 / COUNT(*), 2) AS conversion_rate,
    ROUND(AVG(CASE WHEN Hired = 1 THEN TimeToHire END), 1) AS avg_time_to_hire,
    ROUND(AVG(CASE WHEN Screened = 1 THEN TimeToScreen END), 1) AS avg_time_to_screen,
    SUM(CASE WHEN Offered = 1 AND Hired = 0 THEN 1 ELSE 0 END) AS offers_declined,
    ROUND(SUM(Hired) * 100.0 / NULLIF(SUM(Offered), 0), 1) AS offer_accept_rate
FROM candidates
GROUP BY Recruiter
ORDER BY hires_made DESC;


-- ============================================================================
-- 4. MONTHLY HIRING TRENDS (Running Total + MoM Change)
-- ============================================================================
WITH monthly AS (
    SELECT 
        Month,
        COUNT(*) AS applications,
        SUM(Hired) AS hires,
        ROUND(SUM(Hired) * 100.0 / COUNT(*), 2) AS hire_rate,
        ROUND(AVG(CASE WHEN Hired = 1 THEN TimeToHire END), 1) AS avg_time_to_hire
    FROM candidates
    GROUP BY Month
)
SELECT 
    Month,
    applications,
    hires,
    hire_rate,
    avg_time_to_hire,
    SUM(hires) OVER (ORDER BY Month) AS cumulative_hires,
    hires - LAG(hires) OVER (ORDER BY Month) AS mom_change,
    ROUND((hires - LAG(hires) OVER (ORDER BY Month)) * 100.0 
          / NULLIF(LAG(hires) OVER (ORDER BY Month), 0), 1) AS mom_pct_change
FROM monthly
ORDER BY Month;


-- ============================================================================
-- 5. DEPARTMENT FUNNEL BREAKDOWN (Pivot-style)
-- ============================================================================
SELECT 
    Department,
    COUNT(*) AS applied,
    SUM(Screened) AS screened,
    SUM(Interviewed) AS interviewed,
    SUM(Offered) AS offered,
    SUM(Hired) AS hired,
    ROUND(SUM(Screened) * 100.0 / COUNT(*), 1) AS screen_rate,
    ROUND(SUM(Interviewed) * 100.0 / NULLIF(SUM(Screened), 0), 1) AS interview_rate,
    ROUND(SUM(Offered) * 100.0 / NULLIF(SUM(Interviewed), 0), 1) AS offer_rate,
    ROUND(SUM(Hired) * 100.0 / NULLIF(SUM(Offered), 0), 1) AS accept_rate,
    ROUND(SUM(Hired) * 100.0 / COUNT(*), 1) AS overall_conversion
FROM candidates
GROUP BY Department
ORDER BY overall_conversion DESC;


-- ============================================================================
-- 6. REJECTION ANALYSIS — Where and Why Candidates Drop Off
-- ============================================================================
SELECT 
    RejectionStage,
    RejectionReason,
    COUNT(*) AS candidate_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY RejectionStage), 1) AS pct_within_stage,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM candidates WHERE Hired = 0), 1) AS pct_of_all_rejections
FROM candidates
WHERE Hired = 0 AND RejectionReason IS NOT NULL
GROUP BY RejectionStage, RejectionReason
ORDER BY RejectionStage, candidate_count DESC;


-- ============================================================================
-- 7. TIME-TO-HIRE ANALYSIS BY QUARTILE (NTILE)
-- ============================================================================
WITH hire_times AS (
    SELECT 
        *,
        NTILE(4) OVER (ORDER BY TimeToHire) AS time_quartile
    FROM candidates
    WHERE Hired = 1
)
SELECT 
    time_quartile,
    MIN(TimeToHire) AS min_days,
    MAX(TimeToHire) AS max_days,
    ROUND(AVG(TimeToHire), 1) AS avg_days,
    COUNT(*) AS hires_in_quartile,
    -- Which sources are fastest?
    GROUP_CONCAT(DISTINCT Source) AS common_sources
FROM hire_times
GROUP BY time_quartile
ORDER BY time_quartile;


-- ============================================================================
-- 8. OFFER DECLINE ANALYSIS — Why Candidates Reject Offers
-- ============================================================================
SELECT 
    Department,
    Source,
    COUNT(*) AS offers_declined,
    ROUND(AVG(ExpectedSalary_LPA), 1) AS avg_expected_salary,
    ROUND(AVG(OfferedSalary_LPA), 1) AS avg_offered_salary,
    ROUND(AVG(ExpectedSalary_LPA) - AVG(OfferedSalary_LPA), 1) AS salary_gap,
    GROUP_CONCAT(DISTINCT RejectionReason) AS decline_reasons
FROM candidates
WHERE Offered = 1 AND Hired = 0
GROUP BY Department, Source
HAVING COUNT(*) >= 2
ORDER BY offers_declined DESC;
