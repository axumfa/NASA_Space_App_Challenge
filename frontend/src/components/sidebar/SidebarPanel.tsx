"use client";

import React from "react";
import { SlidersHorizontal, Pin, X, PanelLeftClose } from "lucide-react";
import CropSelector from "./CropSelector";
import PrioritiesSliders from "./PrioritiesSliders";
import WhatIfForm from "./WhatIfForm";
import type { ConfigResponse } from "@/types";
import { useTranslation } from "@/lib/i18n";

interface SidebarPanelProps {
  config?: ConfigResponse;
  mode: "pinned" | "drawer";
  onCollapse?: () => void;
  onPin?: () => void;
  onClose?: () => void;
}

export default function SidebarPanel({
  config,
  mode,
  onCollapse,
  onPin,
  onClose,
}: SidebarPanelProps) {
  const { t, language } = useTranslation();

  const titleText =
    language === "uz" ? "Boshqaruv va ssenariylar" : "Rotation & Climate Controls";

  return (
    <div className="space-y-4">
      {/* Header bar of sidebar panel */}
      <div className="flex items-center justify-between px-1 pb-1 border-b border-[#E3DFD3]/60">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-[#2F6B45]/10 text-[#2F6B45] flex items-center justify-center">
            <SlidersHorizontal className="w-3.5 h-3.5" />
          </div>
          <span className="text-xs font-bold text-[#1A3324] uppercase tracking-wider">
            {titleText}
          </span>
        </div>

        {mode === "pinned" ? (
          <button
            type="button"
            onClick={onCollapse}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold text-[#526356] hover:text-[#1A3324] hover:bg-[#EAE6DB] transition-all border border-transparent hover:border-[#D5D0C5] cursor-pointer"
            title="Collapse controls to give charts full width (auto-spreads on left edge hover)"
          >
            <PanelLeftClose className="w-3.5 h-3.5" />
            <span className="text-[11px]">Collapse</span>
          </button>
        ) : (
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={onPin}
              className="flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-[#2F6B45] bg-[#E8F0EA] hover:bg-[#D7E6DA] border border-[#C5DDCB] transition-colors cursor-pointer"
              title="Pin controls back into layout"
            >
              <Pin className="w-3 h-3" />
              <span className="text-[11px]">Pin to Page</span>
            </button>
            <button
              type="button"
              onClick={onClose}
              className="p-1 rounded-lg text-[#526356] hover:text-[#1A3324] hover:bg-[#EAE6DB] transition-colors cursor-pointer"
              title="Close drawer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {config && <CropSelector crops={config.crops} />}
      {config && (
        <PrioritiesSliders
          profiles={config.profiles}
          priorities={config.priorities}
        />
      )}
      <WhatIfForm />
    </div>
  );
}
