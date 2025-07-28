Here’s your Chennai.py MoM in a clean and well-structured **Markdown (`.md`) format** for GitHub or any documentation platform:

---

````markdown
# 🐍 Chennai.py Meetup – 26th July 2025  
📍 *Institute of Mathematical Sciences, Chennai*  
✍️ *Minutes recorded by: [Your Name]*  

---

## 1. 🎲 Randomness

- Cannot be predicted
- No true randomness — it is imaginary in computation
- **Seed number** is input to some algorithm — it is *pseudo-random*
    - Common use cases: **Games**, **Cryptography**, **OTPs**
- **Seed value depends on the environment**

### ❌ Approaches That Failed:
1. Updating OS time via faker
2. Overriding the `read()` method to give a static value

### ✅ What Worked:
- Using **system call** like `getRandom()` (which relies on real entropy from OS)

> 💡 *Key Insight:* Randomness in Python is not truly random — it’s environment-driven and often based on system entropy.

---

## 2. 📟 MicroPython

### Flow:
**Python Program → Microcontroller Memory → Display Driver → Screen**

- Boards used: **ESP32**, **Raspberry Pi**
- Display Driver: **ILI9341**
- Interface: **SPI (Serial Peripheral Interface)**

👤 *Contributor Mentioned:* [@praveenmax](https://github.com/praveenmax)

### 🔍 Open Questions:
- What happens in *Immediate Direct* or *Frame Buffer* rendering?
- Where is the frame buffer offloaded to?
- Are SPI commands executed sequentially?
- Which command gets executed first?
- What is the display’s refresh rate?

---

## 3. 🧠 MCP – Model Context Protocol

- Enables **One-to-Many** communication
- Acts as an **abstraction layer** and wrapper around third-party services

### Architecture:
```text
MCP Clients (Models) → MCP Servers → MCP Tools
````

### Workflow:

```
Prompt → LLM → Understand Query → List Tools → MCP Server → Third Party Tool → MCP Server → Extended Context → LLM
```

### 🔎 Key Concepts:

* Maps **prompt words** to **MCP parameters**
* Helps LLMs interact intelligently with tools
* Maintains extended context during multi-step operations

> Think of MCP as a middleware that connects language models with external services and tools seamlessly.

---

## 4. ⚡ Lightning Talk @ 5:40 PM – Randomness in Python

A final lightning talk revisited the topic of randomness in Python. Possibly involved deeper insights or system-level examples.

---

## 🙌 Thanks & Acknowledgements

Big thanks to all:

* Speakers
* Organizers
* Participants
  and the whole **Chennai.py** community for making this a fun and informative session.

---

*Feel free to share, fork, and contribute to the learning!*

```

---

Let me know once you've uploaded this to GitHub — I can help you write the README or suggest how to format it for a blog or social post.
```
