import { NavLink } from 'react-router-dom'

const CLASE = ({ isActive }) =>
  `rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
    isActive ? 'bg-marca-600 text-white' : 'text-slate-300 hover:bg-white/10 hover:text-white'
  }`

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <header className="bg-marca-700">
        <nav className="mx-auto flex max-w-6xl flex-wrap items-center gap-2 px-4 py-3">
          <NavLink to="/" className="mr-4 text-lg font-bold text-white">
            Portal de Atención
          </NavLink>
          <NavLink to="/" end className={CLASE}>Nueva solicitud</NavLink>
          <NavLink to="/consulta" className={CLASE}>Consultar ticket</NavLink>
          <NavLink to="/chat" className={CLASE}>Chat</NavLink>
          <span className="mx-2 h-5 w-px bg-white/30" />
          <NavLink to="/admin" end className={CLASE}>Dashboard</NavLink>
          <NavLink to="/admin/tickets" className={CLASE}>Tickets</NavLink>
          <NavLink to="/admin/reportes" className={CLASE}>Reportes</NavLink>
        </nav>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  )
}
