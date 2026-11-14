"use client";

import React from "react";
import { ArrowRight, Wheat } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";
import type { CropInfo } from "@/types";

interface CropSelectorProps {
  crops: Record<string, CropInfo>;
}

export default function CropSelector({ crops }: CropSelectorProps) {
  const { t, language } = useTranslation();
  const currentCrops = useAppStore((s) => s.currentCrops);
  const setCrop = useAppStore((s) => s.setCrop);

  const getCropName = (id: string) => {
    if (!id || id === "—") return t("side.none") || "— None —";
    const trKey = `crop.${id}`;
    const translated = t(trKey);
    return translated !== trKey ? translated : crops[id]?.name || id;
  };

  const cropKeys = Object.keys(crops);

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex items-center gap-2 mb-3">
        <Wheat className="w-4 h-4 text-[#2F6B45]" />
        <h3 className="text-sm font-bold text-[#1A3324]">
          {t("ui.sidebar_rot") || "Current Rotation Sequence"}
        </h3>
      </div>
      <p className="text-xs text-[#526356] mb-3">
        {t("ui.step_rot") || "Select the 1–3 crops in your current yearly rotation:"}
      </p>

      {/* 3 Selectors */}
      <div className="space-y-2.5">
        {[0, 1, 2].map((idx) => {
          const val = currentCrops[idx] || "—";
          return (
            <div key={idx}>
              <label className="block text-[11px] font-semibold text-[#667568] mb-1">
                {idx === 2
                  ? t("side.crop_opt", { n: idx + 1 }) || `Crop #${idx + 1} (Optional)`
                  : t("side.crop", { n: idx + 1 }) || `Crop #${idx + 1}`}
              </label>
              <select
                value={val}
                onChange={(e) => setCrop(idx, e.target.value)}
                className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-[#1A3324] text-xs rounded-xl px-2.5 py-1.5 font-medium focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45] cursor-pointer"
              >
                {idx > 0 && <option value="—">— None —</option>}
                {cropKeys.map((cid) => (
                  <option key={cid} value={cid}>
                    {getCropName(cid)}
                  </option>
                ))}
              </select>
            </div>
          );
        })}
      </div>

      {/* Rotation Preview Chips */}
      {currentCrops.length > 0 && (
        <div className="mt-3.5 pt-3 border-t border-[#EAE6DC]">
          <div className="text-[10px] font-semibold uppercase tracking-wider text-[#7B8A7C] mb-1.5">
            Sequence Preview
          </div>
          <div className="flex flex-wrap items-center gap-1.5">
            {currentCrops.map((cid, i) => (
              <React.Fragment key={cid}>
                <span className="px-2 py-1 rounded-lg bg-[#EBF3ED] text-[#235335] text-xs font-semibold border border-[#CCE0D1]">
                  {getCropName(cid)}
                </span>
                {i < currentCrops.length - 1 && (
                  <ArrowRight className="w-3 h-3 text-[#94A396]" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
