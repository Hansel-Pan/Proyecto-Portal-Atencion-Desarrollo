const ESTILOS_ESTADO = {
  abierto: 'bg-amber-100 text-amber-800',
  escalado: 'bg-orange-100 text-orange-800',
  resuelto_ia: 'bg-emerald-100 text-emerald-800',
  resuelto_manual: 'bg-green-100 text-green-800',
  cerrado: 'bg-slate-200 text-slate-600',
}

const ETIQUETAS_ESTADO = {
  abierto: 'Abierto',
  escalado: 'Escalado',
  resuelto_ia: 'Resuelto por IA',
  resuelto_manual: 'Resuelto manual',
  cerrado: 'Cerrado',
}

const ESTILOS_PRIORIDAD = {
  baja: 'bg-slate-100 text-slate-600',
  media: 'bg-blue-100 text-blue-700',
  alta: 'bg-orange-100 text-orange-700',
  critica: 'bg-red-100 text-red-700',
}

const ETIQUETAS_TIPO = { consulta: 'Consulta', solicitud: 'Solicitud', queja: 'Queja' }

export function BadgeEstado({ estado }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${ESTILOS_ESTADO[estado] ?? 'bg-slate-100 text-slate-600'}`}>
      {ETIQUETAS_ESTADO[estado] ?? estado}
    </span>
  )
}

export function BadgePrioridad({ prioridad }) {
  return (
    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${ESTILOS_PRIORIDAD[prioridad] ?? 'bg-slate-100 text-slate-600'}`}>
      {prioridad}
    </span>
  )
}

export function EtiquetaTipo({ tipo }) {
  return <span className="text-sm">{ETIQUETAS_TIPO[tipo] ?? tipo}</span>
}
