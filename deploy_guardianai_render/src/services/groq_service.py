"""
Serviço de Inferência: Cliente Groq Cloud (openai/gpt-oss-120b com Fallback REST)
"""
import json
import logging
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from src.core.config import MODEL_NAME, GROQ_API_KEY
from src.core.prompts import SYSTEM_INSTRUCTION
from src.schemas.chat import MensagemHistorico

logger = logging.getLogger("GuardianAI.GroqService")

try:
    from groq import Groq
    HAS_GROQ_SDK = True
except ImportError:
    Groq = None
    HAS_GROQ_SDK = False

class GroqService:
    """
    Gerencia a comunicação com a API do Groq (ultra-baixa latência em LPU),
    consumindo o modelo open-weight 'openai/gpt-oss-120b'.
    Possui suporte tanto via SDK oficial 'groq' quanto via fallback REST nativo (urllib).
    Implementa janela deslizante para preservação de histórico sem contaminação contextual.
    """

    MAX_HISTORICO_TURNOS = 6

    @classmethod
    def formatar_mensagens(
        cls,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> List[Dict[str, str]]:
        """
        Formata o histórico e a instrução de sistema no padrão OpenAI/Groq Chat Completions.
        """
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_INSTRUCTION}
        ]

        if historico:
            historico_recente = historico[-cls.MAX_HISTORICO_TURNOS:]
            for msg in historico_recente:
                if not msg.text or not msg.text.strip():
                    continue
                role = "user" if msg.sender.lower() in ["user", "tutor", "cliente"] else "assistant"
                messages.append({
                    "role": role,
                    "content": msg.text.strip()
                })

        messages.append({
            "role": "user",
            "content": prompt_atual.strip()
        })
        return messages

    @classmethod
    def chamar_via_rest(
        cls,
        api_key: str,
        messages: List[Dict[str, str]]
    ) -> Optional[str]:
        """
        Fallback resiliente utilizando HTTP REST nativo sem dependências externas.
        """
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.6,
            "max_tokens": 800
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "PetGuardian-AI/2.0"
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        url = "https://api.groq.com/openai/v1/chat/completions"

        try:
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    dados = json.loads(response.read().decode("utf-8"))
                    choices = dados.get("choices", [])
                    if choices and "message" in choices[0]:
                        conteudo = choices[0]["message"].get("content")
                        if conteudo and conteudo.strip():
                            return conteudo.strip()
        except urllib.error.HTTPError as e:
            try:
                erro_detalhe = e.read().decode("utf-8")
                logger.warning(f"[Groq REST] Erro HTTP {e.code} ({MODEL_NAME}): {erro_detalhe}")
            except Exception:
                logger.warning(f"[Groq REST] Erro HTTP {e.code} ({MODEL_NAME})")
        except Exception as e:
            logger.warning(f"[Groq REST] Falha na chamada ({MODEL_NAME}): {e}")
        return None

    @classmethod
    def chamar_via_sdk(
        cls,
        api_key: str,
        messages: List[Dict[str, str]]
    ) -> Optional[str]:
        """
        Executa chamada de inferência via biblioteca oficial 'groq'.
        """
        if not HAS_GROQ_SDK or Groq is None:
            return None

        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,  # type: ignore[arg-type]
                temperature=0.6,
                max_tokens=800
            )
            if completion.choices and completion.choices[0].message.content:
                return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"[Groq SDK] Falha na chamada ({MODEL_NAME}): {e}")
        return None

    @classmethod
    def gerar_resposta(
        cls,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> Optional[str]:
        """
        Executa inferência com a API do Groq, priorizando o SDK e alternando para REST caso necessário.
        """
        if not GROQ_API_KEY:
            return None

        messages = cls.formatar_mensagens(prompt_atual, historico)

        # 1. Tenta SDK oficial groq
        texto_sdk = cls.chamar_via_sdk(GROQ_API_KEY, messages)
        if texto_sdk:
            return texto_sdk

        # 2. Tenta REST nativo direto
        return cls.chamar_via_rest(GROQ_API_KEY, messages)
