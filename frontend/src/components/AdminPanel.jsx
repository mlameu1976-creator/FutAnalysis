import React, {useEffect, useState} from 'react'
import API from '../api'
import { authHeader, getToken } from '../auth'
export default function AdminPanel(){
  const [matches, setMatches] = useState([])
  const [file, setFile] = useState(null)
  async function load(){
    try{
      const r = await API.get('/admin/matches')
      setMatches(r.data)
    }catch(e){
      console.error(e)
    }
  }
  useEffect(()=>{ load() },[])
  async function del(id){
    try{
      await API.delete(`/admin/matches/${id}`)
      load()
    }catch(e){ console.error(e) }
  }
  async function uploadCsv(e){
    e.preventDefault()
    if(!file) return alert('Selecione um CSV')
    const fd = new FormData()
    fd.append('file', file)
    try{
      await API.post('/admin/import-csv', fd, { headers: {'Content-Type':'multipart/form-data'} })
      alert('Importado')
      setFile(null); load()
    }catch(e){ console.error(e); alert('Erro') }
  }
  return (
    <div>
      <h2 style={{fontSize:20,fontWeight:600}}>Admin</h2>
      <div style={{marginTop:12}} className="card">
        <form onSubmit={uploadCsv}>
          <div style={{marginBottom:8}}>
            <input type="file" accept=".csv" onChange={ev=>setFile(ev.target.files[0])} />
          </div>
          <button type="submit" style={{background:'#10b981',color:'white',padding:'8px 12px',borderRadius:6}}>Upload CSV</button>
        </form>
      </div>
      <div style={{marginTop:12}}>
        <h3 style={{fontWeight:700}}>Matches</h3>
        <ul style={{marginTop:8}}>
          {matches.map(m=>(
            <li key={m.id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',background:'#fff',padding:8,borderRadius:6,marginBottom:6}}>
              <div>{m.title}</div>
              <div><button onClick={()=>del(m.id)} style={{color:'#ef4444'}}>Excluir</button></div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
