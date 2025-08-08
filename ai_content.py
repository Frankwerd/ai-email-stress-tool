# ai_content.py
import google.generativeai as genai

def generate_email_content(api_key: str, purpose: str, tone: str) -> dict:
    """
    Calls the Google Gemini API to generate an email with a specific tone.
    """
    try:
        genai.configure(api_key=api_key)
        print("--- Calling Google Gemini API... ---")

        # The prompt now includes the 'tone' for more control
        prompt_content = f"""
        Generate a subject line and an email body.
        The purpose of this email is: "{purpose}".
        The desired tone of the email must be: "{tone}".
        
        Please format the entire response as follows, with no extra text before or after:
        Subject: [The subject you generate]
        |||
        [The email body you generate]
        """
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt_content)
        ai_text = response.text.strip()
        
        if "|||" in ai_text:
            subject_part, body = ai_text.split("|||", 1)
            subject = subject_part.replace("Subject:", "").strip()
            return {"subject": subject, "body": body.strip()}
        else:
            print("Warning: AI response did not contain the '|||' separator.")
            return {"subject": f"AI Test for {purpose}", "body": ai_text}

    except Exception as e:
        if "API key not valid" in str(e):
            print("!!!!!!!! AUTHENTICATION FAILED: The provided API key is not valid. !!!!!!!!")
        else:
            print(f"!!!!!!!! An error occurred with the Google Gemini API: {e} !!!!!!!!")
        return None