
import { useParams } from 'react-router-dom'
import { backendURL } from '../config'

export default function Verify() {
  const { qrToken } = useParams()
  if (!qrToken) return <div className="p-4">Invalid token</div>
  const pdfUrl = `${backendURL}/pdf/token/${qrToken}`
  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Puzzle Verification</h1>
      <p className="mb-2">Token: {qrToken}</p>
      <a className="text-blue-600 underline" href={pdfUrl} target="_blank">Download printable PDF</a>
    </div>
  )
}
