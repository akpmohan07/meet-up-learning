

---

# 🐍 Chennai.py Meetup – 26th July 2025

📍 *Institute of Mathematical Sciences, Chennai*
✍️ *Minutes recorded by: Mohankumar M*

---

## 🗓️ Schedule

| Time    | Session Title                                              | Speaker          |
| ------- | ---------------------------------------------------------- | ---------------- |
| 3:00 PM | **PseudoRandom in Python**                                 | Madhavakumar     |
| 3:40 PM | **Embedded Graphics & Game Programming using MicroPython** | Praveen          |
| 4:20 PM | **MCP in Action: Supercharge Development with AI**         | Nishanth         |
| 5:00 PM | **Lightning Talks** (5 mins/talk)                          | Multiple         |
| 5:40 PM | **Generating Random Permutations with Python**             | Prof. Amritanshu |

---

## 1. 🎲 PseudoRandom in Python

👤 *Speaker: Madhavakumar*

### 📖 Talk Description:

What is Random? Which Random is Random? Do we actually need Random?
This session dove into the concept of "PseudoRandom" and discussed its advantages, limitations, and real-world implications in Python.

* Randomness cannot be predicted — but no true randomness exists in computation
* **Seed number** is input to an algorithm → gives *pseudo-random* output
* Common uses: **Games**, **Cryptography**, **OTPs**
* **Seed value** is often derived from the environment

### ❌ Approaches That Failed:

1. Updating OS time via faker
2. Overriding the `read()` method to return static data

### ✅ What Worked:

* System calls like `getRandom()` — uses **real entropy** from the OS

> 💡 *Key Insight:* Python’s randomness is deterministic unless fed by an entropy source.

---

## 2. 🎮 Embedded Graphics & Game Programming on MicroPython

👤 *Speaker: Praveen*

### 📖 Talk Description:

In this talk, the audience got an idea of how graphics are processed in **resource-constrained devices** using **MicroPython on ESP32**.
The demo included interfacing various display modules and showcasing a simple game with source code walkthrough.

### Flow:

**Python Program → Microcontroller Memory → Display Driver → Screen**

* Boards used: **ESP32**, **Raspberry Pi**
* Display Driver: **ILI9341**
* Interface: **SPI (Serial Peripheral Interface)**

👤 *Contributor Mentioned:* [https://www.linkedin.com/in/praveenmax/](https://www.linkedin.com/in/praveenmax/)

### 🔍 Open Questions:

* What happens in *Immediate Direct* vs. *Frame Buffer* rendering?
* Where is the frame buffer offloaded to?
* Are SPI commands executed sequentially?
* What determines command priority?
* How is display refresh rate managed?

---

## 3. 🧠 MCP – Model Context Protocol in Action

👤 *Speaker: Nishanth*

### 📖 Talk Description:

This session introduced **MCP (Model Context Protocol)**, explained its setup, and showed how it acts as a middleware that bridges LLMs and developer tools.
The speaker demonstrated a minimal MCP server in Python and a productivity-boosting example such as generating tests using Playwright MCP or similar tool.

### Architecture:

MCP Clients (Models) → MCP Servers → MCP Tools

### Workflow:

Prompt → LLM → Understand Query → List Tools → MCP Server → Third Party Tool → MCP Server → Extended Context → LLM

### 🔑 Concepts:

* Maps **prompts** to **MCP parameters**
* Maintains multi-step **extended context**
* Enables intelligent LLM-tool interaction

> MCP simplifies and scales tool integrations in AI-powered workflows.

---

## 4. ⚡ Lightning Talks

### 🌀 Topic: *Generating Random Permutations with Python*

👤 *Speaker: Prof. Amritanshu*

### 📖 Talk Description:

A crisp 5-minute session exploring how to generate **random permutations** in Python.
Covered efficient techniques using libraries like `random`, `itertools`, and potentially custom shufflers. Emphasis on **correctness**, **uniformity**, and **performance**.

---

## 🙌 Thanks & Acknowledgements

Big thanks to all:

* **Speakers**
* **Organizers**
* **Participants**
* And the whole **Chennai.py** community

for making this a fun, engaging, and insightful meetup!

---

**Feel free to share and contribute to the knowledge!**

---
