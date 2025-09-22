from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# get your API key

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Define the prompt template
prompt = PromptTemplate.from_template("")

# Set up Gemini model

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4,
    google_api_key = GOOGLE_API_KEY
)


# Run it
messages = [
    ("system", """You are a senior medical assistant AI with 10+ years of experience assisting dentists and doctors. 
You are highly skilled at:
- Understanding informal or slang conversations between doctor and patient
- Correcting spelling mistakes and inferring missing words in patient speech
- Extracting structured clinical information

Always:
- Prioritize accuracy and patient safety
- Prefer the doctor’s known medicine preferences when available
- Keep problem and case descriptions short (2–4 words each)
- Follow-up should be schedule based on current date
- Output only the requested JSON in correct structure
- If unsure about medicines or causes, search the web (if tool access is enabled) or say "Not sure" instead of guessing dangerously
- Never make up patient details not implied from the conversation

You are NOT providing a medical diagnosis; you are only structuring information from the conversation to assist the doctor.
"""),
    
    ("user", """Doctor and patient conversation (may contain slang, missing words, or informal language):
---
{conversation_text}
---

Doctor usually recommends these dental medicines:
- Ibuprofen 400mg (pain relief)
- Amoxicillin 500mg (antibiotic)
- Metronidazole 400mg (for infection)
- Diclofenac 50mg (pain relief)
- Chlorhexidine mouthwash (oral rinse)
- Paracetamol 500mg (mild pain)
- Vitamin B-complex (nerve pain support)
- Clotrimazole mouth paint (oral antifungal)

Other medicines available by domain:
- Cefixime 200mg (antibiotic)
- Ketorol-DT 10mg (strong painkiller)
- Mox-Clav 625mg (broad spectrum antibiotic)
- Benzocaine gel (topical numbing gel)
- Lidocaine oral spray (local anaesthetic)
- Pantoprazole 40mg (gastric protection with antibiotics)
- Multivitamin syrup
- Calcium supplements

Cases usually handled by this doctor:
- jaw swelling
- tooth pain
- gum bleeding
- tooth decay
- mouth ulcers
- sensitive teeth
- broken tooth
- wisdom tooth pain
- dental cleaning
- bad breath

Your task:
1. Understand the conversation, even if it contains slang or spelling errors.
2. Identify:
   - patient name (if mentioned)
   - patient age (if mentioned)
   - list of problems (2–4 words each)
   - suggested medicines (prefer doctor's list first)
   - possible causes (short 5-7 words approx each)
   - expected follow-up action (if any), example: if follow_up is tommorow than current_date+1 
3. Respond strictly in this JSON format:

```json
{{
  "name": "<string or null>",
  "age": "<number or null>",
  "case": ["<short problem 1>", "<short problem 2>", or more (if any)],
  "medicine": ["<medicine 1>", "<medicine 2>", or more (if any)],
  "cause": ["<short cause 1>", "<short cause 2>"],
  "follow_up": "<YYYY-MM-DD or null>"
}}

IMP Note: in case of NULL value, it's best to exclude that key from JSON
"""),
]
prompt_template = ChatPromptTemplate.from_messages(messages)

def parse_input(text):
    prompt = prompt_template.invoke({"conversation_text": text})
    response = llm.invoke(prompt)

    try:
        content = re.sub(r"```(json)?", "", response.content).strip()
        data = json.loads(content)
        return {"status": True, "data": data}
    except Exception as a:
        return {"status": False, "message": a}