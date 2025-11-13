import React, {useEffect, useState} from 'react'
import API from '../api'
export default function MatchList(){
  const [matches, setMatches] = useState([])
  useEffect(()=>{ API.get('/matches').then(r=>setMatches(r.data)).catch(()=>{}) },[])
  return (
    <div>
      <h2 style={{fontSize:20,fontWeight:600}}>Partidas</h2>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(320px,1fr))',gap:12,marginTop:12}}>
        {matches.map(m=> (
          <div key={m.id} className="card">
            <div style={{fontWeight:700}}>{m.title}</div>
            <div style={{fontSize:12,color:'#6b7280'}}>{m.competition} • {m.date}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
