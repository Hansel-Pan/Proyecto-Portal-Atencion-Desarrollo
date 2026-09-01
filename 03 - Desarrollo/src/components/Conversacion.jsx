const AUTOR_ESTILO = {
  cliente: 'ml-auto bg-marca-500 text-white',
  ia: 'mr-auto bg-white border border-slate-200',
  agente: 'mr-auto bg-emerald-50 border border-emerald-200',
}

const ETIQUETAS = { cliente: 'Tú', ia: 'Asistente IA', agente: 'Agente' }

function hora(fecha) {
  return new Date(fecha).toLocaleTimeString('es', { hour: '2-digit', minute: '2-digit' })
}

export default function Conversacion({ interacciones }) {
  if (!interacciones?.length) return <p className="text-sm text-slate-500">Sin mensajes.</p>
  return (
    <div className="flex flex-col gap-3">
      {interacciones.map((i) => (
        <div key={i.id} className={`max-w-[85%] rounded-2xl px-4 py-2.5 shadow-sm ${AUTOR_ESTILO[i.autor]}`}>
          <p className="whitespace-pre-wrap text-sm">{i.mensaje}</p>
          <p className={`mt-1 text-[11px] ${i.autor === 'cliente' ? 'text-marca-100' : 'text-slate-400'}`}>
            {ETIQUETAS[i.autor]} · {hora(i.fecha)}
            {i.modelo ? ` · ${i.modelo}` : ''}
            {i.confianza != null ? ` · confianza ${(i.confianza * 100).toFixed(0)}%` : ''}
          </p>
        </div>
      ))}
    </div>
  )
}
