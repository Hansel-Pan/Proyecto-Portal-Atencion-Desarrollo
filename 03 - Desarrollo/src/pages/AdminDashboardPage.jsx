import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { api } from '../api/client'

const COLORES = ['#3b6ef5', '#10b981', '#f59e0b', '#ef4444']

const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
const ETIQUETAS_TIPO = { consulta: 'Consultas', solicitud: 'Solicitudes', queja: 'Quejas' }
const ETIQUETAS_ESTADO = {
  abierto: 'Abiertos',
  escalado: 'Escalados',
  resuelto_ia: 'Resueltos IA',
  resuelto_manual: 'Resueltos manual',
  cerrado: 'Cerrados',
}
const ETIQUETAS_PRIORIDAD = { baja: 'Baja', media: 'Media', alta: 'Alta', critica: 'Crítica' }

function aDatos(diccionario, etiquetas) {
  return Object.entries(etiquetas ?? {}).map(([clave, etiqueta]) => ({
    nombre: etiqueta,
    cantidad: diccionario?.[clave] ?? 0,
  }))
}

export default function AdminDashboardPage() {
  const [mes, setMes] = useState(() => new Date().toISOString().slice(0, 7))
  const [metricas, setMetricas] = useState(null)
  const [mesCargado, setMesCargado] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let vigente = true
    api
      .reporteMensual(mes)
      .then((r) => {
        if (!vigente) return
        setMetricas(r.metricas)
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

  const tarjetas = metricas && [
    { titulo: 'Total tickets', valor: metricas.total_tickets },
    { titulo: 'Resueltos por IA', valor: metricas.resueltos_por_ia },
    { titulo: 'Escalados a manual', valor: metricas.escalados },
    { titulo: 'Pendientes', valor: metricas.pendientes },
    { titulo: 'Tasa resolución IA', valor: `${metricas.tasa_resolucion_ia_pct}%` },
    {
      titulo: 'Tiempo promedio',
      valor:
        metricas.tiempo_promedio_atencion_seg != null
          ? `${Math.round(metricas.tiempo_promedio_atencion_seg / 60)} min`
          : '—',
    },
  ]

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <label className="flex items-center gap-2 text-sm">
          <span className="font-medium">Mes:</span>
          <input
            type="month"
            value={mes}
            onChange={(e) => setMes(e.target.value)}
            className="rounded-lg border border-slate-300 px-2 py-1.5"
          />
        </label>
      </div>

      {cargando && <p className="mt-8 text-sm text-slate-400">Cargando métricas…</p>}
      {error && <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {metricas && !cargando && (
        <>
          {metricas.total_tickets === 0 ? (
            <p className="mt-8 rounded-xl border border-dashed border-slate-300 p-8 text-center text-sm text-slate-500">
              No hay tickets registrados en {MESES[Number(mes.slice(5)) - 1]} {mes.slice(0, 4)}.
            </p>
          ) : (
            <>
              <div className="mt-5 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
                {tarjetas.map((t) => (
                  <div key={t.titulo} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-400">{t.titulo}</p>
                    <p className="mt-1 text-2xl font-bold">{t.valor}</p>
                  </div>
                ))}
              </div>

              <div className="mt-6 grid gap-6 lg:grid-cols-3">
                <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                  <h2 className="mb-2 text-sm font-semibold">Tickets por tipo</h2>
                  <ResponsiveContainer width="100%" height={260}>
                    <PieChart>
                      <Pie data={aDatos(metricas.por_tipo, ETIQUETAS_TIPO)} dataKey="cantidad" nameKey="nombre" innerRadius={45} outerRadius={80} paddingAngle={3}>
                        {aDatos(metricas.por_tipo, ETIQUETAS_TIPO).map((_, i) => (
                          <Cell key={i} fill={COLORES[i % COLORES.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                  <h2 className="mb-2 text-sm font-semibold">Tickets por estado</h2>
                  <ResponsiveContainer width="100%" height={260}>
                    <BarChart data={aDatos(metricas.por_estado, ETIQUETAS_ESTADO)}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="nombre" tick={{ fontSize: 11 }} interval={0} angle={-20} textAnchor="end" height={50} />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="cantidad" fill="#3b6ef5" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                  <h2 className="mb-2 text-sm font-semibold">Tickets por prioridad</h2>
                  <ResponsiveContainer width="100%" height={260}>
                    <BarChart data={aDatos(metricas.por_prioridad, ETIQUETAS_PRIORIDAD)}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="nombre" tick={{ fontSize: 12 }} />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="cantidad" fill="#10b981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}
