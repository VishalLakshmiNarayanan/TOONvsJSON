# **TOON Benchmark**
### Token-Oriented Object Notation vs. Standard Serialization Formats

<p>
Transmitting structured data costs tokens — and tokens cost money.<br>
TOON introduces a <b>token-efficient serialization format</b> that minimizes structural overhead compared to JSON, YAML, and CSV.
</p>

<p>
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.10+-skyblue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini-API-orange?style=for-the-badge"/>
</p>

---

## Overview

This benchmark answers a simple question:

> **"Which data format uses the fewest tokens when generating structured data with LLMs?"**

Using the Gemini 2.5 Flash API, we generate 20 F1 driver records in 5 different formats and measure:
- **Output Tokens** (primary metric)
- **Bytes** (storage efficiency)
- **Time Taken** (latency)
- **Tokens/Sec** (throughput)

---

## Formats Tested

| Format | Description |
|--------|-------------|
| **Standard JSON** | Pretty-printed with indentation and newlines |
| **Minified JSON** | Single-line, no whitespace |
| **YAML** | Hyphen-prefixed list format |
| **TOON** | Token-Oriented Object Notation (custom) |
| **CSV** | Comma-separated values, no header |

---

## TOON Format Example

```
drivers[20]{number, name, team, points}:
1, Max Verstappen, Red Bull Racing, 575
11, Sergio Perez, Red Bull Racing, 285
44, Lewis Hamilton, Mercedes, 234
...
```

**Key Features:**
- Single header declaration with schema
- Minimal delimiters (commas only)
- No repeated keys, quotes, or brackets per record
- Human-readable structure

---

## Results

| Format | Output Tokens | Bytes | Time (s) | Tokens/Sec |
|--------|---------------|-------|----------|------------|
| Standard JSON | ~450 | ~2,100 | 1.2 | 375 |
| Minified JSON | ~320 | ~1,200 | 0.9 | 356 |
| YAML | ~380 | ~1,600 | 1.1 | 345 |
| **TOON** | **~280** | **~950** | 0.8 | 350 |
| CSV | ~250 | ~800 | 0.7 | 357 |

> 📌 **Key Takeaway:**
> TOON achieves **12-38% fewer tokens** than standard JSON while maintaining structural clarity that CSV lacks. For high-volume LLM applications, this translates to significant cost savings.

---

## Tech Stack

<p>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" height="45" />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" height="45" />
</p>

**Libraries:**
- `google-genai` - Gemini API client
- `python-dotenv` - Environment management

---

## Running the Benchmark

```bash
# Install dependencies
pip install google-genai python-dotenv

# Set API key
export GEMINI_API_KEY="your-api-key"

# Run benchmark
python testingtoon.py
```

---

## Use Cases

- **API Cost Optimization** - Reduce token usage in high-volume applications
- **Streaming Applications** - Faster parsing with predictable structure
- **Agent Communication** - Minimize overhead in multi-agent systems
- **IoT/Edge Devices** - Lightweight data transmission

---

## License

MIT
