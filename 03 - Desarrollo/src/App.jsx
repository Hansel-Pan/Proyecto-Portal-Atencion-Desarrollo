import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import AdminDashboardPage from './pages/AdminDashboardPage'
import AdminReportePage from './pages/AdminReportePage'
import AdminTicketsPage from './pages/AdminTicketsPage'
import ChatPage from './pages/ChatPage'
import ConsultaPage from './pages/ConsultaPage'
import InicioPage from './pages/InicioPage'
import MockupPage from './pages/MockupPage'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<InicioPage />} />
          <Route path="/consulta" element={<ConsultaPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/mockup" element={<MockupPage />} />
          <Route path="/admin" element={<AdminDashboardPage />} />
          <Route path="/admin/tickets" element={<AdminTicketsPage />} />
          <Route path="/admin/reportes" element={<AdminReportePage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
