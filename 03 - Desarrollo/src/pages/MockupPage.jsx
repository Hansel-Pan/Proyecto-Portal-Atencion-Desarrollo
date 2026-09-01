const inputCls =
  'w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-marca-500 focus:outline-none focus:ring-2 focus:ring-marca-100'

const stats = [
  { label: 'Total tickets', value: '1,284', tone: 'bg-marca-50 text-marca-700' },
  { label: 'Resueltos IA', value: '842', tone: 'bg-emerald-50 text-emerald-700' },
  { label: 'Escalados', value: '186', tone: 'bg-amber-50 text-amber-700' },
  { label: 'Tasa IA', value: '65.6%', tone: 'bg-violet-50 text-violet-700' },
]

const tickets = [
  { codigo: 'TCK-2026-000142', cliente: 'María López', tipo: 'Consulta', estado: 'Resuelto IA', prioridad: 'Media', ia: 'Sí' },
  { codigo: 'TCK-2026-000145', cliente: 'Carlos Ruiz', tipo: 'Queja', estado: 'Escalado', prioridad: 'Alta', ia: 'No' },
  { codigo: 'TCK-2026-000149', cliente: 'Ana García', tipo: 'Solicitud', estado: 'Abierto', prioridad: 'Baja', ia: 'Sí' },
  { codigo: 'TCK-2026-000152', cliente: 'José Mena', tipo: 'Consulta', estado: 'Resuelto manual', prioridad: 'Media', ia: 'No' },
]

const barras = [
  { label: 'Consultas', value: 74 },
  { label: 'Solicitudes', value: 52 },
  { label: 'Quejas', value: 31 },
]

const mensajes = [
  { autor: 'cliente', text: 'Hola, necesito saber el horario de atención de mi sucursal.' },
  { autor: 'ia', text: 'Puedes consultar horarios en el sitio web; también te ayudo con citas y seguimiento.' },
  { autor: 'cliente', text: '¿Y si quiero cambiar mi pedido con una factura vencida?' },
  { autor: 'ia', text: 'Te puedo indicar cómo revisar pendientes y cómo escalar tu caso si requiere atención humana.' },
]

export default function MockupPage() {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-marca-600">Mockup del portal</p>
            <h1 className="mt-1 text-3xl font-bold text-slate-800">Portal de Atención al Cliente</h1>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-sm font-medium text-emerald-700">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
            Sistema activo · 24/7
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="space-y-6">
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Crear nueva solicitud</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Atención 24/7: nuestro asistente con IA intentará resolver su consulta al instante.
                </p>
              </div>
              <span className="rounded-full bg-marca-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-marca-700">
                Nuevo ticket
              </span>
            </div>

            <form className="mt-6 space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <label className="block">
                  <span className="mb-1 block text-sm font-medium text-slate-700">Nombre *</span>
                  <input defaultValue="Juan Pérez" readOnly className={inputCls} />
                </label>
                <label className="block">
                  <span className="mb-1 block text-sm font-medium text-slate-700">Email *</span>
                  <input defaultValue="juan.perez@empresa.com" readOnly className={inputCls} />
                </label>
                <label className="block">
                  <span className="mb-1 block text-sm font-medium text-slate-700">Teléfono</span>
                  <input defaultValue="+52 55 1234 5678" readOnly className={inputCls} />
                </label>
                <label className="block">
                  <span className="mb-1 block text-sm font-medium text-slate-700">Empresa</span>
                  <input defaultValue="NovaTech" readOnly className={inputCls} />
                </label>
              </div>

              <div>
                <span className="mb-1 block text-sm font-medium text-slate-700">Tipo *</span>
                <div className="flex gap-2">
                  {['Consulta', 'Solicitud', 'Queja'].map((tipo, index) => (
                    <button
                      type="button"
                      key={tipo}
                      className={`flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition ${
                        index === 0
                          ? 'border-marca-600 bg-marca-50 text-marca-700'
                          : 'border-slate-300 bg-white text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {tipo}
                    </button>
                  ))}
                </div>
              </div>

              <label className="block">
                <span className="mb-1 block text-sm font-medium text-slate-700">Asunto *</span>
                <input defaultValue="Consulta sobre horarios y seguimiento de pedido" readOnly className={inputCls} />
              </label>

              <label className="block">
                <span className="mb-1 block text-sm font-medium text-slate-700">Descripción *</span>
                <textarea
                  rows={5}
                  readOnly
                  className={`${inputCls} resize-y`}
                  defaultValue="Necesito revisar el horario de atención para mi sucursal y me gustaría saber si es posible hacer seguimiento del pedido 2458."
                />
              </label>

              <button className="w-full rounded-lg bg-marca-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-marca-700">
                Enviar solicitud
              </button>
            </form>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between gap-3">
              <h2 className="text-xl font-bold text-slate-800">Chat con el asistente IA</h2>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-500">
                Ticket TCK-2026-000142
              </span>
            </div>

            <div className="space-y-3 rounded-xl border border-slate-200 bg-slate-100 p-4">
              {mensajes.map((m, index) => (
                <div
                  key={index}
                  className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm shadow-sm ${
                    m.autor === 'cliente'
                      ? 'ml-auto bg-marca-500 text-white'
                      : 'mr-auto bg-white text-slate-700'
                  }`}
                >
                  {m.text}
                </div>
              ))}
            </div>

            <div className="mt-4 flex gap-2">
              <input
                defaultValue="¿Puedo consultar el estado del pedido para hoy?"
                readOnly
                className={`${inputCls} flex-1`}
              />
              <button className="rounded-lg bg-marca-600 px-5 py-2 text-sm font-semibold text-white hover:bg-marca-700">
                Enviar
              </button>
            </div>
          </section>
        </div>

        <aside className="space-y-6">
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between gap-2">
              <h2 className="text-xl font-bold text-slate-800">Dashboard</h2>
              <label className="text-sm text-slate-500">
                Mes: <input type="month" defaultValue="2026-09" readOnly className="ml-2 rounded-lg border border-slate-300 px-2 py-1 text-sm" />
              </label>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {stats.map((stat) => (
                <div key={stat.label} className={`rounded-xl border border-slate-200 p-3 ${stat.tone}`}>
                  <p className="text-[11px] font-semibold uppercase tracking-wide opacity-75">{stat.label}</p>
                  <p className="mt-1 text-2xl font-bold">{stat.value}</p>
                </div>
              ))}
            </div>

            <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="mb-3 flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-700">Tickets por tipo</h3>
                <span className="text-xs text-slate-500">Mes actual</span>
              </div>

              <div className="space-y-3">
                {barras.map((bar) => (
                  <div key={bar.label}>
                    <div className="mb-1 flex items-center justify-between text-xs text-slate-600">
                      <span>{bar.label}</span>
                      <span>{bar.value}</span>
                    </div>
                    <div className="h-2.5 overflow-hidden rounded-full bg-slate-200">
                      <div
                        className="h-full rounded-full bg-marca-500"
                        style={{ width: `${(bar.value / 80) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-800">Tickets</h2>
              <button className="text-sm font-medium text-marca-600 hover:underline">Ver todos</button>
            </div>

            <div className="overflow-hidden rounded-xl border border-slate-200">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-3 py-2">Código</th>
                    <th className="px-3 py-2">Cliente</th>
                    <th className="px-3 py-2">Estado</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 bg-white">
                  {tickets.map((ticket) => (
                    <tr key={ticket.codigo} className="align-top">
                      <td className="px-3 py-2 font-mono text-[11px] font-semibold text-marca-600">{ticket.codigo}</td>
                      <td className="px-3 py-2">
                        <span className="font-medium text-slate-700">{ticket.cliente}</span>
                        <span className="mt-0.5 block text-[11px] text-slate-400">{ticket.tipo}</span>
                      </td>
                      <td className="px-3 py-2">
                        <span className="inline-flex rounded-full bg-emerald-50 px-2 py-1 text-[10px] font-semibold text-emerald-700">
                          {ticket.estado}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </aside>
      </div>
    </div>
  )
}
