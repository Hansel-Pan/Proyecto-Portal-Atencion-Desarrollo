import { useEffect, useState } from 'react'
import { api } from '../api/client'

const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

function nombreMes(mes) {
  return `${MESES[Number(mes.slice(5)) - 1]} ${mes.slice(0, 4)}`
}

async function descargar(formato, mes) {
  const blob = await api.descargarExporte(formato, mes)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `reporte-${mes}.${formato}`
  a.click()
  URL.revokeObjectURL(url)
}

export default function AdminReportePage() {
  const [mes, setMes] = useState(() => new Date().toISOString().slice(0, 7))
  const [metricas, setMetricas] = useState(null)
  const [insight, setInsight] = useState(null)
  const [mesCargado, setMesCargado] = useState(null)
  const [recalculando, setRecalculando] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let vigente = true
    Promise.all([api.reporteMensual(mes), api.insightsMensuales(mes)])
      .then(([r, i]) => {
        if (!vigente) return
        setMetricas(r.metricas)
        setInsight(i)
        setError(null)
        setMesCargado(mes)
      })
      .catch((err) => {
        if (!vigente) return
        setError(err.message)
        setMesCargado(mes)
      })
    return () => {
      vigente = false
    }
  }, [mes])

  const cargando = mes !== mesCargado

  function recalcular() {
    setRecalculando(true)
    api
      .insightsMensuales(mes, true)
      .then(setInsight)
      .catch((err) => setError(err.message))
      .finally(() => setRecalculando(false))
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Reporte mensual</h1>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm">
            <span className="font-medium">Mes:</span>
            <input type="month" value={mes} onChange={(e) => setMes(e.target.value)} className="rounded-lg border border-slate-300 px-2 py-1.5" />
          </label>
          <button onClick={() => descargar('pdf', mes)} className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium hover:bg-slate-50">
            Exportar PDF
          </button>
          <button onClick={() => descargar('excel', mes)} className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium hover:bg-slate-50">
            Exportar Excel
          </button>
        </div>
      </div>

      {cargando && <p className="mt-8 text-sm text-slate-400">Cargando reporte…</p>}
      {error && <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {metricas && !cargando && (
        <div className="mt-6 space-y-6">
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {[
              { t: 'Total tickets', v: metricas.total_tickets },
              { t: 'Resueltos IA', v: metricas.resueltos_por_ia },
              { t: 'Pendientes', v: metricas.pendientes },
              { t: 'Satisfacción prom.', v: metricas.satisfaccion_promedio ?? '—' },
            ].map((c) => (
              <div key={c.t} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{c.t}</p>
                <p className="mt-1 text-2xl font-bold">{c.v}</p>
              </div>
            ))}
          </div>

          <div className="rounded-xl border border-marca-100 bg-gradient-to-br from-marca-50 to-white p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h2 className="text-lg font-bold">Resumen ejecutivo con IA · <span className="capitalize">{nombreMes(mes)}</span></h2>
              <button
                onClick={recalcular}
                disabled={recalculando}
                className="rounded-lg bg-marca-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-marca-700 disabled:opacity-50"
              >
                {recalculando ? 'Regenerando…' : 'Regenerar análisis'}
              </button>
            </div>
            {insight ? (
              <>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed text-slate-700">{insight.resumen}</p>

                {insight.hallazgos?.length > 0 && (
                  <div className="mt-5">
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-500">Hallazgos</h3>
                    <ul className="mt-2 space-y-2">
                      {insight.hallazgos.map((h, i) => (
                        <li key={i} className="rounded-lg bg-white p-3 shadow-sm">
                          <p className="text-sm font-semibold">{h.titulo}</p>
                          {h.detalle && <p className="mt-0.5 text-sm text-slate-600">{h.detalle}</p>}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {insight.recomendaciones?.length > 0 && (
                  <div className="mt-5">
                    <h3 className="text-sm font-bold uppercase tracking-wide text-slate-500">Recomendaciones</h3>
                    <ul className="mt-2 space-y-2">
                      {insight.recomendaciones.map((r, i) => (
                        <li key={i} className="rounded-lg border-l-4 border-emerald-400 bg-white p-3 shadow-sm">
                          <p className="text-sm font-semibold">{r.titulo}</p>
                          {r.detalle && <p className="mt-0.5 text-sm text-slate-600">{r.detalle}</p>}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <p className="mt-4 text-xs text-slate-400">
                  Modelo: {insight.modelo}
                  {insight.generado_en ? ` · Generado: ${new Date(insight.generado_en).toLocaleString('es')}` : ''}
                  {insight.desde_cache ? ' · servido desde caché' : ''}
                </p>
              </>
            ) : (
              <p className="mt-3 text-sm text-slate-400">Generando análisis…</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
