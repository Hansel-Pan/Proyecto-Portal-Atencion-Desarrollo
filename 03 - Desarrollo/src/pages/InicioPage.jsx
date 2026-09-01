import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import { BadgeEstado } from '../components/badges'

const TIPOS = [
  { valor: 'consulta', texto: 'Consulta' },
  { valor: 'solicitud', texto: 'Solicitud' },
  { valor: 'queja', texto: 'Queja' },
]

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-marca-500 focus:outline-none focus:ring-2 focus:ring-marca-100'

export default function InicioPage() {
  const [form, setForm] = useState({
    nombre: '',
    email: '',
    telefono: '',
    empresa: '',
    tipo: 'consulta',
    asunto: '',
    descripcion: '',
  })
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState(null)
  const [resultado, setResultado] = useState(null)

  const set = (campo) => (e) => setForm((f) => ({ ...f, [campo]: e.target.value }))

  async function enviar(e) {
    e.preventDefault()
    setEnviando(true)
    setError(null)
    try {
      const ticket = await api.crearTicket({
        cliente: {
          nombre: form.nombre,
          email: form.email,
          telefono: form.telefono || null,
          empresa: form.empresa || null,
        },
        tipo: form.tipo,
        asunto: form.asunto,
        descripcion: form.descripcion,
      })
      setResultado(ticket)
    } catch (err) {
      setError(err.message)
    } finally {
      setEnviando(false)
    }
  }

  if (resultado) {
    const respuestaIA = resultado.interacciones.find((i) => i.autor === 'ia')
    return (
      <div className="mx-auto max-w-2xl">
        <div className="rounded-xl border border-emerald-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-emerald-700">Solicitud registrada</h1>
            <BadgeEstado estado={resultado.estado} />
          </div>
          <p className="mt-4 text-sm text-slate-500">Guarde este código para hacer seguimiento:</p>
          <p className="mt-1 font-mono text-3xl font-bold tracking-wider text-marca-600">{resultado.codigo}</p>
          {respuestaIA && (
            <div className="mt-5 rounded-lg bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Respuesta del asistente IA</p>
              <p className="mt-1 whitespace-pre-wrap text-sm">{respuestaIA.mensaje}</p>
            </div>
          )}
          <div className="mt-6 flex gap-3">
            <Link to="/consulta" className="rounded-lg bg-marca-600 px-4 py-2 text-sm font-medium text-white hover:bg-marca-700">
              Consultar estado
            </Link>
            <button
              onClick={() => setResultado(null)}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50"
            >
              Crear otra solicitud
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="text-2xl font-bold">Crear nueva solicitud</h1>
      <p className="mt-1 text-sm text-slate-500">
        Atención 24/7: nuestro asistente con IA intentará resolver su consulta al instante.
      </p>

      <form onSubmit={enviar} className="mt-6 space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Nombre *</span>
            <input required minLength={2} value={form.nombre} onChange={set('nombre')} className={inputCls} />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Email *</span>
            <input required type="email" value={form.email} onChange={set('email')} className={inputCls} />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Teléfono</span>
            <input value={form.telefono} onChange={set('telefono')} className={inputCls} />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Empresa</span>
            <input value={form.empresa} onChange={set('empresa')} className={inputCls} />
          </label>
        </div>

        <fieldset>
          <span className="mb-1 block text-sm font-medium">Tipo *</span>
          <div className="flex gap-2">
            {TIPOS.map((t) => (
              <button
                type="button"
                key={t.valor}
                onClick={() => setForm((f) => ({ ...f, tipo: t.valor }))}
                className={`flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition-colors ${
                  form.tipo === t.valor
                    ? 'border-marca-600 bg-marca-50 text-marca-700'
                    : 'border-slate-300 hover:bg-slate-50'
                }`}
              >
                {t.texto}
              </button>
            ))}
          </div>
        </fieldset>

        <label className="block">
          <span className="mb-1 block text-sm font-medium">Asunto *</span>
          <input required minLength={5} maxLength={200} value={form.asunto} onChange={set('asunto')} className={inputCls} />
        </label>

        <label className="block">
          <span className="mb-1 block text-sm font-medium">Descripción *</span>
          <textarea
            required
            minLength={10}
            rows={5}
            value={form.descripcion}
            onChange={set('descripcion')}
            className={`${inputCls} resize-y`}
          />
        </label>

        {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

        <button
          disabled={enviando}
          className="w-full rounded-lg bg-marca-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-marca-700 disabled:opacity-50"
        >
          {enviando ? 'Enviando…' : 'Enviar solicitud'}
        </button>
      </form>
    </div>
  )
}
