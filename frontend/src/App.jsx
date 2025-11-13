import React from 'react'
import MatchList from './components/MatchList'
import AdminPanel from './components/AdminPanel'
export default function App(){
  return (
    <div style={{minHeight:'100vh',background:'#f3f4f6'}}>
      <header style={{background:'#4f46e5',color:'white',padding:12}}><div className="container">FutAnalysis</div></header>
      <main className="container" style={{paddingTop:20}}>
        <MatchList />
        <hr style={{margin:'24px 0'}} />
        <AdminPanel />
      </main>
    </div>
  )
}
