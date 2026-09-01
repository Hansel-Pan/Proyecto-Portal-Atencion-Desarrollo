import { useEffect, useRef, useState } from 'react'
import { api } from '../api/client'
import { BadgeEstado } from '../components/badges'

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-marca-500 focus:outline-none focus:ring-2 focus:ring-marca-100'

export default function ChatPage() {
  const [cliente, setCliente] = useState({
    nombre: localStorage.getItem('chat_nombre') ?? '',
    email: localStorage.getItem('chat_email') ?? '',
  })
  const [iniciado, setIniciado] = useState(false)
  const [ticketRef, setTicketRef] = useState(null)
  const [estado, setEstado] = useState(null)
  const [mensajes, setMensajes] = useState([])
  const [texto, setTexto] = useState('')
  const [ocupado, setOcupado] = useState(false)
  const [error, setError] = useState(null)
  const finRef = useRef(null)

  useEffect(() => {
    finRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes])

  function iniciar(e) {
    e.preventDefault()
    localStorage.setItem('chat_nombre', cliente.nombre)
    localStorage.setItem('chat_email', cliente.email)
    setIniciado(true)
  }

  function agregarDeInteracciones(interacciones) {
    setMensajes((m) => [
      ...m,
      ...interacciones.map((i) => ({ autor: i.autor, texto: i.mensaje })),
    ])
  }

  async function enviar(e) {
    e.preventDefault()
    const mensaje = texto.trim()
    if (!mensaje || ocupado) return
    setTexto('')
    setOcupado(true)
    setError(null)
    try {
      if (!ticketRef) {
        const ticket = await api.crearTicket({
          cliente: { nombre: cliente.nombre, email: cliente.email },
          tipo: 'consulta',
          asunto: mensaje.slice(0, 80),
          descripcion: mensaje,
        })
        setTicketRef(ticket.codigo)
        setEstado(ticket.estado)
        agregarDeInteracciones(ticket.interacciones)
      } else {
        const ticket = await api.enviarMensaje(ticketRef, mensaje)
        setEstado(ticket.estado)
        agregarDeInteracciones(ticket.interacciones.slice(-2))
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setOcupado(false)
    }
  }

  if (!iniciado) {
    return (
      <div className="mx-auto max-w-md">
        <h1 className="text-2xl font-bold">Chat con el asistente IA</h1>
        <p className="mt-1 text-sm text-slate-500">Disponible 24/7. Para identificar su conversación, cuéntenos:</p>
        <form onSubmit={iniciar} className="mt-5 space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Nombre *</span>
            <input required minLength={2} value={cliente.nombre} onChange={(e) => setCliente((c) => ({ ...c, nombre: e.target.value }))} className={inputCls} />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium">Email *</span>
            <input required type="email" value={cliente.email} onChange={(e) => setCliente((c) => ({ ...c, email: e.target.value }))} className={inputCls} />
          </label>
          <button className="w-full rounded-lg bg-marca-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-marca-700">
            Comenzar chat
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="mx-auto flex h-[calc(100vh-11rem)] max-w-3xl flex-col">
      <div className="flex items-center justify-between pb-3">
        <h1 className="text-xl font-bold">Chat con el asistente IA</h1>
        {ticketRef && (
          <span className="flex items-center gap-2 text-xs text-slate-500">
            {ticketRef} <BadgeEstado estado={estado} />
          </span>
        )}
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto rounded-xl border border-slate-200 bg-slate-100 p-4">
        {mensajes.length === 0 && (
          <p className="mt-8 text-center text-sm text-slate-400">
            Escriba su consulta; el asistente la analizará de inmediato.
          </p>
        )}
        {mensajes.map((m, idx) => (
          <div
            key={idx}
            className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-2 text-sm shadow-sm ${
              m.autor === 'cliente' ? 'ml-auto bg-marca-500 text-white' : 'mr-auto bg-white'
            }`}
          >
            {m.texto}
          </div>
        ))}
        {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        <div ref={finRef} />
      </div>

      <form onSubmit={enviar} className="mt-3 flex gap-2">
        <input
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Escriba su mensaje…"
          className={`${inputCls} flex-1`}
        />
        <button
          disabled={ocupado || !texto.trim()}
          className="rounded-lg bg-marca-600 px-5 py-2 text-sm font-semibold text-white hover:bg-marca-700 disabled:opacity-50"
        >
          Enviar
        </button>
      </form>
    </div>
  )
}
