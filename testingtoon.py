import os
import time
import json
from dotenv import load_dotenv
from google import genai as gemini 


load_dotenv()
try:

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:

        raise ValueError("GEMINI_API_KEY not found in environment variables.")
except ValueError as e:
    print(f"Error: {e}")
    exit()

client = gemini.Client(api_key=GEMINI_API_KEY)

MODEL = 'gemini-2.5-flash' 

NUM_RECORDS = 20
USER_PROMPT = (
    f"Generate exactly {NUM_RECORDS} F1 driver records for a single, recent season. "
    "Use realistic driver numbers, names, teams, and total points. "
    "Do not include any introductory or concluding text. Just the data."
)


def run_test(format_name: str, system_prompt: str, user_prompt: str) -> dict:
    """Runs the Gemini API call and extracts performance metrics."""
    
    print(f"-> Running Test: {format_name}...")
    
    start_time = time.time()
    
    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=[user_prompt],
            config={
                "system_instruction": system_prompt,
                "temperature": 0.0,
            }
        )
    except Exception as e:
        print(f"API Error during {format_name} test: {e}")
        return {"Format": format_name, "Error": str(e)}

    end_time = time.time()
    
    output_text = response.text.strip()
    
    usage = response.usage_metadata
    output_tokens = usage.candidates_token_count

    total_time = end_time - start_time
    output_bytes = len(output_text.encode('utf-8'))
    tokens_per_sec = output_tokens / total_time if total_time > 0 else 0
    
    return {
        "Format": format_name,
        "Output Tokens": output_tokens,
        "Bytes": output_bytes,
        "Time Taken (s)": round(total_time, 4),
        "Tokens/Sec": round(tokens_per_sec, 2),
        "Raw Output (Preview)": output_text[:60].replace('\n', ' | ') + "..."
    }

json_system_prompt = (
    "Output the requested list of F1 driver records in **STANDARD, PRETTY-PRINTED JSON** "
    "format. The structure must be an array of objects with keys: 'number', 'name', 'team', 'points'. "
    "Use indentation and newlines for readability. Do not use markdown code fences."
)
json_results = run_test("Standard JSON", json_system_prompt, USER_PROMPT)


minified_json_system_prompt = (
    "Output the requested list of F1 driver records in **MINIFIED JSON** format. "
    "The output must be on a **single line** with absolutely no whitespace, newlines, or indentation. "
    "Use the key structure: 'number', 'name', 'team', 'points'. Do not use markdown code fences."
)
minified_json_results = run_test("Minified JSON", minified_json_system_prompt, USER_PROMPT)


yaml_system_prompt = (
    "Output the requested list of F1 driver records in **YAML** format. The list items must be prefixed with a hyphen (-) and use keys: 'number', 'name', 'team', 'points'. Do not use markdown code fences."
)
yaml_results = run_test("YAML", yaml_system_prompt, USER_PROMPT)

toon_system_prompt = (
    "Output the requested list of F1 driver records in the **TOON (Token-Oriented Object Notation)** format. "
    "The header must be exactly: `drivers[20]{number, name, team, points}:` "
    "Each driver's data must be on a new line, comma-separated. Do not use markdown code fences."
)
toon_results = run_test("TOON", toon_system_prompt, USER_PROMPT)

csv_system_prompt = (
    "Output the requested list of F1 driver records in **CSV** format. "
    "Include only the 20 data rows, separated by commas, in this exact column order: number, name, team, points. "
    "DO NOT include any header row, quotes, or markdown code fences. Just the data."
)
csv_results = run_test("CSV", csv_system_prompt, USER_PROMPT)




print("\n" + "="*70)
print("F1 DATA SERIALIZATION BENCHMARK RESULTS (Gemini API)")
print("="*70)

results = [json_results, minified_json_results, yaml_results, toon_results, csv_results]


def display_results(results):

    valid_results = [r for r in results if "Error" not in r]

    if not valid_results:
        print("No successful test results to display.")
        return

    header = list(valid_results[0].keys())
    col_widths = {key: len(key) for key in header}
    
    for row in valid_results:
        for key, value in row.items():
            col_widths[key] = max(col_widths[key], len(str(value)))

    header_line = " | ".join(f"{col:<{col_widths.get(col, len(col))}}" for col in header)
    print(header_line)
    print("-" * len(header_line))

    for row in results:
        if "Error" in row:
             print(f"{row['Format']:<{col_widths['Format']}} | ERROR: {row['Error']}")
        else:
            data_line = " | ".join(f"{str(row.get(col, 'N/A')):<{col_widths.get(col, len(col))}}" for col in header)
            print(data_line)

display_results(results)

print("\n**Key Takeaway:** Compare 'Output Tokens' to see how TOON minimizes structural overhead (brackets, quotes, repeated keys) compared to JSON/YAML, while offering structure absent in CSV.")