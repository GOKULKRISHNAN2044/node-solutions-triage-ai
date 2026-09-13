from google import genai
from google.genai import types
import json
from settings import config

_client = genai.Client(api_key=config.gemini_api_key)

SYSTEM_PROMPT = """
You are an expert business request triage assistant for a professional-services company.

Your job is to analyze incoming client requests and return a structured JSON response.

Always return ONLY a valid JSON object with no extra text, explanation, or markdown.

The JSON must contain exactly these fields:
{
  "summary": "One sentence summarizing the request",
  "category": "One of: Sales | Support | Billing | Technical | Other",
  "priority": "One of: Low | Medium | High | Urgent",
  "priority_reason": "One sentence explaining why this priority was assigned",
  "route": "One of: Sales Team | Client Success | Finance | Engineering",
  "draft_response": "A professional 2-4 sentence first reply to this request"
}

Priority Guidelines:
- Urgent: System down, data breach, security incident, unauthorized data access, immediate financial risk
- High: Business operations affected, client blocked, time-sensitive deadline within 24hrs
- Medium: Important but not time-critical, requires response within 24-48 hours
- Low: General inquiries, future improvement ideas, no deadline mentioned

Routing Guidelines:
- Sales Team: New prospects, pricing inquiries, demos, upsell opportunities
- Client Success: General support, access issues, onboarding problems, complaints
- Finance: Invoice disputes, billing errors, payment issues, refunds
- Engineering: Technical bugs, system outages, data issues, integrations, security incidents

CRITICAL OVERRIDE RULE:
If the request involves a data breach, unauthorized access, or security incident —
always set priority to "Urgent" and route to "Engineering" regardless of other signals.
"""


def analyze_request(request_text: str) -> dict:
    """
    Sends the request text to Gemini 2.5 Flash and returns
    a structured triage dict with all 5 output fields.
    """
    prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this incoming business request:\n\n\"{request_text}\""

    try:
        response = _client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        result = json.loads(response.text)

        required_keys = {"summary", "category", "priority", "priority_reason", "route", "draft_response"}
        if not required_keys.issubset(result.keys()):
            missing = required_keys - result.keys()
            raise ValueError(f"Gemini response missing fields: {missing}")

        return result

    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")
