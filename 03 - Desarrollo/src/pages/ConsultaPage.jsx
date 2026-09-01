import { useState } from 'react'
import { api } from '../api/client'
import { BadgeEstado, BadgePrioridad, EtiquetaTipo } from '../components/badges'
import Conversacion from '../components/Conversacion'

const fecha = (f) => new Date(f).toLocaleString('es')

export default function ConsultaPage() {
  const [ref, setRef] = useState('')
  const [ticket, setTicket] = useState(null)
  const [buscando, setBuscando] = useState(false)
  const [error, setError] = useState(null)

  async function buscar(e) {
    e.preventDefault()
    setBuscando(true)
    setError(null)
    setTicket(null)
    try {
      setTicket(await api.obtenerTicket(ref.trim()))
    } catch (err) {
      setError(err.message)
    } finally {
      setBuscando(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="text-2xl font-bold">Consultar estado de un ticket</h1>
      <p className="mt-1 text-sm text-slate-500">Ingrese el código (ej. TCK-2026-000001) o el número de ticket.</p>

      <form onSubmit={buscar} className="mt-5 flex gap-2">
        <input
          required
          value={ref}
          onChange={(e) => setRef(e.target.value)}
          placeholder="TCK-2026-000001"
          className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-marca-500 focus:outline-none focus:ring-2 focus:ring-marca-100"
        />
        <button
          disabled={buscando}
          className="rounded-lg bg-marca-600 px-5 py-2 text-sm font-semibold text-white hover:bg-marca-700 disabled:opacity-50"
        >
          {buscando ? 'Buscando…' : 'Buscar'}
        </button>
      </form>

      {error && <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {ticket && (
        <div className="mt-6 space-y-4">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="font-mono text-lg font-bold text-marca-600">{ticket.codigo}</p>
              <BadgeEstado estado={ticket.estado} />
            </div>
            <h2 className="mt-2 font-semibold">{ticket.asunto}</h2>
            <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-2 text-sm sm:grid-cols-3">
              <div><dt className="text-slate-400">Tipo</dt><dd><EtiquetaTipo tipo={ticket.tipo} /></dd></div>
              <div><dt className="text-slate-400">Prioridad</dt><dd><BadgePrioridad prioridad={ticket.prioridad} /></dd></div>
              <div><dt className="text-slate-400">Creado</dt><dd>{fecha(ticket.fecha_creacion)}</dd></div>
              {ticket.fecha_resolucion && (
                <div><dt className="text-slate-400">Resuelto</dt><dd>{fecha(ticket.fecha_resolucion)}</dd></div>
              )}
              {ticket.tiempo_atencion_seg != null && (
                <div><dt className="text-slate-400">Tiempo de atención</dt><dd>{ticket.tiempo_atencion_seg}s</dd></div>
              )}
            </dl>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-4 font-semibold">Conversación</h3>
            <Conversacion interacciones={ticket.interacciones} />
          </div>
        </div>
      )}
    </div>
  )
}
