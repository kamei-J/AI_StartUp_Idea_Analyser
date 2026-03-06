def Ideas(state: str) -> str:
    return f"""
You are an expert startup ideation consultant.

Context:
{state}

Generate **3-5 innovative startup ideas**.

For EACH idea provide:

1. Idea Name
2. Description (2-3 sentences)
3. Target Market
4. Unique Value Proposition
5. Potential Challenges

Return the output in the following structured Markdown format:

### Idea 1
Name:
Description:
Target Market:
Value Proposition:
Challenges:

### Idea 2
Name:
Description:
Target Market:
Value Proposition:
Challenges:

Focus on:
- AI
- SaaS
- Automation
- Emerging technologies

Ideas must solve **real-world problems and be scalable**.
"""

def MarketResearchAnalyser(state: str) -> str:
    return f"""
You are a professional startup market research analyst.

Startup Idea:
{state}

Provide a **detailed market research report**.

Include:

1. Market Overview
2. Market Size (TAM, SAM, SOM if possible)
3. Growth Rate (CAGR estimates)
4. Key Industry Trends
5. Target Customer Segments
6. Customer Pain Points
7. Barriers to Entry
8. Opportunities and Threats

Output Format:

## Market Overview

## Market Size

## Growth Trends

## Customer Segments

## Key Pain Points

## Barriers to Entry

## Opportunities

## Threats

Use realistic estimates and data-driven reasoning.
"""

def CompetitorAnalysis(state: str) -> str:
    return f"""
You are a competitive intelligence analyst.

Startup Idea:
{state}

Conduct a competitor analysis.

Identify **3-5 competitors** and analyze them.

Output format:

## Competitor 1
Name:
Product:
Market Position:
Strengths:
Weaknesses:
Pricing Model:

## Competitor 2
Name:
Product:
Market Position:
Strengths:
Weaknesses:
Pricing Model:

Then provide:

## Competitive Gap Analysis
What competitors are missing.

## Differentiation Opportunities
How this startup can stand out.
"""

def BusinessModelAnalysis(state: str) -> str:
    return f"""
You are a startup business strategist.

Startup Idea:
{state}

Evaluate **3 potential business models**.

For each model analyze:

- Revenue Streams
- Cost Structure
- Key Resources
- Distribution Channels
- Scalability
- Risks

Output format:

## Business Model 1: Subscription SaaS
Revenue Streams:
Cost Structure:
Advantages:
Disadvantages:

## Business Model 2: Freemium
Revenue Streams:
Cost Structure:
Advantages:
Disadvantages:

## Business Model 3: Marketplace
Revenue Streams:
Cost Structure:
Advantages:
Disadvantages:

Finally provide:

## Recommended Model
Explain which model is best and why.
"""

def final_report(state: str) -> str:
    return f"""
You are a startup feasibility consultant.

Startup Idea:
{state}

Generate a **complete startup feasibility report**.

Structure the report as follows:

# Startup Feasibility Report

## 1. Startup Idea Overview
Description and unique value proposition.

## 2. Market Analysis
Key market size, growth, and demand insights.

## 3. Competitor Landscape
Major competitors and differentiation.

## 4. Business Model Recommendation
Recommended revenue strategy.

## 5. Risks and Challenges
Potential obstacles.

## 6. Go-To-Market Strategy
How the startup can acquire its first customers.

## 7. Final Feasibility Score
Score the idea from **1–10** and explain why.

Make the report **clear, structured, and actionable**.
"""

def fact_check_prompt(report: str) -> str:
    return f"""
You are a fact-checking analyst.

Your task is to verify the claims made in the following startup feasibility report.

Report:
{report}

Instructions:
1. Identify key factual claims (market size, CAGR, competitors, trends).
2. Cross-check them with the provided web search evidence.
3. Label each claim as:

- VERIFIED
- PARTIALLY VERIFIED
- UNVERIFIED

Output format:

## Claim 1
Statement:
Verification Status:
Explanation:

## Claim 2
Statement:
Verification Status:
Explanation:

Finally provide:

## Overall Credibility Score
Score the report from 1–10 based on factual reliability.
"""
