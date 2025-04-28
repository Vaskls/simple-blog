from passlib.context import CryptContext
import requests
import random
import json
from .config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Generate():
     
    @staticmethod
    def random_color():
        # Generates random hex value for the color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)

    # generate random string for salt

    @staticmethod
    def random_cat():
        # Generates link to random cat picture
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
            return response.json()[0]['url']
        except Exception as e: # Api is down
            print(e)
            return "https://miramarvet.com.au/wp-content/uploads/2021/08/api-cat2.jpg"


    @staticmethod
    def hashed_password(password: str) -> str:
        return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def filter_middleware(contents):
    try:
        payload = json.dumps({
            "model": "deepseek/deepseek-chat:free",
            "messages": [
            {
                "role": "user",
                "content": f"""I'll provide you with comment. 
            
Your response should have all the offensive / racist / inappropriate / harmful / in-exclusive content replaced with appropriete numbers of "*" symbol. 
EVERYTHING which's not not offensive should remain in your final response.
DO NOT ADD ANYTHING ELSE EXCEPT ORIGINAL CONTENT POST FILTER IN YOUR RESPONSE.

Contents for filtering: \n\n
{contents}
            """
            }
        ]})
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            
            data=payload,
        )
        filtered_result = response.json()['choices'][0]['message']['content'] # if we don't get correct json it throws an error, so we don't filter anythng
        print("OK")
        return filtered_result
    except Exception as e:
        print(str(e))
        return contents