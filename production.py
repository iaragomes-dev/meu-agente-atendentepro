import asyncio
import os
import datetime # <--- Novidade: Para saber a hora da mensagem
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

load_dotenv()

# Função simples para gravar no arquivo (O "MonkAI" caseiro)
def salvar_log(quem, mensagem):
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{agora}] {quem}: {mensagem}\n"
    
    # Abre o arquivo 'historico_conversas.txt' e adiciona a linha no final
    with open("historico_conversas.txt", "a", encoding="utf-8") as f:
        f.write(linha)

async def main():
    print("☁️  Iniciando AtendentePro (Com Registro de Logs)...")

    try:
        client_azure = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        deploy_name = os.getenv("AZURE_DEPLOYMENT_NAME")
    except Exception as e:
        print(f"❌ Erro de Configuração: {e}")
        return

    # O SUPER PROMPT (Mantivemos igual)
    super_prompt = """
    VOCÊ É O ASSISTENTE VIRTUAL DA "MINHA EMPRESA".
    DIRETRIZES:
    1. TOM DE VOZ: Profissional, empático, use emojis moderadamente (👋, ✅).
    2. SE PEDIR HUMANO: Passe IMEDIATAMENTE: 
       📞 0800-123-4567 | 📧 atendimento@empresa.com | 💬 (11) 99999-9999
    3. SE FOR RECLAMAÇÃO: Acolha, pergunte detalhes e confirme o registro.
    """

    print(f"✅ Conectado! Logs sendo salvos em 'historico_conversas.txt'")
    print("💬 Digite 'sair' para encerrar.\n")
    
    salvar_log("SISTEMA", "--- Nova Sessão Iniciada ---")

    messages = [{"role": "system", "content": super_prompt}]

    while True:
        user_input = input("👤 Você: ")
        if user_input.lower() in ["sair", "exit"]:
            salvar_log("SISTEMA", "--- Sessão Encerrada ---\n")
            break
            
        # 1. Salva o que você falou
        salvar_log("USUÁRIO", user_input)
        messages.append({"role": "user", "content": user_input})

        try:
            response = await client_azure.chat.completions.create(
                model=deploy_name,
                messages=messages,
                temperature=0.7
            )
            bot_reply = response.choices[0].message.content
            
            print(f"🤖 Bot: {bot_reply}\n")
            
            # 2. Salva o que o Robô falou
            salvar_log("ROBÔ", bot_reply)
            
            messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"❌ Erro: {e}")
            salvar_log("ERRO", str(e))

if __name__ == "__main__":
    asyncio.run(main())