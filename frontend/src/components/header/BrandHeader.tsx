"use client";

import React from "react";
import { Sprout } from "lucide-react";
import { useTranslation } from "@/lib/i18n";

export default function BrandHeader() {
  const { t } = useTranslation();

  return (
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-xl bg-[#2F6B45] text-white flex items-center justify-center shadow-sm">
        <Sprout className="w-6 h-6" />
      </div>
      <div>
        <div className="flex items-center gap-2">
          <span className="text-xl font-bold tracking-tight text-[#1A3324]">
            Field Shift
          </span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-[#E8F0EA] text-[#2F6B45] font-semibold tracking-wide border border-[#C5DDCB]">
            NASA Space Apps
          </span>
        </div>
        <p className="text-xs text-[#526356] font-medium leading-tight">
          {t("ui.tagline") || "Crop-rotation decision support with NASA data"}
        </p>
      </div>
    </div>
  );
}
