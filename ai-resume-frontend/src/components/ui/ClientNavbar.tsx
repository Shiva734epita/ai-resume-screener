"use client"; // ✅ Ensure this is a client component

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";

export default function ClientNavbar() {
  const hideNavbarOn = ["/auth/login", "/auth/register", "/auth/reset-password", "/dashboard", "/auth/reset-password/verify"];
  const pathname = usePathname();
  
  if (hideNavbarOn.includes(pathname)) return null; // ✅ Hide navbar on auth pages

  return <Navbar showLogin={true} showRegister={true} showHome={true} />;
}
