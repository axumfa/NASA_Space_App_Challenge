"use client";

import React from "react";
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import { useAppStore } from "@/lib/store";

export default function SidebarToggle() {
  const sidebarPinned = useAppStore((s) => s.sidebarPinned);
  const setSidebarPinned = useAppStore((s) => s.setSidebarPinned);

  return (
    <button
      type="button"
      onClick={() => setSidebarPinned((prev) => !prev)}
      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#D5D0C5] bg-white hover:bg-[#F3EFE6] text-xs font-semibold text-[#2F6B45] transition-all shadow-2xs hover:shadow-xs active:scale-95 cursor-pointer"
      title={
        sidebarPinned
          ? "Collapse controls (auto-spreads on left edge hover)"
          : "Expand and pin controls to layout"
      }
    >
      {sidebarPinned ? (
        <>
          <PanelLeftClose className="w-4 h-4" />
          <span className="hidden sm:inline">Collapse</span>
        </>
      ) : (
        <>
          <PanelLeftOpen className="w-4 h-4" />
          <span className="hidden sm:inline">Controls</span>
        </>
      )}
    </button>
  );
}
