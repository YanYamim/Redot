// Configuração da API
const rawEnv = import.meta.env.VITE_API_URL ?? ''
let API_BASE_URL = rawEnv ? rawEnv.replace(/\/$/, '') : ''

if (!API_BASE_URL) {
  if (typeof window === 'undefined') {
    API_BASE_URL = 'http://127.0.0.1:8000'
  }
}

// Prefix API calls with /api in the browser so the dev server can proxy
// them without colliding with client-side routes like /login.
const apiPrefix = API_BASE_URL ? `${API_BASE_URL}/api` : '/api'

export const API_ENDPOINTS = {
  LOGIN: `${apiPrefix}/login`,
  CADASTRO: `${apiPrefix}/usuario/cadastro`,
  PAGAMENTO: `${apiPrefix}/planos/pagamento`,
  RADAR: `${apiPrefix}/radar`,
  RADAR_RESULTADOS: `${apiPrefix}/radar/resultados`,
  RADAR_STATUS: `${apiPrefix}/radar/status`,
}

export default API_BASE_URL
