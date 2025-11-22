# [file name]: tools.py
from ddgs import DDGS
import time
import re


def search_web(query, max_results=3):
    """
    Clean, fast web search using DDGS
    """
    # VALIDATE: Ensure query is not AI reasoning text
    if len(query) > 100 or any(phrase in query.lower() for phrase in [
        'here are', 'effective web search', 'search query', 'user input interpretation'
    ]):
        # If it's AI reasoning, extract the actual search intent
        clean_query = _extract_clean_query(query)
        if not clean_query:
            return "Search query too complex - using internal knowledge"
        query = clean_query

    print(f"🔍 Searching for: '{query}'")

    try:
        # USING DDGS (new package name)
        with DDGS() as ddgs:
            results = []
            # DDGS returns a generator, so we need to collect results
            for result in ddgs.text(query, max_results=max_results):
                results.append(result)
                if len(results) >= max_results:
                    break

        if not results:
            return "No quick results found"

        # Format results
        formatted = f"🔍 Search Results for '{query}':\n\n"
        for i, res in enumerate(results):
            title = res.get('title', 'No title').strip()
            url = res.get('href', 'No URL').strip()
            snippet = res.get('body', 'No summary')[:200].strip()

            formatted += f"{i + 1}. {title}\n"
            formatted += f"   📝 {snippet}\n"
            formatted += f"   🔗 {url}\n\n"

        return formatted

    except Exception as e:
        return f"Search unavailable: {str(e)}"


def _extract_clean_query(ai_reasoning_text):
    """
    Extract clean search query from AI reasoning text
    """
    # Look for quoted search queries in the AI text
    quoted_queries = re.findall(r'`([^`]+)`', ai_reasoning_text)
    if quoted_queries:
        return quoted_queries[0]

    # Look for search queries after "search query:" or similar
    patterns = [
        r'search query[:\s]+([^\n\.]+)',
        r'query[:\s]+([^\n\.]+)',
        r'search for[:\s]+([^\n\.]+)'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, ai_reasoning_text, re.IGNORECASE)
        if matches:
            return matches[0].strip()

    return None


def smart_company_search(user_input):
    """
    Direct company search without AI query generation
    """
    # Extract company name directly
    companies = {
        'tesla', 'apple', 'microsoft', 'google', 'amazon', 'netflix',
        'meta', 'starbucks', 'salesforce', 'nvidia', 'intel', 'dell',
        'hp', 'ibm', 'oracle', 'adobe', 'spotify', 'uber', 'airbnb',
        'samsung', 'sony', 'cisco', 'qualcomm', 'amd', 'paypal', 'visa'
    }

    user_lower = user_input.lower()

    # Find mentioned company
    for company in companies:
        if company in user_lower:
            return search_web(f"{company} company news financial 2024")

    # Generic company research - take first 3-4 words max
    words = user_input.split()[:4]
    base_query = " ".join(words)
    return search_web(f"{base_query} company business news")


def fast_company_search(company_name):
    """
    Ultra-fast company-specific search
    """
    try:
        with DDGS() as ddgs:
            results = []
            query = f"{company_name} company latest news financial 2024"

            for result in ddgs.text(query, max_results=2):
                results.append(result)
                if len(results) >= 2:
                    break

        if not results:
            return f"No recent data found for {company_name}"

        formatted = f"📊 Quick {company_name.title()} Update:\n\n"
        for i, res in enumerate(results):
            title = res.get('title', 'No title')
            snippet = res.get('body', '')[:150]
            formatted += f"• {title}\n"
            if snippet:
                formatted += f"  {snippet}...\n"

        return formatted

    except Exception as e:
        return f"Quick search failed for {company_name}"