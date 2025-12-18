# Orbi: an Intelligent Travel Assistant

Orbi was created to address real-world challenges I frequently encounter as a travel enthusiast.


## ✨ High-Level Overview

The system is a **graph-based conversational assistant** that:

- Maintains conversational context across turns
- Decides when to rely on **LLM knowledge vs. external APIs**
- Integrates **multiple real-world APIs** for factual grounding
- Detects and mitigates hallucinations using techniques such as **verification**

---

## 🧠 Assistant Purpose & Capabilities

**Domain:** Travel planning and recommendations

The assistant can handle at least the following task types:

1. **Weather-based questions**
   - Example: *“is April a good time to travel to Tokyo?”*

2. **Recommendations & activities**
   - Example: *“What are the best activities to do in Tokyo?”*

3. **Flights Search**
   - Example: *“What are the available flights from TLV to HND on December 28th, 2025?”*

4. **Time-based questions**
   - Example: *“What will be the time in Tokyo when i land there, 8 hours from now?”*

---


## 🗂 System Architecture

The system is built around a **LangGraph-based execution graph**, where each node has a single responsibility.
Please scroll down to view a more detailed breakdown of the system.

### Core Components

```
User (CLI)
  ↓
Router Node
  ↓
Execution Node (tool or direct reasoning)
  ↓
Finalizer Node (LLM response + verification)
  ↓
Streaming Output
```

### Key Modules

- **Graph / Nodes** – Control the conversational flow
- **LLM Infrastructure** – Centralized model creation and caching
- **External APIs** – Provide factual grounding
- **Verifier Model** – Detects hallucination risk

---

## 🔄 System Flow (Step by Step)

### 1️⃣ User Input

The user interacts with the assistant through a CLI.
Each input is appended to the conversation state and also kept in memory implicitly using a checkpointer.

---

### 2️⃣ Routing Decision

A router node determines whether the request:

- Can be answered using **general LLM knowledge**, or
- Requires **external data retrieval**

This decision is guided by prompt instructions and explicit rules.

---

### 3️⃣ External Data Integration

When needed, the system calls external APIs, such as:

- **Geocoding API** – Place → coordinates
- **Weather / Climate API** – Coordinates → historical climate data
- **Flight / travel APIs** (where applicable)

The retrieved data is **merged explicitly** into the LLM prompt.

---

### 4️⃣ Response Generation

The main LLM generates a response using:

- Conversation history
- Retrieved external facts (when applicable)
- Prompt constraints designed to reduce hallucinations

Only the **final answer** is returned to the user.

---

### 5️⃣ Hallucination Verification

After generation, a **dedicated verifier LLM (Gemini)** evaluates the answer:

- Was external data required?
- Was external data actually used?
- Is the response potentially misleading?

Based on this check, the system may:

- Add a transparency note
- Flag uncertainty
- Warn the user about non-grounded answers

---

## 🧪 Hallucination Detection & Management

Hallucination mitigation is handled at multiple layers:

### Prompt-Level Controls

- Explicit instructions to distinguish **retrieved facts vs. estimates**
- Requests for step-by-step reasoning (internally)
- Constraints on speculation

### Tool-Usage Enforcement

- Clear decision logic for when tools **must** be used
- Post-response checks to ensure tools were actually invoked

### Verifier Model

- A **separate, deterministic Gemini model** is used
- Non-streaming, temperature = 0
- Focused only on validation, not generation

This separation improves reliability and debuggability.

---

## 📊 How This Meets the Evaluation Criteria

### 1️⃣ Conversation Quality

- Multi-turn context is preserved using a graph-based state
- Clarifying questions are asked only when necessary
- Responses prioritize clarity and usefulness through carefully crafted system prompts

### 2️⃣ Hallucination Handling

- Explicit tool-vs-LLM decision logic (e.g., “Is factual information required?”)
- Verification step executed after response generation
- Transparency notes added when responses are not grounded in external data
- Low model temperature (0.2 as default) to reduce variance and hallucinations (configurable)

### 3️⃣ Context Management

* Conversation history is preserved **per session**, both explicitly (via the message list) and implicitly (using an in-memory checkpointer)
* Follow-up questions correctly reference and build upon prior turns in the conversation
* In testing, the LLM demonstrated effective use of conversational context; for example, after asking *“What is the time in China?”* and encountering a network error, a subsequent *“Try again”* prompt was correctly interpreted as referring to China, and the request was reissued accordingly


### 4️⃣ External Data Integration

- Tools are invoked **only when appropriate**, based on explicit tool descriptions and clear detection of factual information requirements
- The system integrates **multiple external APIs**: six APIs across three providers (Open-Meteo, Amadeus, and WorldTimeAPI)
- Retrieved external data is **explicitly injected into the LLM prompts** rather than implicitly assumed
- The system avoids **silent blending of factual data and model assumptions**, preserving transparency and accuracy

---

## 🧑‍💻 Interface

- **CLI-based interface** (required by assignment)
- Designed to be easily extended to a web UI

---

## 🔮 Future Improvements

If extended further, the system could be enhanced in several directions:

### Expanded Capabilities

* Travel warnings and safety advisories
* Recommended vaccinations based on destination
* End-to-end cost estimation, including:
  * Flights
  * Accommodation
  * Food
  * Local transportation
  * Insurance and entertainment

### Additional Features

* Web-based UI with streaming support (SSE / WebSockets)
* Decomposition into domain-specialized agents coordinated by a central orchestrator

### Architectural & Quality Improvements

* Reduced response latency (currently some queries may take up to 30 seconds)
* Confidence scoring instead of binary verification
* Caching of external API responses that don't update frequently
* Persistent user profiles and preferences
* More advanced recovery strategies after hallucination detection
* Comprehensive unit tests and automated evaluation scenarios

---


**IMPORTANT NOTE**
**Please find the transcripts in the dedicated "transcripts" folder.**


**RUNNING THE PROJECT**:

Prerequisites
Ensure you have the following installed:
- Python 3.10+
- UV package manager
- Git


# Running Orbi with `uv`

This guide explains how to run the **Orbi Intelligent Travel Assistant** end‑to‑end using **`uv`**, a fast Python package manager and environment runner.

---

## 1️⃣ Install `uv`

If you do not already have `uv` installed:

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

---

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/Wex47/Orbi.git
cd orbi
```

---

## 3️⃣ Install Dependencies

From the project root, run:

```bash
uv sync
```

This will:

* Create an isolated Python environment
* Install all dependencies defined in `pyproject.toml`
* Use `uv.lock` (if present) for reproducible installs

No manual virtual‑environment activation is required.

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root with the following values:

```env
# LLM Providers
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key   # required if using Claude

# Amadeus (Flights API)
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
```

### Notes

* `GOOGLE_API_KEY` is required for the **Gemini verifier model**
* `ANTHROPIC_API_KEY` is required if the main chat model is Claude
* Open‑Meteo and WorldTimeAPI do not require authentication

---

## 5️⃣ Run the Assistant (CLI)

Start the assistant using:

```bash
uv run python -m app.main
```

You should see output similar to:

```
[thread_id=...] (set THREAD_ID env var to resume)

You:
```

The assistant is now ready to accept input.

---

## 6️⃣ Example Queries

Try queries such as:

```text
What’s the weather like in Paris in April?
Is January a good time to visit Tokyo?
What flights are available from TLV to HND on December 28th, 2025?
What is the time difference between Tel Aviv and Tokyo?
```

The system will:

* Route the query (direct vs tool‑based)
* Call external APIs when required
* Verify the response using a dedicated verifier LLM
* Stream the final answer to the CLI

-----

No further setup is required.