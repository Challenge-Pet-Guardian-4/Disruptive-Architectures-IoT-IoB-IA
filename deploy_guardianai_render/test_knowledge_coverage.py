"""
Teste de cobertura da Base de Conhecimento: cada pergunta deve recuperar o chunk esperado
entre os 2 primeiros resultados, e perguntas fora de escopo não devem recuperar nada.
Uso: python test_knowledge_coverage.py   (executar dentro de deploy_guardianai_render)
"""
import sys

from src.knowledge import BASE_CHUNKS_RAG
from src.services.knowledge_service import KnowledgeService

CASOS = [
    ("Meu gato arranha o sofá o tempo todo", "beh_03"),
    ("Meu cachorro late demais e destrói tudo", "beh_02"),
    ("Meu gato faz xixi fora da caixa de areia", "beh_04"),
    ("Como adestrar meu filhote sem gritar?", "beh_01"),
    ("Meu cachorro rosnou e mordeu", "beh_05"),
    ("Com que frequência dou banho no meu cachorro?", "hyg_01"),
    ("Como evitar pulgas e carrapatos?", "hyg_02"),
    ("Meu cão está se coçando muito e perdendo pelo", "hyg_03"),
    ("Como limpar o ouvido do meu cachorro?", "hyg_04"),
    ("Como cortar as unhas do meu gato?", "hyg_05"),
    ("Posso raspar o pelo do meu husky no verão?", "hyg_06"),
    ("De quanto em quanto tempo vermifugar?", "hyg_07"),
    ("Qual a melhor idade para castrar minha cadela?", "rep_01"),
    ("Minha cadela está no cio, o que fazer?", "rep_02"),
    ("Cadela não castrada com secreção com pus e apática", "rep_03"),
    ("Minha gata está grávida, quando nascem os filhotes?", "rep_04"),
    ("Encontrei filhotes órfãos, posso dar leite de vaca?", "rep_05"),
    ("Posso viajar de carro com meu cachorro?", "life_01"),
    ("Quais documentos para viajar de avião com pet?", "life_02"),
    ("Abandonar animal é crime?", "life_03"),
    ("Quais os custos de ter um cachorro?", "life_04"),
    ("Vou adotar meu primeiro gato, o que preciso?", "life_05"),
    ("Meu filho pequeno pode brincar com o cachorro?", "life_06"),
    ("O que colocar no kit de primeiros socorros do pet?", "life_07"),
    ("Filhote com vômito e diarreia com sangue e muito fraco", "inf_01"),
    ("Como saber se meu gato tem FIV ou FeLV?", "inf_02"),
    ("Meu cachorro parece engasgado mas está tossindo muito", "inf_03"),
    ("Como prevenir a leishmaniose no meu cachorro?", "inf_04"),
    ("Fezes com muco e diarreia de giárdia, como limpar a casa?", "inf_05"),
    ("Meu cão comeu bolo de cacau", "tox_02"),
    ("Quais frutas meu cachorro pode comer?", "faq_01"),
    ("Qual a tabela de preços do transplante de córnea e parcelamento na clínica?", None),
    ("qual a capital da França", None),
]


def main() -> int:
    ids = [c["id"] for c in BASE_CHUNKS_RAG]
    assert len(ids) == len(set(ids)), "IDs de chunk duplicados"
    obrigatorios = {"id", "source", "category", "title", "content", "keywords"}
    assert all(obrigatorios <= c.keys() for c in BASE_CHUNKS_RAG), "Chunk sem campo obrigatório"

    falhas = 0
    for pergunta, esperado in CASOS:
        topo = [c["id"] for c in KnowledgeService.buscar_chunks_rag(pergunta, top_k=3)["chunks"]]
        ok = (not topo) if esperado is None else esperado in topo[:2]
        falhas += not ok
        print(f"{'OK' if ok else 'XX'} {pergunta[:55]:<55} -> {topo} (esperado: {esperado})")

    categorias = sorted({c["category"] for c in BASE_CHUNKS_RAG})
    print(f"\n{len(ids)} chunks | {len(categorias)} categorias: {', '.join(categorias)}")
    print(f"{len(CASOS) - falhas}/{len(CASOS)} casos aprovados")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
