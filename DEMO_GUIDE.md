# 🚀 Guia de Demonstração - Santé Dashboard

## 🎯 Objetivo
Este guia demonstra como usar o sistema Santé com diferentes cidades e dados epidemiológicos.

## 📊 Dados de Exemplo Disponíveis

### 1. Recife, Brazil (Original)
- **Arquivo**: `sample_data.csv`
- **Características**: Dados de influenza com tendência crescente
- **R(t) Esperado**: Alto (acima de 1.0)
- **Cenário**: Surto epidêmico em desenvolvimento

### 2. New York, USA (Novo)
- **Arquivo**: `new_york_data.csv`
- **Características**: Dados de influenza com pico e declínio
- **R(t) Esperado**: Médio a baixo (tendência decrescente)
- **Cenário**: Surto controlado, casos em redução

### 3. Freetown, Sierra Leone (Novo)
- **Arquivo**: `freetown_data.csv`
- **Características**: Dados de influenza com crescimento moderado
- **R(t) Esperado**: Médio (estável)
- **Cenário**: Transmissão controlada, vigilância ativa

## 🔄 Como Testar

### Passo 1: Acessar o Sistema
1. Acesse: `http://localhost:5000`
2. Login: `admin` / `admin`

### Passo 2: Upload de Dados
1. Vá em **"Upload CSV"**
2. Escolha um dos arquivos de exemplo
3. Clique em **"Upload and Process"**

### Passo 3: Visualizar Dashboard
1. Você será redirecionado ao dashboard da cidade
2. Observe as diferenças nos indicadores:
   - **R(t)**: Taxa de transmissão
   - **R0**: Número básico de reprodução
   - **Taxa de Internação**: Percentual de casos graves

### Passo 4: Explorar o Mapa
1. **Zoom**: Use scroll do mouse para zoom
2. **Pan**: Clique e arraste para mover o mapa
3. **Marcadores**: Clique nos círculos para ver detalhes
4. **Cores**: Observe as mudanças de cor baseadas no risco

## 🎨 Diferenças Visuais

### Recife (Alto Risco)
- 🔴 **Cor**: Vermelho (R(t) > 1.2)
- 📈 **Tendência**: Crescente
- ⚠️ **Alerta**: RED ALERT
- 🗺️ **Mapa**: Zonas de risco intensas

### New York (Médio/Baixo Risco)
- 🟠 **Cor**: Laranja a Verde (R(t) < 1.0)
- 📉 **Tendência**: Decrescente
- ✅ **Alerta**: YELLOW ALERT
- 🗺️ **Mapa**: Zonas de risco moderadas

### Freetown (Médio Risco)
- 🟠 **Cor**: Laranja (R(t) ≈ 1.0)
- ➡️ **Tendência**: Estável
- ⚠️ **Alerta**: YELLOW ALERT
- 🗺️ **Mapa**: Zonas de risco equilibradas

## 🔍 Análise dos Dados

### Padrões Epidemiológicos
1. **Crescimento Exponencial**: Recife mostra surto ativo
2. **Controle de Transmissão**: New York demonstra sucesso nas medidas
3. **Estabilidade**: Freetown mantém transmissão controlada

### Indicadores-Chave
- **R(t) > 1.0**: Epidemia em crescimento
- **R(t) = 1.0**: Epidemia estável
- **R(t) < 1.0**: Epidemia em declínio

## 💡 Casos de Uso

### Para Gestores de Saúde
- **Monitoramento**: Acompanhar tendências em tempo real
- **Alertas**: Receber notificações de risco
- **Decisões**: Base para implementar medidas de controle

### Para Pesquisadores
- **Análise**: Dados estruturados para estudos
- **Modelagem**: Base para previsões epidemiológicas
- **Comparação**: Análise entre diferentes regiões

### Para Educadores
- **Demonstração**: Sistema prático de vigilância
- **Treinamento**: Capacitação em análise de dados
- **Simulação**: Cenários epidemiológicos diversos

## 🚀 Próximos Passos

1. **Teste Todas as Cidades**: Faça upload de cada arquivo CSV
2. **Compare Dashboards**: Observe as diferenças nos indicadores
3. **Explore o Mapa**: Teste a funcionalidade de navegação
4. **Analise XAI**: Entenda os fatores que influenciam as previsões

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique se o ambiente virtual está ativado
- Confirme se todas as dependências estão instaladas
- Use `python test_simple.py` para verificar a estrutura
