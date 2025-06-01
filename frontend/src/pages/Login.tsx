import { useState } from 'react'
import axios from 'axios'
import { backendURL } from '../config'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const nav = useNavigate()

  const handleLogin = async () => {
    try {
      const form = new FormData()
      form.append('username', email)
      form.append('password', password)
      const { data } = await axios.post(`${backendURL}/auth/token`, form)
      localStorage.setItem('token', data.access_token)
      nav('/leaderboard')
    } catch (err) {
      alert('Login failed. Check credentials or server.')
    }
  }

  return (
    <div className="flex flex-col items-center mt-20">
      <h1 className="text-2xl mb-4">Login</h1>
      <input
        className="border p-2 mb-2"
        placeholder="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        className="border p-2 mb-2"
        placeholder="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleLogin}
      >
        Login
      </button>

      {/* ✅ Register Link */}
      <p className="text-sm mt-4">
        Don’t have an account?{' '}
        <a href="/register" className="text-blue-600 underline">
          Register here
        </a>
      </p>
    </div>
  )
}
