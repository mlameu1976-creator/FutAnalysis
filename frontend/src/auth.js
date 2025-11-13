export function setToken(token){ localStorage.setItem('token', token) }
export function getToken(){ return localStorage.getItem('token') }
export function authHeader(){ const t = getToken(); return t ? { Authorization: `Bearer ${t}` } : {} }
