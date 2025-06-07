import re
import requests
import json
from datetime import datetime, timedelta
import dateparser  


def extract_task_from_message(message):
    """Extract structured task details from a message using the Gemini API and convert dates."""

    api_key = 'AIzaSyD3D4nbriWWFNhgAa8g0ZkgMAs6DEGsPOI'
    if not api_key:
        raise ValueError("API key not found. Set GEMINI_API_KEY as an environment variable.")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}

    prompt = f'''Extract the following task details from the given message:
       Title: 
       Person: 
       Place: 
       Date: 
       Time: 
       Optional link (if remote)

       Message: "{message}"

       Please structure the output as a JSON with the above fields.
       '''

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()

        candidates = response_data.get("candidates", [])
        if not candidates:
            return {"error": "No candidates found in the response"}

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            return {"error": "No parts found in the response content"}

        extracted_task = parts[0].get("text", "")
        if extracted_task:
            match = re.search(r'```json\n(.*?)\n```', extracted_task, re.DOTALL)
            if match:
                json_data = match.group(1).strip()
                try:
                    task_details = json.loads(json_data)
                    task_details["Date"] = convert_to_absolute_date(task_details.get("Date", ""))
                    return task_details
                except json.JSONDecodeError:
                    return {"error": "Failed to parse extracted task"}
            else:
                return {"error": "No valid JSON found in the extracted task"}

    except requests.RequestException as e:
        return {"error": "Request failed", "details": str(e)}


def convert_to_absolute_date(date_str):
    """Convert words like 'tomorrow' or 'Monday' to a date in dd.mm.yy format."""
    if not date_str:
        return None
    parsed_date = dateparser.parse(date_str, settings={"PREFER_DATES_FROM": "future"})
    if parsed_date:
        return parsed_date.strftime("%d.%m.%y")
    return None


# if __name__ == "__main__":
#     message = "Let's meet tomorrow at the park at 3 PM to discuss the project."
#     task_details = extract_task_from_message(message)
#     print("Extracted Task Details:", task_details)
