"use client";

import { useEffect, useState } from "react";

export default function HydrationProvider({ children }: { children: React.ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) return <div suppressHydrationWarning={true} />; // ✅ Prevents hydration mismatch

  return <>{children}</>;
}
