import requests
import json

class ChatService:
    def __init__(self) -> None:
                # URL da API (neste exemplo, estamos utilizando a API de clima da OpenWeatherMap)
        self.api_url = f"https://dkmtfrbiz5nnu6nfrzpfivqfjq0jqejz.lambda-url.us-east-1.on.aws/session"#"https://whgwhoynzp365r4yqpeucj4cdm0rffop.lambda-url.us-east-1.on.aws/session"

        # Parâmetros da requisição (substitua 'YOUR_API_KEY' pela sua chave de API)
        self.params = {}

        self.header={"Content-Type": "application/json"}

    def chat(self,query,chat_session,prompt):
        body = {
        "prompt": {
            "prompt": prompt,
            "user_message": query
        }
        }
        # Realiza a requisição POST à API
        response = requests.post(self.api_url+f'/{chat_session}', json=body, headers=self.header)
        ebi = response.json()["EBI"]
        return ebi,response.json()["Ai_response"]
    
    def history(self,chat_session):
        #{"role": "user", "content": prompt}
        response = requests.get(self.api_url+f'/{chat_session}/history')
        history = response.json()['history'] 
        history_formated = []
        for item in history:
            if item['type'] == "human":
                history_formated.append({'role':"user","content":item['content']})
            if item['type'] == "ai":
                history_formated.append({'role':"assistant","content":item['content']})
        return history_formated
    
    def ebi(self,chat_session):
        #{"role": "user", "content": prompt}
        response = requests.get(self.api_url+f'/{chat_session}/history')
        ebi = response.json()['EBI']   
        if isinstance(ebi,dict):
            return ebi
        else:
            return None
    
    def chat_list(self):
        response = requests.get(self.api_url+'/list')
        return  response.json()["Session_ids"]


if __name__ == "__main__":
    prompt = "você é um assistente"
    chat = ChatService(12,prompt)
    print(chat.chat("Olá!"))
    #print(chat.history())
    #print(chat.chat_list())
