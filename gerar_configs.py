import os
from pathlib import Path

base_path = Path("client_templates/meu_cliente")
base_path.mkdir(parents=True, exist_ok=True)


triage_content = """agent_name: "Triage Agent"
keywords:
  - agent: "Flow Agent"
    keywords:
      - "produto"
      - "serviço"
      - "preço"
      - "comprar"
  - agent: "Knowledge Agent"
    keywords:
      - "documentação"
      - "manual"
      - "como funciona"
      - "erro"
  - agent: "Escalation Agent"
    keywords:
      - "falar com humano"
      - "atendente"
      - "pessoa"
  - agent: "Feedback Agent"
    keywords:
      - "reclamação"
      - "sugestão"
      - "elogio"
"""


flow_content = """agent_name: "Flow Agent"
topics:
  - id: 1
    label: "Vendas"
    keywords: ["comprar", "preço", "orçamento"]
  - id: 2
    label: "Suporte"
    keywords: ["problema", "erro", "ajuda"]
  - id: 3
    label: "Financeiro"
    keywords: ["pagamento", "boleto", "fatura"]
"""

interview_content = """agent_name: "Interview Agent"
interview_questions: |
  Para cada tópico, faça as seguintes perguntas:
  
  ## Vendas
  1. Qual produto você tem interesse?
  2. Qual quantidade desejada?
  3. Qual seu email para contato?
  
  ## Suporte
  1. Descreva o problema
  2. Quando começou?
  3. Já tentou alguma solução?
"""

guardrails_content = """scope: |
  Este assistente pode ajudar com:
  - Informações sobre produtos
  - Suporte técnico
  - Dúvidas sobre serviços

forbidden_topics:
  - "política"
  - "religião"
  - "conteúdo adulto"

out_of_scope_message: |
  Desculpe, não posso ajudar com esse assunto.
  Posso ajudar com produtos, suporte ou serviços.
"""

escalation_content = """name: "Escalation Agent"
triggers:
  explicit_request:
    - "quero falar com um humano"
    - "atendente humano"
    - "falar com uma pessoa"
  frustration:
    - "você não está me ajudando"
    - "isso não resolve"
    
channels:
  phone:
    enabled: true
    number: "0800-123-4567"
    hours: "Seg-Sex 8h-18h"
  email:
    enabled: true
    address: "atendimento@empresa.com"
    sla: "Resposta em até 24h"
  whatsapp:
    enabled: true
    number: "(11) 99999-9999"

business_hours:
  start: 8
  end: 18
  days: [monday, tuesday, wednesday, thursday, friday]

messages:
  greeting: "Entendo que você precisa de um atendimento especializado."
  out_of_hours: "Nosso atendimento funciona de Seg-Sex, 8h-18h."
"""

feedback_content = """name: "Feedback Agent"
protocol_prefix: "SAC"
ticket_types:
  - name: "duvida"
    label: "Dúvida"
    default_priority: "normal"
  - name: "reclamacao"
    label: "Reclamação"
    default_priority: "alta"
  - name: "sugestao"
    label: "Sugestão"
    default_priority: "baixa"

email:
  enabled: true
  brand_color: "#660099"
  brand_name: "Minha Empresa"
  sla_message: "Retornaremos em até 24h úteis."

priorities:
  - name: "baixa"
    sla_hours: 72
  - name: "normal"
    sla_hours: 24
  - name: "alta"
    sla_hours: 8
  - name: "urgente"
    sla_hours: 2
"""

files_to_create = {
    "triage_config.yaml": triage_content,
    "flow_config.yaml": flow_content,
    "interview_config.yaml": interview_content,
    "guardrails_config.yaml": guardrails_content,
    "escalation_config.yaml": escalation_content,
    "feedback_config.yaml": feedback_content
}

print("⚙️ Gerando arquivos de configuração...")
for filename, content in files_to_create.items():
    with open(base_path / filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Criado: client_templates/meu_cliente/{filename}")

print("\n🚀 Configurações salvas com sucesso!")