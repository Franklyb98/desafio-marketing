# Sistema de Segmentação e Campanhas de Marketing

Sistema desenvolvido em Python para automatizar a extração, organização e segmentação de clientes, permitindo o gerenciamento de campanhas de marketing e a simulação de envios de mensagens via WhatsApp.

O projeto foi desenvolvido como desafio prático, utilizando a API DummyJSON para obtenção de dados, SQLite para armazenamento e Flask para disponibilizar uma interface web de gerenciamento.

## Funcionalidades

- **Extração de dados:** consumo da API DummyJSON para obtenção de clientes e carrinhos de compras.
- **Armazenamento de dados brutos:** salvamento dos dados extraídos em arquivos JSON, organizados por data e horário.
- **Banco de dados:** consolidação e armazenamento das informações em SQLite.
- **Segmentação automática:** classificação de clientes conforme critérios comerciais.
- **Revisão de segmentação:** possibilidade de visualizar, confirmar e ajustar as trilhas sugeridas.
- **Gerenciamento de campanhas:** organização de mensagens e agendamentos por trilha.
- **Simulação de envios:** integração simulada com a API da Botmaker, sem realizar envios reais.
- **Histórico:** registro das simulações realizadas e dos respectivos detalhes das requisições.
- **Testes automatizados:** validação das principais funcionalidades do sistema.

## Regras de segmentação

Um cliente pode pertencer a mais de uma trilha, conforme suas características e comportamento de compra.

As classificações seguem a seguinte prioridade:

| Prioridade | Trilha | Critério |
|---|---|---|
| 1 | Alto valor | Valor total do carrinho maior ou igual a R$ 10.000 |
| 2 | Compra em quantidade | Quantidade total de itens maior ou igual a 15 |
| 3 | Incentivo | Valor total do carrinho inferior a R$ 1.000 |
| 4 | Público jovem | Idade inferior a 30 anos |
| 5 | Geral | Clientes que não atendem aos critérios anteriores |

As trilhas são independentes: um mesmo cliente pode atender aos critérios de diferentes segmentos.

## Tecnologias utilizadas

- **Python** – linguagem principal.
- **Flask** – desenvolvimento da aplicação web.
- **SQLite** – armazenamento e gerenciamento dos dados.
- **Requests** – consumo da API DummyJSON.
- **Python-dotenv** – gerenciamento de variáveis de ambiente.
- **Pytest** – testes automatizados.
- **HTML5 e CSS3** – estrutura e estilização da interface.
- **Git e GitHub** – versionamento e gerenciamento do código.

## Estrutura do projeto

```text
desafio-marketing/
│
├── database/
│   ├── database.py
│   ├── decisions.py
│   └── history.py
│
├── data/
│   └── raw/
│
├── services/
│   ├── classification.py
│   ├── messages.py
│   ├── scheduler.py
│   └── whatsapp.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── 404.html
│   ├── 500.html
│   ├── agendamentos.html
│   ├── clientes.html
│   ├── detalhes.html
│   └── historico.html
│
├── test/
│   ├── test_classification.py
│   ├── test_messages.py
│   ├── test_scheduler.py
│   └── test_whatsapp.py
│
├── app.py
├── extraction.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

## Instalação e configuração

### 1. Clone o repositório

```bash
git clone https://github.com/Franklyb98/desafio-marketing.git
```

Entre na pasta do projeto:

```bash
cd desafio-marketing
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

Para instalar as dependências do projeto e de desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

Abra o arquivo `.env` e configure as variáveis:

```env
BOTMAKER_ACCESS_TOKEN=seu_token_aqui
BOTMAKER_CHANNEL_ID=seu_channel_id_aqui
BOTMAKER_INTENT_NAME=seu_intent_aqui
FLASK_SECRET_KEY=coloque_sua_chave_secreta_aqui
DIA_ENVIO=0
```

As variáveis da Botmaker são utilizadas na configuração da simulação. Não é necessário inserir credenciais reais para executar o fluxo simulado.

**Importante:** o arquivo `.env` contém configurações locais e não deve ser enviado ao GitHub. Utilize o `.env.example` como modelo.

## Execução do projeto

Execute os comandos abaixo na ordem indicada, a partir da pasta raiz do projeto.

### 1. Extração dos dados

```bash
python extraction.py
```

Realiza a consulta à API DummyJSON e salva os dados brutos em arquivos JSON.

### 2. Consolidação no banco de dados

```bash
python -m database.database
```

Processa os arquivos extraídos, consolida as informações dos clientes e armazena os resultados no SQLite.

### 3. Classificação dos clientes

```bash
python -m services.classification
```

Aplica as regras de segmentação e salva as trilhas sugeridas para cada cliente.

### 4. Inicialização da aplicação web

```bash
python app.py
```

Após iniciar a aplicação, acesse:

http://127.0.0.1:5000

## Testes automatizados

O projeto utiliza Pytest para validar as funcionalidades implementadas.

Para executar os testes:

```bash
python -m pytest -v
```

Os testes contemplam:

- Regras de classificação dos clientes.
- Geração de mensagens.
- Lógica de agendamento.
- Formatação e validação de telefones.
- Simulação de integração com WhatsApp.

**Resultado da última execução:** 14 testes aprovados.

## Integração com WhatsApp

O projeto contempla uma integração simulada com a API da Botmaker.

O sistema permite simular o envio de mensagens, registrar os detalhes das requisições e acompanhar o histórico das operações.

**Atenção:** não são realizadas transmissões reais de mensagens pelo WhatsApp. A integração foi implementada para demonstrar o fluxo de comunicação e o registro das operações.

## Segurança e boas práticas

- Uso de variáveis de ambiente para configurações sensíveis.
- Arquivo `.env` protegido pelo `.gitignore`.
- Separação entre lógica de negócio, acesso ao banco de dados e interface web.
- Tratamento de erros durante a extração e processamento dos dados.
- Organização dos arquivos por responsabilidade.
- Testes automatizados para validação das funcionalidades.

## Autor

**Marcus Vinicius Aparecido Ferreira dos Santos**

- GitHub: [Franklyb98](https://github.com/Franklyb98)
- LinkedIn: [Vinicius Ferreira](https://www.linkedin.com/in/viniciusferreira55/)