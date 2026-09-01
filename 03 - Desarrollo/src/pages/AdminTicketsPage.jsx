import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { BadgeEstado, BadgePrioridad, EtiquetaTipo } from '../components/badges'

const fecha = (f) => new Date(f).toLocaleDateString('es', { day: '2-digit', month: '2-digit', year: 'numeric' })

const inputCls = 'rounded-lg border border-slate-300 px-2.5 py-1.5 text-sm'

const VACIO = { tipo: '', estado: '', prioridad: '', fecha_desde: '', fecha_hasta: '' }

export default function AdminTicketsPage() {
  const [filtros, setFiltros] = useState(VACIO)
  const [pagina, setPagina] = useState(1)
  const [datos, setDatos] = useState({ total: 0, items: [] })
  const [claveCargada, setClaveCargada] = useState(null)
  const [error, setError] = useState(null)

  const clave = JSON.stringify({ ...filtros, pagina })
  const cargando = clave !== claveCargada

  useEffect(() => {
    let vigente = true
    api
      .listarTickets({ ...filtros, pagina, tamanio_pagina: 15 })
      .then((r) => {
        if (!vigente) return
        setDatos(r)
        setError(null)
        setClaveCargada(clave)
      })
      .catch((err) => {
        if (!vigente) return
        setError(err.message)
        setClaveCargada(clave)
      })
    return () => {
      vigente = false
    }
  }, [clave, filtros, pagina])

  function cambiarFiltro(campo) {
    return (e) => {
      setPagina(1)
      setFiltros((f) => ({ ...f, [campo]: e.target.value }))
    }
  }

  const paginasTotales = Math.max(1, Math.ceil(datos.total / 15))

  return (
    <div>
      <h1 className="text-2xl font-bold">Tickets</h1>

      <div className="mt-4 flex flex-wrap items-center gap-2 rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
        <select value={filtros.tipo} onChange={cambiarFiltro('tipo')} className={inputCls}>
          <option value="">Todos los tipos</option>
          <option value="consulta">Consulta</option>
          <option value="solicitud">Solicitud</option>
          <option value="queja">Queja</option>
        </select>
        <select value={filtros.estado} onChange={cambiarFiltro('estado')} className={inputCls}>
          <option value="">Todos los estados</option>
          <option value="abierto">Abierto</option>
          <option value="escalado">Escalado</option>
          <option value="resuelto_ia">Resuelto IA</option>
          <option value="resuelto_manual">Resuelto manual</option>
          <option value="cerrado">Cerrado</option>
        </select>
        <select value={filtros.prioridad} onChange={cambiarFiltro('prioridad')} className={inputCls}>
          <option value="">Toda prioridad</option>
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
          <option value="critica">Crítica</option>
        </select>
        <input type="date" value={filtros.fecha_desde} onChange={cambiarFiltro('fecha_desde')} className={inputCls} />
        <span className="text-sm text-slate-400">→</span>
        <input type="date" value={filtros.fecha_hasta} onChange={cambiarFiltro('fecha_hasta')} className={inputCls} />
        <button onClick={() => { setFiltros(VACIO); setPagina(1) }} className="ml-auto text-sm font-medium text-marca-600 hover:underline">
          Limpiar filtros
        </button>
      </div>

      {error && <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      <div className="mt-4 overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Código</th>
              <th className="px-4 py-3">Cliente</th>
              <th className="px-4 py-3">Fecha</th>
              <th className="px-4 py-3">Tipo</th>
              <th className="px-4 py-3">Estado</th>
              <th className="px-4 py-3">Prioridad</th>
              <th className="px-4 py-3">IA</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {cargando && (
              <tr><td colSpan={7} className="px-4 py-8 text-center text-slate-400">Cargando…</td></tr>
            )}
            {!cargando && datos.items.length === 0 && (
              <tr><td colSpan={7} className="px-4 py-8 text-center text-slate-400">No hay tickets con esos filtros.</td></tr>
            )}
            {!cargando &&
              datos.items.map((t) => (
                <tr key={t.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-mono text-xs font-semibold text-marca-600">{t.codigo}</td>
                  <td className="px-4 py-3">
                    {t.cliente.nombre}
                    <span className="block text-xs text-slate-400">{t.cliente.email}</span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">{fecha(t.fecha_creacion)}</td>
                  <td className="px-4 py-3"><EtiquetaTipo tipo={t.tipo} /></td>
                  <td className="px-4 py-3"><BadgeEstado estado={t.estado} /></td>
                  <td className="px-4 py-3"><BadgePrioridad prioridad={t.prioridad} /></td>
                  <td className="px-4 py-3">{t.resuelto_por_ia ? 'Sí' : '—'}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-between text-sm">
        <span className="text-slate-500">{datos.total} ticket(s) en total</span>
        <div className="flex items-center gap-2">
          <button
            disabled={pagina <= 1}
            onClick={() => setPagina((p) => p - 1)}
            className="rounded-lg border border-slate-300 px-3 py-1.5 font-medium disabled:opacity-40"
          >
            Anterior
          </button>
          <span>Página {pagina} de {paginasTotales}</span>
          <button
            disabled={pagina >= paginasTotales}
            onClick={() => setPagina((p) => p + 1)}
            className="rounded-lg border border-slate-300 px-3 py-1.5 font-medium disabled:opacity-40"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  )
}
