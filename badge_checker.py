import requests
import time

# URL da API
url = "https://badges.roblox.com/v1/universes/486136289/badges"

# Conjunto para armazenar os valores "id" das respostas anteriores
previous_ids = set()

# URL do webhook do Discord
discord_webhook_url = "https://discord.com/api/webhooks/1101596781462159430/3mFVISOCvFPxi1Mk4c_HozuFu1Qk9hRg4EpNqa2WcNNqVwBrC-oRypI85DQkFjky3a8L"

# Cookie de autenticação (substitua pelo seu cookie real)
auth_cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_DFEBA203F39E8504FC6B96786984AF75CB475D1E3AF2B5691FB9FC85D3501BBB7038C367D8C200A27EFBC35352CBCE1C4E52B667F670487C704FFA3ECEEEFDD69AF3749B683C19DE40D8E7F5C65BD5A902F7A8E817DA00BF1F102967ED86284D66D45E27F1493CE4EF6056C2080FC1635EC8D37E4B3178E7DF15553AC050441AA9D9BDA9AC3913F5401937E3578E023FE0D89B5DA23C0106C858A9FDDFB3AC766036C39CB9E85539760F98AE595C28591B5C09D35F6E1524753245A8B54D4004FE3E1BE799DB1385F90B6A2FF4F496535FCD453526ED816E369D4599F5BE975BE1B2E3743E82E964C6E22CBA61BDCE40B8E6498ABA7700B60CF30FABDFE343B2A8D18B601FD4F4D4E4FC6DD7BE0B2ABADA40B35FB312010C93F84AE7294082F2419121F1E02F6DBFBB6AD8164C59AC3B4E5A63644509BE1B3FCC557C7218705C2E54A6489478D7981F4115CCA33A1C227821F49865EACCBAF6A2F7D16C86B2DF42C488BCE96784EFD3AF703C8B1B990DCC4FC5EA1829D5AD86BB3AFA547C4CAFC0CD95C6D5FFBBC85DD78741ABE791C4C3F922FF67DDF7544F8BC5793EAA5F3B987FCA941A9A0D069520EC0786481605439AAC37517482FD4137A40094B046754F022775"

# Headers para a solicitação
headers=({'Cookie': '.ROBLOSECURITY=' + auth_cookie})

# Função para enviar uma mensagem para o webhook do Discord
def send_to_discord_webhook(data):
    content = f"Novo elemento detectado:\n\nNome: {data['name']}\nID: {data['id']}"
    data = {"content": content}
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print("Mensagem enviada com sucesso para o webhook do Discord")
    else:
        print(f"Falha ao enviar mensagem para o webhook do Discord. Código de status: {response.status_code}")

# Loop principal
while True:
    try:
        # Fazer uma solicitação GET para a API com o cookie de autenticação
        response = requests.get(url, headers=headers)

        # Verificar se o limite de taxa foi atingido (mais de 60 solicitações por minuto)
        if response.headers.get('X-RateLimit-Remaining') == '0':
            print("Limite de taxa atingido. Aguardando...")
            time.sleep(60)  # Esperar um minuto antes de fazer a próxima solicitação
        else:
            # Obter os elementos da resposta JSON
            data_list = response.json().get("data")

            # Verificar cada elemento
            for data in data_list:
                current_id = data['id']
                if current_id not in previous_ids:
                    print(f"Novo badge detectado:\n\nNome: {data['name']}\nID: {current_id}")
                    previous_ids.add(current_id)

                    # Enviar os dados para o webhook do Discord
                    send_to_discord_webhook(data)

            # Esperar por um período curto (por exemplo, 10 segundos) antes de fazer a próxima solicitação
            time.sleep(10)

    except Exception as e:
        print(f"Erro ao fazer solicitação: {str(e)}")
        # Esperar por um período curto (por exemplo, 10 segundos) antes de tentar novamente
        time.sleep(10)
