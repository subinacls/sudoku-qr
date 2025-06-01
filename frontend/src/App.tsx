
import { Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Leaderboard from './pages/Leaderboard'
import Verify from './pages/Verify'
import SubmitPhotoWithCrop from './pages/SubmitPhotoWithCrop'


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/leaderboard" element={<Leaderboard />} />
      <Route path="/verify/:qrToken" element={<Verify />} />
      <Route path="/submit-photo/:qrToken" element={<SubmitPhotoWithCrop />} />
    </Routes>
  )
}
