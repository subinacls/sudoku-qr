
import useSWR from 'swr'
import axios from 'axios'
import { backendURL } from '../config'

const fetcher = (url: string) => axios.get(url).then(r => r.data)

export default function Leaderboard() {
  const { data, error } = useSWR(`${backendURL}/leaderboard/`, fetcher)
  if (error) return <div>Error loading leaderboard</div>
  if (!data) return <div>Loading...</div>
  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Leaderboard</h1>
      <table className="table-auto border">
        <thead><tr><th className="border px-2">Rank</th><th className="border px-2">User</th><th className="border px-2">Best Score</th></tr></thead>
        <tbody>
          {data.map((row: {email:string, best_score:number}, idx: number)=>(
            <tr key={idx}>
              <td className="border px-2">{idx+1}</td>
              <td className="border px-2">{row.email}</td>
              <td className="border px-2">{row.best_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
