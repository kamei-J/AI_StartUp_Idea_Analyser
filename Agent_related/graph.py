from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_tavily import TavilySearch
from Agent_related.prompt import Ideas, MarketResearchAnalyser, CompetitorAnalysis, BusinessModelAnalysis, fact_check_prompt, final_report
from Agent_related.state import AgentState
from Agent_related.tools import wikipediaQueryRunner_with_error_handling

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

tavily_tool = TavilySearch(max_results=7)

def planner_agent(state: dict) -> dict:
    """Generate one or more startup ideas from a short description.

    The user provides a high–level prompt (e.g. "green energy for pets").
    We wrap it with the `Ideas` prompt template and invoke the LLM.
    The raw text is returned so that downstream nodes can either display
    it or parse individual plans later.
    """
    user_input = state.get("user_input", "")
    prompt = Ideas(user_input)
    response = llm.invoke(prompt)
    if response is None:
        raise ValueError("planner_agent: LLM returned no response")
    # store the generated text under a standardized key
    return {"startup_idea": response.content}

def researcher_agent(state: dict) -> dict:
    """Research the startup idea using Wikipedia + Tavily for real market insights."""

    startup_idea = state.get("startup_idea", "")
    if not startup_idea:
        raise ValueError("researcher_agent: No startup_idea provided in state")

    # ---------------------------
    # Wikipedia Research
    # ---------------------------
    try:
        wiki_tool = wikipediaQueryRunner_with_error_handling()
        wiki_result = wiki_tool.run(startup_idea)

        wiki_context = (
            wiki_result if wiki_result
            else "No relevant Wikipedia information found."
        )

    except Exception as e:
        wiki_context = f"Error retrieving Wikipedia data: {str(e)}"

    # ---------------------------
    # Tavily Market Research
    # ---------------------------
    try:
        market_queries = [
            f"{startup_idea} global market size 2024 2025 report",
            f"{startup_idea} industry CAGR growth rate forecast",
            f"{startup_idea} market demand statistics target customers",
            f"top companies and startups in {startup_idea} industry",
            f"{startup_idea} market trends technology adoption",
            f"{startup_idea} investment funding venture capital startups",
            f"{startup_idea} industry challenges regulations barriers"
        ]

        tavily_results = []

        for query in market_queries:
            result = tavily_tool.invoke({"query": query})
            if result:
                tavily_results.append(str(result))

        tavily_context = (
            "\n\n".join(tavily_results)
            if tavily_results
            else "No market statistics found via Tavily search."
        )

    except Exception as e:
        tavily_context = f"Error retrieving Tavily search data: {str(e)}"

    # ---------------------------
    # Build Enhanced Prompt
    # ---------------------------
    base_prompt = MarketResearchAnalyser(startup_idea)

    enhanced_prompt = f"""
{base_prompt}

Use the following external research data.

Wikipedia Background:
{wiki_context}

Web Market Research (Tavily Search):
{tavily_context}

Focus especially on:
- Market Size
- Growth Rate (CAGR)
- Industry Trends
- Customer Demand
- Major Companies
"""

    response = llm.invoke(enhanced_prompt)

    if response is None:
        raise ValueError("researcher_agent: LLM returned no response")

    return {"market_analysis": response.content}

def analysis_agent(state: dict) -> dict:
    """Conduct competitor analysis by searching the web for real competitors.

    This agent uses web search to find actual competitors in the market,
    then enhances the competitor analysis prompt with search results.
    """
    startup_idea = state.get("startup_idea", "")
    if not startup_idea:
        raise ValueError("analysis_agent: No startup_idea provided in state")

    # Search the web for competitors
    try:
        search_query = f"competitors in {startup_idea} market"
        search_results = tavily_tool.invoke({"query": search_query})
        search_context = search_results if search_results else "No competitor information found from search."
    except Exception as e:
        search_context = f"Error retrieving search data: {str(e)}"

    # Enhance the competitor analysis prompt with search context
    base_prompt = CompetitorAnalysis(startup_idea)
    enhanced_prompt = f"{base_prompt}\n\nAdditional context from web search:\n{search_context}"

    response = llm.invoke(enhanced_prompt)
    if response is None:
        raise ValueError("analysis_agent: LLM returned no response")
    return {"competitor_analysis": response.content}

def strategies_agent(state: dict) -> dict:
    """Strategize business models based on market and competitor analyses.

    This agent incorporates insights from market research and competitor analysis
    to recommend viable business models and strategies.
    """
    startup_idea = state.get("startup_idea", "")
    market_analysis = state.get("market_analysis", "")
    competitor_analysis = state.get("competitor_analysis", "")

    # Build enhanced prompt with previous analyses
    base_prompt = BusinessModelAnalysis(startup_idea)
    enhanced_prompt = f"{base_prompt}\n\nMarket Analysis:\n{market_analysis}\n\nCompetitor Analysis:\n{competitor_analysis}"

    response = llm.invoke(enhanced_prompt)
    if response is None:
        raise ValueError("strategies_agent: LLM returned no response")
    return {"business_model_analysis": response.content}

def final_report_agent(state: dict) -> dict:
    """Compile a complete startup feasibility report summarizing all analyses.

    This agent synthesizes the startup idea, market research, competitor analysis,
    and business model strategies into a comprehensive final report.
    """
    startup_idea = state.get("startup_idea", "")
    market_analysis = state.get("market_analysis", "")
    competitor_analysis = state.get("competitor_analysis", "")
    business_model_analysis = state.get("business_model_analysis", "")

    # Build comprehensive prompt with all previous analyses
    base_prompt = final_report(startup_idea)
    enhanced_prompt = f"{base_prompt}\n\nDetailed Analyses:\n\nMarket Analysis:\n{market_analysis}\n\nCompetitor Analysis:\n{competitor_analysis}\n\nBusiness Model Analysis:\n{business_model_analysis}"

    response = llm.invoke(enhanced_prompt)
    if response is None:
        raise ValueError("final_report_agent: LLM returned no response")
    return {"final_report": response.content}

def fact_check_agent(state: dict) -> dict:
    """Validate the final report by cross-checking claims with web search."""

    final_report = state.get("final_report", "")

    if not final_report:
        raise ValueError("fact_check_agent: No final_report found")

    try:
        # Search for evidence related to the report
        search_query = "startup market statistics industry trends competitors analysis"
        search_results = tavily_tool.invoke({"query": search_query})

        search_context = search_results if search_results else "No search evidence found."

    except Exception as e:
        search_context = f"Search error: {str(e)}"

    prompt = fact_check_prompt(final_report)

    enhanced_prompt = f"""
{prompt}

External Evidence From Web Search:
{search_context}

Use the evidence above to validate the claims.
"""

    response = llm.invoke(enhanced_prompt)

    if response is None:
        raise ValueError("fact_check_agent: LLM returned no response")

    return {"fact_check_report": response.content}


graph = StateGraph(AgentState)

graph.add_node("planner", planner_agent)
graph.add_node("researcher", researcher_agent)
graph.add_node("analysis", analysis_agent)
graph.add_node("strategies", strategies_agent)
graph.add_node("final", final_report_agent)
graph.add_node("fact_check", fact_check_agent)

graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "analysis")
graph.add_edge("analysis", "strategies")
graph.add_edge("strategies", "final")

graph.add_edge("final", "fact_check")
graph.add_edge("fact_check", END)

graph.set_entry_point("planner")

agent = graph.compile()

