# 🗺️ Mapa de Risco - Funcionalidades Implementadas

## Visão Geral
O mapa de risco foi implementado usando **OpenStreetMap** (gratuito) e **Leaflet.js** para criar uma visualização interativa e profissional do risco epidemiológico por cidade.

## 🎯 Funcionalidades Principais

### 1. Mapa Base
- **OpenStreetMap**: Mapa base de alta qualidade e gratuito
- **Zoom e Pan**: Navegação completa do mapa
- **Responsivo**: Adapta-se a diferentes tamanhos de tela

### 2. Visualização de Risco
- **Cores Dinâmicas**: Baseadas no valor do R(t)
  - 🔴 **Vermelho**: R(t) > 1.2 (Alto Risco)
  - 🟠 **Laranja**: 1.0 < R(t) ≤ 1.2 (Médio Risco)
  - 🟢 **Verde**: R(t) ≤ 1.0 (Baixo Risco)

### 3. Elementos do Mapa
- **Marcador Principal**: Círculo colorido representando a cidade
- **Heatmap**: Zona de risco ao redor da cidade com intensidade baseada no R(t)
- **Zonas de Risco**: Múltiplas áreas com diferentes intensidades
- **Popups Informativos**: Clique para ver detalhes da cidade

### 4. Coordenadas das Cidades
```javascript
const cityCoordinates = {
  'Recife': [-8.0476, -34.8770],
  'São Paulo': [-23.5505, -46.6333],
  'Rio de Janeiro': [-22.9068, -43.1729],
  'New York': [40.7128, -74.0060],
  'London': [51.5074, -0.1278],
  'Tokyo': [35.6762, 139.6503],
  'Freetown': [8.4844, -13.2284]
};
```

**Cidades Disponíveis para Teste:**
- 🌍 **Recife, Brazil** - Dados de exemplo originais
- 🗽 **New York, USA** - Dados de exemplo expandidos
- 🌍 **Freetown, Sierra Leone** - Dados de exemplo internacionais

## 🔧 Como Expandir

### Adicionar Novas Cidades
1. Adicione as coordenadas no objeto `cityCoordinates`
2. O mapa automaticamente detectará e posicionará a cidade

### Integrar com Geocoding
```javascript
// Exemplo com serviço de geocoding
async function getCityCoordinates(cityName) {
  const response = await fetch(`https://api.example.com/geocode?city=${cityName}`);
  const data = await response.json();
  return [data.lat, data.lng];
}
```

### Personalizar Zonas de Risco
```javascript
// Ajustar raio e intensidade do heatmap
const heatmapRadius = 2000; // 2km
const heatmapOpacity = 0.3; // 30% de opacidade
```

## 🎨 Personalização Visual

### Cores de Risco
- **Alto Risco**: `#ef4444` (vermelho)
- **Médio Risco**: `#f97316` (laranja)
- **Baixo Risco**: `#22c55e` (verde)

### Estilos CSS
```css
#risk-map {
  height: 400px;
  width: 100%;
  border-radius: 0.5rem;
  z-index: 1;
}
```

## 📱 Responsividade
- **Desktop**: Mapa em tamanho completo
- **Tablet**: Mapa adaptado para telas médias
- **Mobile**: Mapa otimizado para dispositivos móveis

## 🚀 Performance
- **Lazy Loading**: Tiles do mapa carregados sob demanda
- **Otimização**: Renderização eficiente com Leaflet.js
- **Cache**: Tiles do OpenStreetMap são cacheados automaticamente

## 🔗 Dependências
- **Leaflet.js**: Biblioteca de mapas interativos
- **OpenStreetMap**: Dados de mapa gratuitos
- **Tailwind CSS**: Estilização responsiva

## 💡 Próximos Passos
1. **Geocoding Automático**: Integrar com API de geocoding
2. **Múltiplas Cidades**: Mostrar várias cidades no mesmo mapa
3. **Dados em Tempo Real**: Atualizar risco em tempo real
4. **Camadas Adicionais**: Adicionar camadas de dados demográficos
