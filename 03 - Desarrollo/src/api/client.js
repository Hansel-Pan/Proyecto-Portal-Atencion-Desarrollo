const BASE =
  import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? 'http://localhost:8000' : '')

async function request(path, opciones = {}) {
  const resp = await fetch(`${BASE}${path}`, {
    method: opciones.method ?? 'GET',
    headers: { 'Content-Type': 'application/json' },
    body: opciones.body ? JSON.stringify(opciones.body) : undefined,
  })
  const datos = await resp.json().catch(() => null)
  if (!resp.ok) {
    throw new Error(typeof datos?.detail === 'string' ? datos.detail : `Error ${resp.status}`)
  }
  return datos
}

function query(params) {
  const limpios = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== '' && v != null),
  )
  return new URLSearchParams(limpios).toString()
}

export const api = {
  crearTicket: (datos) => request('/tickets', { method: 'POST', body: datos }),
  obtenerTicket: (ref) => request(`/tickets/${encodeURIComponent(ref)}`),
  enviarMensaje: (ref, mensaje) =>
    request(`/tickets/${encodeURIComponent(ref)}/mensajes`, { method: 'POST', body: { mensaje } }),
  listarTickets: (params) => request(`/admin/tickets?${query(params)}`),
  reporteMensual: (mes) => request(`/admin/reportes/mensual?mes=${mes}`),
  insightsMensuales: (mes, recalcular = false) =>
    request(`/admin/reportes/mensual/insights?mes=${mes}&recalcular=${recalcular}`),
  descargarExporte: async (formato, mes) => {
    const resp = await fetch(`${BASE}/admin/reportes/mensual/exportar/${formato}?mes=${mes}`)
    if (!resp.ok) throw new Error(`Error ${resp.status} al exportar`)
    return resp.blob()
  },
}
