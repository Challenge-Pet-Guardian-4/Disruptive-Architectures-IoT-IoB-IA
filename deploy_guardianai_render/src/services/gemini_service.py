"""
Serviço de Inferência: Cliente Google Gemini (SDK Oficial com Fallback REST)
"""
import json
import logging
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from src.core.config import MODEL_NAME, GEMINI_API_KEY
from src.core.prompts import SYSTEM_INSTRUCTION
from src.schemas.chat import MensagemHistorico

logger = logging.getLogger("GuardianAI.GeminiService")

try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    genai = None
    types = None
    HAS_GENAI_SDK = False

class GeminiService:
    """
    Gerencia a comunicação com os modelos da família Gemini,
    suportando chamadas via SDK oficial google-genai e fallback resiliente via REST.
    Implementa janela deslizante para preservação de histórico sem contaminação contextual.
    """

    MAX_HISTORICO_TURNOS = 6

    @classmethod
    def formatar_contents_rest(
        cls,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> List[Dict[str, Any]]:
        contents = []
        if historico:
            # Janela deslizante de segurança
            historico_recente = historico[-cls.MAX_HISTORICO_TURNOS:]
            for msg in historico_recente:
                if not msg.text or not msg.text.strip():
                    continue
                role = "user" if msg.sender.lower() in ["user", "tutor", "cliente"] else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.text.strip()}]
                })
        
        contents.append({
            "role": "user",
            "parts": [{"text": prompt_atual.strip()}]
        })
        return contents

    @classmethod
    def chamar_via_rest(
        cls,
        api_key: str,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> Optional[str]:
        contents = cls.formatar_contents_rest(prompt_atual, historico)
        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            },
            "generationConfig": {
                "temperature": 0.6,
                "maxOutputTokens": 800
            }
        }
        headers = {"Content-Type": "application/json"}
        body_bytes = json.dumps(payload).encode("utf-8")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"

        try:
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    dados = json.loads(response.read().decode("utf-8"))
                    candidates = dados.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
        except Exception as e:
            logger.warning(f"[Gemini REST] Falha na chamada ({MODEL_NAME}): {e}")
        return None

    @classmethod
    def chamar_via_sdk(
        cls,
        api_key: str,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> Optional[str]:
        if not HAS_GENAI_SDK or genai is None or types is None:
            return None

        try:
            client = genai.Client(api_key=api_key)

            contents_sdk = []
            if historico:
                historico_recente = historico[-cls.MAX_HISTORICO_TURNOS:]
                for msg in historico_recente:
                    if not msg.text or not msg.text.strip():
                        continue
                    role = "user" if msg.sender.lower() in ["user", "tutor", "cliente"] else "model"
                    contents_sdk.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg.text.strip())]
                    ))

            contents_sdk.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt_atual.strip())]
            ))

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents_sdk,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.6,
                    max_output_tokens=800
                )
            )
            if response and response.text:
                return response.text
        except Exception as e:
            logger.warning(f"[Gemini SDK] Falha na chamada ({MODEL_NAME}): {e}")
        return None

    @classmethod
    def gerar_resposta(
        cls,
        prompt_atual: str,
        historico: Optional[List[MensagemHistorico]] = None
    ) -> Optional[str]:
        """
        Executa inferência com chave de API, tentando o SDK oficial e utilizando REST como fallback.
        """
        if not GEMINI_API_KEY:
            return None

        # 1. Tenta SDK oficial google-genai
        texto_sdk = cls.chamar_via_sdk(GEMINI_API_KEY, prompt_atual, historico)
        if texto_sdk:
            return texto_sdk

        # 2. Tenta REST direto
        return cls.chamar_via_rest(GEMINI_API_KEY, prompt_atual, historico)
