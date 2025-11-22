# AI Research Agent - Company Account Plan Generator

## Eightfold.ai AI Agent Building Assignment Submission

### Live Application
**Deployed Application**: https://agenticairesearch.streamlit.app/

### Problem Statement: Company Research Assistant (Account Plan Generator)

This project implements an interactive AI agent that helps users research companies through natural conversation and generate comprehensive account plans, fulfilling all specified requirements.

## Core Requirements Implementation

### Information Gathering and Synthesis
- **Multi-Source Integration**: Combines real-time web search via DuckDuckGo API with Google Gemini AI's knowledge base
- **Intelligent Synthesis**: Analyzes and integrates findings from multiple sources into coherent insights
- **Source Attribution**: Formats search results with titles, URLs, and summaries for transparency

### Research Process Updates
- **Status Reporting**: Provides real-time updates like "Researching live data..." and "Analyzing search results..."
- **Conflict Detection**: Identifies conflicting information between sources and prompts for clarification
- **Progress Transparency**: Maintains users informed about current processing stage and next steps

### Interactive Account Plan Management
- **Dynamic Section Editing**: Real-time modification of account plan sections through sidebar editors
- **Structured Output**: Generates organized plans with standardized sections (Company Overview, Key Financials, Market Position, etc.)
- **Export Capability**: Download functionality for completed plans in markdown format

### Multi-Modal Interaction
- **Text Interface**: Traditional chat-based interaction with streaming responses
- **Voice Integration**: Speech-to-text input and text-to-speech output with automatic playback
- **Seamless Switching**: Users can alternate between interaction modes within the same session

## System Architecture

### Component Architecture
```
User Interface Layer (Streamlit)
    |
Application Layer (main.py)
    |
Business Logic Layer (agent.py)
    |       |
External Services    Data Processing
(tools.py, audio.py)   Layer
```

### Core Components Description

**Research Agent (agent.py)**
- Central intelligence handling conversation flow and decision-making
- Persona management system for adaptive response styles
- Search necessity evaluation and query optimization
- Response generation with context integration

**Web Search Module (tools.py)**
- DuckDuckGo API integration for real-time data retrieval
- Query optimization and result filtering
- Search result formatting and relevance scoring
- Error handling and fallback mechanisms

**Audio Processing System (audio.py)**
- Voice input processing via streamlit-mic-recorder
- Text-to-speech output using pyttsx3
- Audio file management and playback control
- Thread-safe audio operations

**User Interface (main.py)**
- Streamlit-based web application
- Real-time chat interface with message history
- Interactive sidebar for configuration and plan editing
- Responsive design for various device sizes

### Data Flow
1. User input received via text or voice
2. Input processing and intent analysis
3. Search necessity evaluation
4. External data retrieval if required
5. Response generation with persona adaptation
6. Account plan section detection and updating
7. Output delivery via text and audio

## Design Decisions and Rationale

### Agentic Behavior Implementation
**Decision**: Proactive status updates and clarification requests
**Rationale**: Creates transparent interaction flow and demonstrates true agentic behavior beyond simple question-answering. Users remain informed about processing stages and can provide additional context when needed.

**Decision**: Multi-persona system with distinct interaction styles
**Rationale**: Addresses varied user preferences and scenarios outlined in evaluation criteria. Each persona demonstrates different aspects of intelligent adaptability.

### Conversation Quality Focus
**Decision**: Natural language processing with context maintenance
**Rationale**: Prioritizes fluid, human-like interactions over transactional exchanges. Maintains conversation history for coherent multi-turn dialogues.

**Decision**: Structured yet flexible account plan generation
**Rationale**: Balances standardization for consistency with adaptability for different company types and research depths.

### Technical Implementation Choices
**Decision**: Streamlit framework for rapid prototyping and deployment
**Rationale**: Enables focus on agent intelligence rather than UI complexity while providing professional web interface.

**Decision**: Modular architecture with separation of concerns
**Rationale**: Enhances maintainability, testing capability, and future extensibility. Clear boundaries between components.

**Decision**: DuckDuckGo for search functionality
**Rationale**: Provides real-time data without API key requirements while maintaining privacy focus.

## User Scenario Handling

### The Confused User
- Implementation: Clarifying Assistant persona with proactive questioning
- Technique: Multiple-choice clarification and guided discovery
- Example: "I'm not sure what to research" triggers step-by-step assistance

### The Efficient User
- Implementation: Efficient User persona with bullet-point responses
- Technique: Information prioritization and concise delivery
- Example: "Quick bullet points on Tesla" returns structured highlights

### The Chatty User
- Implementation: Context maintenance with gentle redirection
- Technique: Acknowledgment of off-topic content with research focus retention
- Example: Handling personal anecdotes while maintaining research objectives

### Edge Case Users
- Implementation: Comprehensive error handling and graceful degradation
- Technique: Clear communication of limitations with helpful alternatives
- Example: Invalid company names trigger helpful suggestions rather than errors

## Technical Specifications

### Dependencies and Requirements
- Python 3.8+
- Streamlit 1.28+ for web interface
- Google Generative AI for core intelligence
- DuckDuckGo Search API for real-time data
- Pyttsx3 for text-to-speech functionality
- Additional packages for audio processing and utilities

### Installation and Setup

#### Local Development
1. Clone the repository:
```bash
git clone https://github.com/amanchauhan786/ResearchCompanyAgenticAI.git
cd ResearchCompanyAgenticAI
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run main.py
```

#### Cloud Deployment
The application is deployed on Streamlit Community Cloud and accessible at:
**https://agenticairesearch.streamlit.app/**

### Configuration Options
- AI persona selection (5 distinct styles)
- Audio settings (auto-play enable/disable)
- Search preferences and result limits
- Account plan template customization

## Live Demo Access

### Immediate Testing
Visit the deployed application: **https://agenticairesearch.streamlit.app/**

### API Key Requirement
To use the application, you need a Google Gemini API key:
1. Visit https://aistudio.google.com/
2. Create an API key
3. Enter the key in the application sidebar

### Test Scenarios for Demonstration
1. **Basic Research**: "Research Tesla company"
2. **Persona Testing**: "Research Microsoft as Creative Strategist"
3. **Voice Interaction**: Use the microphone button for voice input
4. **Plan Generation**: "Create account plan for Apple"
5. **Edge Cases**: Test with ambiguous or invalid inputs

## Evaluation Criteria Alignment

### Conversational Quality
- Natural dialogue flow with context maintenance
- Persona-appropriate language and tone
- Professional yet approachable communication style
- Effective handling of various conversation patterns

### Agentic Behaviour
- Proactive status updates and progress reporting
- Intelligent decision-making about search necessity
- Conflict identification and resolution prompting
- Adaptive response strategies based on context

### Technical Implementation
- Robust error handling and graceful degradation
- Efficient data processing and integration
- Responsive user interface with real-time updates
- Reliable voice processing capabilities

### Intelligence & Adaptability
- Context-aware responses and follow-up handling
- Multi-persona adaptation to user preferences
- Intelligent synthesis of multiple information sources
- Flexible account plan generation and modification

## Demonstration Scenarios for Video

1. **Complete User Journey**: From initial confusion to comprehensive account plan generation
2. **Persona Comparison**: Same research request handled by different AI personas
3. **Multi-Modal Interaction**: Seamless switching between text and voice modes
4. **Edge Case Handling**: Graceful management of invalid inputs and ambiguous requests
5. **Real-time Plan Editing**: Interactive modification of generated account plans

## Project Repository

**GitHub Repository**: https://github.com/amanchauhan786/ResearchCompanyAgenticAI

### Repository Structure
```
ResearchCompanyAgenticAI/
├── main.py                 # Primary application interface
├── agent.py               # Core AI agent logic
├── tools.py               # Search and data processing
├── audio.py               # Voice input/output handling
├── requirements.txt       # Project dependencies
└── README.md             # Comprehensive documentation
```

## Limitations and Future Enhancements

### Current Limitations
- Search functionality dependent on external service availability
- Audio features require system-level text-to-speech support
- English language limitation for international deployment
- Limited to publicly available company information

### Enhancement Opportunities
- Additional data source integrations (financial APIs, news feeds)
- Multi-language support for global usability
- Advanced analytics and visualization capabilities
- Collaborative features for team-based research
- Extended persona library for specialized use cases

## Submission Compliance

This implementation fully addresses all specified requirements:
- Interactive company research through natural conversation
- Multi-source information gathering and synthesis
- Research process updates and conflict detection
- Interactive account plan generation and editing
- Dual interaction modes (text and voice)
- Comprehensive documentation including architecture and design decisions

The agent demonstrates sophisticated conversational capabilities, intelligent agentic behavior, robust technical implementation, and adaptive intelligence across multiple user scenarios.

## Contact and Support

For questions or issues regarding the deployed application or source code, please refer to the GitHub repository or contact through the submission platform.

---
**Live Application**: https://agenticairesearch.streamlit.app/

**Source Code**: https://github.com/amanchauhan786/ResearchCompanyAgenticAI

**Submission Date**: November 2024
