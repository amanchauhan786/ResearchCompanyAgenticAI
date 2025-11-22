# [file name]: agent.py
import google.generativeai as genai
from utils.tools import search_web
import re


class ResearchAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat = self.model.start_chat(history=[])
        self.current_persona = "Standard Professional"

    def update_persona(self, persona_prompt, persona_name):
        """Injects the selected persona into the system context."""
        self.current_persona = persona_name
        system_message = f"""
        SYSTEM UPDATE: Adopt the following persona guidelines strictly: {persona_prompt}

        IMPORTANT BEHAVIORS:
        1. Provide status updates during research ("I'm finding conflicting information about X")
        2. Ask clarifying questions when information is ambiguous
        3. Acknowledge when you need to search for information
        4. Structure account plans with clear sections
        5. Adapt your response style to the selected persona
        """
        try:
            self.chat.send_message(system_message)
        except:
            # If history is too long, restart chat
            self.chat = self.model.start_chat(history=[])
            self.chat.send_message(system_message)

    def _extract_account_plan(self, text):
        """Extract account plan sections from response."""
        plan_sections = {}
        current_section = None
        current_content = []

        lines = text.split('\n')
        for line in lines:
            if line.startswith('## '):
                if current_section:
                    plan_sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif line.startswith('### '):
                if current_section:
                    plan_sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[4:].strip()
                current_content = []
            elif current_section and line.strip():
                current_content.append(line)

        if current_section:
            plan_sections[current_section] = '\n'.join(current_content).strip()

        return plan_sections

    def get_response(self, user_input, current_plan_context=""):
        status_updates = []
        search_context = ""

        # 1. DECISION: Check if search is needed with reasoning
        decision_prompt = f"""
        User Input: '{user_input}'
        Current Persona: {self.current_persona}

        Analyze if this query requires external, current information (news, financial data, company updates, market trends) to provide an accurate response.

        Consider:
        - Does it require recent data (last 1-2 years)?
        - Is it about specific financial figures, news, or market data?
        - Would web search significantly improve answer quality?

        Answer ONLY 'YES' or 'NO' followed by a brief reason.
        Example: "YES - Need current financial data"
        """

        try:
            decision_response = self.model.generate_content(decision_prompt).text.strip()
            decision = "YES" if decision_response.startswith("YES") else "NO"
            status_updates.append(f"🔍 Analysis: {decision_response}")
        except Exception as e:
            decision = "NO"
            status_updates.append(f"⚠️ Decision analysis failed, defaulting to NO")

        # 2. ACTION: Search if needed
        if "YES" in decision:
            status_updates.append("🕵️ Researching live data...")

            # Generate search query
            query_prompt = f"""
            Convert this user input to an effective web search query for company research:
            User: '{user_input}'
            Persona: {self.current_persona}

            Focus on:
            - Company financials, news, leadership
            - Industry trends, competitors
            - Recent developments, market analysis
            """

            try:
                search_query = self.model.generate_content(query_prompt).text.strip()
                status_updates.append(f"📝 Search query: {search_query}")

                # Perform search
                raw_data = search_web(search_query)
                search_context = f"\n[LIVE SEARCH RESULTS]:\n{raw_data}\n"
                status_updates.append("✅ Search completed, analyzing results...")

            except Exception as e:
                search_context = f"\n[SEARCH ERROR]: {str(e)}\n"
                status_updates.append("❌ Search failed, proceeding without live data")

        # 3. Generate thoughtful response
        full_prompt = f"""
        PERSONA: {self.current_persona}
        CURRENT ACCOUNT PLAN CONTEXT:
        {current_plan_context}

        USER REQUEST: {user_input}

        {search_context}

        INSTRUCTIONS:
        1. First, acknowledge the request and mention if you're using search data
        2. Provide status updates on your findings ("I'm noticing conflicting information about...")
        3. If updating the account plan, structure it clearly with headers (## Section Name)
        4. Ask clarifying questions when needed
        5. Adapt to the persona style
        6. End with a natural conversational closing

        Important sections for account plans:
        ## Company Overview
        ## Key Financials  
        ## Market Position
        ## Growth Opportunities
        ## Strategic Recommendations
        """

        try:
            response = self.chat.send_message(full_prompt)
            response_text = response.text

            # Extract account plan updates
            plan_updates = self._extract_account_plan(response_text)

            return response_text, status_updates, search_context, plan_updates

        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."
            return error_msg, ["❌ Error generating response"], "", {}