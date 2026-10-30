# Sistema de Segmentação e Campanhas de Marketing

## Sobre o projeto

Aplicação desenvolvida em Python para automatizar a extração, organização e classificação de clientes com base em seus perfis de compra.

O sistema permite que um analista revise as classificações sugeridas, confirme as trilhas de comunicação e acompanhe o agendamento de mensagens semanais. Também possui uma funcionalidade de simulação de envios via WhatsApp.

## Funcionalidades

- Extração de clientes e carrinhos por meio da API DummyJSON.
- Armazenamento dos dados brutos em arquivos JSON, organizados por data e horário.
- Persistência e consolidação dos dados em banco SQLite.
- Classificação automática de clientes em cinco trilhas:
  - Alto valor;
  - Compra em quantidade;
  - Incentivo;
  - Público jovem;
  - Geral.
- Visualização dos clientes e dos motivos de classificação.
- Confirmação e ajuste manual das trilhas pelo analista.
- Agendamento de três mensagens semanais por trilha, respeitando a prioridade definida.
- Personalização das mensagens com o primeiro nome do cliente.
- Simulação de requisições para integração com WhatsApp via Botmaker.
- Registro do histórico de simulações e dos dados das requisições.
- Tratamento de páginas de erro 404 e 500.
- Interface web com painel de clientes, agendamentos e histórico.
- Testes automatizados com Pytest.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- Requests
- HTML5
- CSS3
- Jinja2
- Python-dotenv
- Pytest
- Git e GitHub

##