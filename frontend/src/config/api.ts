// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const API_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/login`,
  CADASTRO: `${API_BASE_URL}/usuario/cadastro`,
  PAGAMENTO: `${API_BASE_URL}/planos/pagamento`,
  RADAR: `${API_BASE_URL}/radar`,
  RADAR_RESULTADOS: `${API_BASE_URL}/radar/resultados`,
  RADAR_STATUS: `${API_BASE_URL}/radar/status`,
}

export default API_BASE_URL
