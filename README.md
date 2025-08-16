# Santé – Flask MVC (Login, Upload CSV, Dashboard)

Este projeto é um MVP em Flask seguindo o padrão MVC:
- Autenticação com Flask-Login (usuário: `admin`, senha: `admin`)
- CRUD mínimo: criação/atualização de uma *Cidade* via upload de CSV
- Dashboard inspirado no protótipo fornecido (gráfico histórico + previsão ilustrativa)
- **NEW**: Mapa de risco interativo com OpenStreetMap e heatmap
- **NEW**: Interface completamente em inglês

## Como rodar

```bash
# 1. Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente (opcional)
cp env_example .env
# Edite o arquivo .env se necessário

# 4. Inicializar banco de dados
export FLASK_APP=main.py  # no Windows: set FLASK_APP=main.py
flask init-db

# 5. Executar aplicação
python main.py
# ou
flask run
```

A aplicação estará disponível em http://localhost:5000

## Estrutura do Projeto

```
sante_flask_mvc/
├── main.py              # Ponto de entrada principal da aplicação
├── app.py               # Configuração da aplicação Flask (legado)
├── wsgi.py              # Ponto de entrada WSGI alternativo
├── run.py               # Ponto de entrada alternativo
├── config.py            # Configurações da aplicação
├── models.py            # Modelos de dados (SQLAlchemy)
├── controllers/         # Controladores (Blueprints)
│   ├── auth.py         # Autenticação
│   ├── cities.py       # Gerenciamento de cidades
│   └── dashboard.py    # Dashboard de monitoramento
├── services/            # Serviços de negócio
│   ├── analytics.py    # Cálculos de indicadores
│   └── csv_loader.py   # Processamento de CSV
├── templates/           # Templates HTML
├── static/              # Arquivos estáticos
├── env_example          # Exemplo de configurações de ambiente
└── requirements.txt     # Dependências Python
```

## CSV esperado
Colunas obrigatórias: `city,state,country,week_label,cases`

### Arquivos de Exemplo Disponíveis:
- **`sample_data.csv`** - Recife, Brazil (dados de exemplo originais)
- **`new_york_data.csv`** - New York, USA (dados de exemplo)
- **`freetown_data.csv`** - Freetown, Sierra Leone (dados de exemplo)

Veja a seção "Sample CSV Files" na página de upload para baixar os exemplos.

## Funcionalidades

- **Login/Logout**: Sistema de autenticação simples
- **Upload CSV**: Processamento automático de dados epidemiológicos
- **Dashboard**: Visualização de casos históricos e previsões
- **Indicadores**: R(t), R0, taxa de internação
- **Sistema de Alertas**: Baseado no R(t) para tomada de decisão
- **XAI**: Explicabilidade dos fatores que influenciam as previsões
- **🌍 Mapa Interativo**: Mapa de risco com OpenStreetMap e heatmap
- **🌐 Interface em Inglês**: Interface completamente traduzida

## Novas Funcionalidades Implementadas

### 🗺️ Mapa de Risco Interativo
- **OpenStreetMap**: Mapa base gratuito e de alta qualidade
- **Heatmap**: Visualização de risco baseada no R(t) com cores dinâmicas
- **Zonas de Risco**: Múltiplas áreas com diferentes intensidades de risco
- **Popups Informativos**: Clique nos marcadores para ver detalhes da cidade
- **Legenda Visual**: Cores codificadas para níveis de risco (Alto/Meio/Baixo)

### 🌐 Interface em Inglês
- **Login**: Página de login moderna e responsiva
- **Upload**: Interface intuitiva para upload de CSV
- **Dashboard**: Todos os elementos traduzidos para inglês
- **Navegação**: Menu e navegação em inglês
- **Mensagens**: Flash messages e feedback em inglês

## Problemas Resolvidos

- ✅ **Erro de importação**: Corrigido imports relativos para absolutos
- ✅ **Estrutura MVC**: Ajustada para funcionar corretamente
- ✅ **Dashboard**: Atualizado para seguir exatamente o padrão visual do arquivo conceitual
- ✅ **Execução**: Múltiplos pontos de entrada criados (main.py, wsgi.py, run.py)
- ✅ **Imports**: Todos os imports agora são absolutos e funcionam corretamente
- ✅ **Mapa**: Implementado mapa real com OpenStreetMap e heatmap
- ✅ **Tradução**: Interface completamente em inglês

## Observações
- Forecast e indicadores são aproximações ilustrativas (MVP).
- O mapa de risco usa OpenStreetMap (gratuito) e pode ser expandido com mais cidades.
- Ajuste a validação e o pipeline de dados conforme a necessidade de produção.
- O dashboard segue exatamente o padrão visual do arquivo conceitual fornecido.
- **Login**: admin / admin

## Solução de Problemas

Se encontrar problemas de importação:
1. Use `python main.py` diretamente
2. Verifique se todas as dependências estão instaladas: `pip install -r requirements.txt`
3. Certifique-se de que o ambiente virtual está ativado

## Tecnologias Utilizadas

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Tailwind CSS, Chart.js, Leaflet.js
- **Mapas**: OpenStreetMap (gratuito e de alta qualidade)
- **Visualização**: Heatmaps, gráficos interativos, tooltips
- **Idioma**: Interface completamente em inglês
