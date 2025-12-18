# Orbi: an Intelligent Travel Assistant

Orbi was born to solve real problems I frequently encounter as a travelling hobbiest.

## ✨ High-Level Overview

The system is a **graph-based conversational assistant** that:

- Maintains conversational context across turns
- Decides when to rely on **LLM knowledge vs. external APIs**
- Integrates **multiple real-world APIs** for factual grounding
- Detects and mitigates hallucinations using techniques such as **verification logic**

---

## 🧠 Assistant Purpose & Capabilities

**Domain:** Travel planning and recommendations

The assistant can handle at least the following task types:

1. **Weather-based questions**
   - Example: *“is April a good time to travel in Tokyo?”*

2. **Recommendations & activities**
   - Example: *“What are the best activities to do in Tokyo?”*

3. **Flights Search**
   - Example: *“What are the available flights from TLV to HND on December 28th, 2025?”*

4. **Time-based questions**
   - Example: *“What is the time difference between Tokyo and Tel-Aviv?”*

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
- Responses prioritize clarity and usefulness

### 2️⃣ Hallucination Handling

- Explicit tool-vs-LLM decision logic
- Verification step after response generation
- Transparency notes when answers are not grounded
- Low temperature (Can be tuned)

### 3️⃣ Context Management

- Conversation history is preserved per session explicitly and implicitly
- Follow-up questions correctly reference prior turns

### 4️⃣ External Data Integration

- At least two external APIs are integrated: 6 APIs are used, from 3 different providers (opem-meteo, amadeus, worldtimeapi)
- Retrieved data is explicitly injected into prompts
- No silent blending of facts and guesses

---

## 🧑‍💻 Interface

- **CLI-based interface** (required by assignment)
- Designed to be easily extended to a web UI

---

## 🔮 Future Improvements

If extended further, the system could include:

- further capabilities, such as:
- travel warning
- recommended vaccinations
- E2E pricing (including food, transportation, entretaiment, insurance, hotels)

- further features, such as:
- Web UI with streaming (SSE / WebSockets)
- breaking down agents to domain-specialized ones, and having one agent that orchestrates them 

- Better design, such as:
- reducing the time to respond (currently queries can take up to 30 seconds)
- Confidence scoring instead of binary verification
- Caching of API responses
- User profiles and preferences
- More advanced recovery strategies after hallucination detection
- Unit tests and automated evaluation scenarios


**Please find the transcripts in the main project folder**
