import { NextResponse } from "next/server";

export function middleware(req) {
  const isLogged = true; // depois vira auth real

  if (!isLogged && req.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}