from services.messages import MENSAGENS


def test_todas_as_trilhas_tem_tres_mensagens():
    for trilha, mensagens in MENSAGENS.items():
        assert len(mensagens) == 3, f"A trilha {trilha} não possui 3 mensagens"


def test_mensagens_possuem_nome_personalizavel():
    for trilha, mensagens in MENSAGENS.items():
        for mensagem in mensagens:
            assert "{nome}" in mensagem, (
                f"Mensagem da trilha {trilha} não possui o campo {{nome}}"
            )