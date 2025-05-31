
import { useState } from 'react'
import axios from 'axios'
import { backendURL } from '../config'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const nav = useNavigate()

  const handleRegister = async () => {
    await axios.post(`${backendURL}/auth/register`, { email, password })
    nav('/login')
  }

  return (
    <div className="flex flex-col items-center mt-20">
      <h1 className="text-2xl mb-4">Register</h1>
      <input className="border p-2 mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input type="password" className="border p-2 mb-2" placeholder="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={handleRegister}>Register</button>
    </div>
  )
}
