"""
Repositório de Persistência do Chat e Auditoria de Triagens
"""
import logging
from typing import Optional, List, Dict, Any
from src.database.connection import get_db_connection

logger = logging.getLogger("GuardianAI.ChatRepository")

class ChatRepository:
    """
    Encapsula todas as operações de banco de dados para mensagens de chat
    e auditoria de triagens clínicas, garantindo SRP e isolamento de SQL.
    """

    @staticmethod
    def salvar_mensagem(
        session_id: str,
        sender: str,
        text: str,
        pet_id: Optional[int] = None
    ) -> bool:
        """
        Registra uma mensagem individual no histórico do SQLite.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO mensagens_chat (session_id, pet_id, sender, text)
                    VALUES (?, ?, ?, ?)
                """, (session_id, pet_id, sender, text))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem no SQLite: {e}")
            return False

    @staticmethod
    def salvar_auditoria(
        session_id: str,
        pergunta: str,
        resposta: str,
        categoria: str,
        urgencia: str,
        origem_resposta: str,
        pet_id: Optional[int] = None,
        nome_pet: Optional[str] = None
    ) -> bool:
        """
        Registra o parecer e metadados da triagem clínica na tabela de auditoria.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO auditoria_triagens (
                        session_id, pet_id, nome_pet, pergunta, resposta,
                        categoria, urgencia, origem_resposta
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, pet_id, nome_pet, pergunta, resposta,
                    categoria, urgencia, origem_resposta
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erro ao registrar auditoria no SQLite: {e}")
            return False

    @staticmethod
    def buscar_historico(
        session_id: Optional[str] = None,
        pet_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Recupera as mensagens filtradas por session_id ou pet_id em ordem cronológica.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                filtros = []
                parametros: List[Any] = []

                if session_id:
                    filtros.append("session_id = ?")
                    parametros.append(session_id)
                if pet_id:
                    filtros.append("pet_id = ?")
                    parametros.append(pet_id)

                where_sql = f"WHERE {' AND '.join(filtros)}" if filtros else ""
                ordem_sql = "ORDER BY id ASC" if filtros else "ORDER BY id DESC"
                parametros.append(limit)

                cursor.execute(f"""
                    SELECT id, session_id, pet_id, sender, text, timestamp
                    FROM mensagens_chat
                    {where_sql}
                    {ordem_sql}
                    LIMIT ?
                """, tuple(parametros))

                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao buscar histórico no SQLite: {e}")
            return []

    @staticmethod
    def listar_auditorias(
        pet_id: Optional[int] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Recupera os registros de auditoria clínica mais recentes.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                where_sql = "WHERE pet_id = ?" if pet_id else ""
                parametros = (pet_id, limit) if pet_id else (limit,)

                cursor.execute(f"""
                    SELECT id, session_id, pet_id, nome_pet, pergunta, resposta,
                           categoria, urgencia, origem_resposta, timestamp
                    FROM auditoria_triagens
                    {where_sql}
                    ORDER BY id DESC
                    LIMIT ?
                """, parametros)

                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao listar auditorias no SQLite: {e}")
            return []

    @staticmethod
    def listar_sessoes(
        pet_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Recupera as sessões de conversa do pet agrupadas, com título baseado na primeira
        pergunta do tutor, quantidade de mensagens e data da última interação.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                where_sql = "WHERE m.pet_id = ?" if pet_id else ""
                parametros = (pet_id, limit) if pet_id else (limit,)

                cursor.execute(f"""
                    SELECT
                        m.session_id,
                        COUNT(*) AS total_mensagens,
                        MAX(m.timestamp) AS last_activity,
                        COALESCE(
                            (SELECT text FROM mensagens_chat WHERE session_id = m.session_id AND sender = 'user' ORDER BY id ASC LIMIT 1),
                            m.text
                        ) AS titulo
                    FROM mensagens_chat m
                    {where_sql}
                    GROUP BY m.session_id
                    ORDER BY MAX(m.id) DESC
                    LIMIT ?
                """, parametros)

                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao listar sessões de chat no SQLite: {e}")
            return []

    @staticmethod
    def excluir_sessao(session_id: str) -> bool:
        """
        Exclui todas as mensagens e registros de auditoria vinculados a uma sessão.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM mensagens_chat WHERE session_id = ?", (session_id,))
                cursor.execute("DELETE FROM auditoria_triagens WHERE session_id = ?", (session_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erro ao excluir sessão {session_id} no SQLite: {e}")
            return False
