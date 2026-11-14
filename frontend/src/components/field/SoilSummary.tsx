"use client";

import React from "react";
import { Layers, Database } from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import type { SoilData, SatelliteData } from "@/types";

interface SoilSummaryProps {
  soil: SoilData;
  satellite: SatelliteData;
}

export default function SoilSummary({ soil, satellite }: SoilSummaryProps) {
  const { t } = useTranslation();

  const record = soil.records && soil.records.length > 0 ? soil.records[0] : null;

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324] flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5 text-[#2F6B45]" />
          <span>{t("ui.sec_soil") || "Soil Physical Properties & Root-Zone Hydrology"}</span>
        </h4>
        <span className="text-[10px] text-[#7B8A7C] font-mono">
          Source: {soil.source || "ISRIC SoilGrids 250m"}
        </span>
      </div>

      {soil.ok && record ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5">
          {Object.entries(record).map(([k, v]) => {
            const labelKey = `soil.${k}`;
            const label = t(labelKey) !== labelKey ? t(labelKey) : k;

            return (
              <div
                key={k}
                className="p-2.5 rounded-xl border border-[#EAE6DC] bg-[#FAF9F5] text-center"
              >
                <div className="text-[10px] font-semibold text-[#7B8A7C] uppercase tracking-wider mb-1 line-clamp-1">
                  {label}
                </div>
                <div className="text-sm font-bold text-[#1A3324] font-mono">
                  {typeof v === "number" ? v.toFixed(1) : String(v)}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-[#FAF9F5] text-xs text-[#7B8A7C] text-center border border-dashed border-[#D5D0C5]">
          Soil data not directly retrieved for this point. Default regional characteristics apply.
        </div>
      )}
    </div>
  );
}
