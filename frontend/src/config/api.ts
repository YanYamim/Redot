// Configuração da API
const rawEnv = import.meta.env.VITE_API_URL ?? ''
let API_BASE_URL = ''
if (rawEnv) {
  API_BASE_URL = rawEnv.replace(/\/api\/?$/, '').replace(/\/$/, '')
} else {
  API_BASE_URL = ''
}

if (!API_BASE_URL) {
  if (typeof window === 'undefined') {
    API_BASE_URL = 'http://127.0.0.1:8000'
  }
}

// If a build-time VITE_API_URL used http but the page is served over https,
// upgrade the scheme at runtime so the browser doesn't block mixed content.
if (typeof window !== 'undefined' && API_BASE_URL.startsWith('http:') && window.location.protocol === 'https:') {
  API_BASE_URL = API_BASE_URL.replace(/^http:/, 'https:')
}

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
