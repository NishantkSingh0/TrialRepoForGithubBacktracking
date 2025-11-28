import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

genai.configure(api_key=os.getenv("Gemini"))

model = genai.GenerativeModel("gemini-1.5-pro")

def respond(prompt: str):
    print("Input Prompt:",prompt)
    SystemPrompt=("""You are an AI that summarizes Git commit histories into easy-to-read execution flow descriptions.
The Description provided you is like a Descriptions of most important commits on an repository. you have to explain them in flow as given below.
### Task:
- Commits are grouped in 5s, separated by "---".
- For each group, write a **#### heading** summarizing the theme.
- Then write a **5-6 line description** of what the commits likely do and their impact on project flow.
- Focus on meaningful changes (features, fixes, refactors, security, performance, CI).
- Be concise, insightful, and preserve '---' separators between groups.

### Output Format:
#### <Heading for these commits> [Step 1]:-
<5-6 line description of these commits>
---
#### <Heading for next commits> [Step 2]:-
<5-6 line description of these commits>
---
#### <Heading for next commits> [Step 3]:-
<5-6 line description of these commits>"""
)
    
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": SystemPrompt
                    },
                    {"text": prompt}
                ]
            }
        ],
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 1500
        }
    )
    print("OutputResponse:",response.text)
    return response.text