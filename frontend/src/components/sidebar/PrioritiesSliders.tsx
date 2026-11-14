"use client";

import React, { useState } from "react";
import { Sliders, ChevronDown, ChevronUp } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";

interface PrioritiesSlidersProps {
  profiles: Record<string, Record<string, number>>;
  priorities: string[];
}

export default function PrioritiesSliders({
  profiles,
  priorities,
}: PrioritiesSlidersProps) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(true);
  const profile = useAppStore((s) => s.profile);
  const weights = useAppStore((s) => s.weights);
  const setProfile = useAppStore((s) => s.setProfile);
  const setWeight = useAppStore((s) => s.setWeight);

  const handleProfileChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const profName = e.target.value;
    const profWeights = profiles[profName];
    setProfile(profName, profWeights);
  };

  const envPriorities = ["water_saving", "soil_om", "nitrogen", "erosion"];
  const econPriorities = ["forage", "income"];

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] shadow-xs overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between text-left hover:bg-[#FAF9F5] transition-colors cursor-pointer"
      >
        <div className="flex items-center gap-2">
          <Sliders className="w-4 h-4 text-[#2F6B45]" />
          <h3 className="text-sm font-bold text-[#1A3324]">
            {t("ui.sidebar_prio") || "Farmer Priorities"}
          </h3>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-[#7B8A7C]" />
        ) : (
          <ChevronDown className="w-4 h-4 text-[#7B8A7C]" />
        )}
      </button>

      {isOpen && (
        <div className="p-4 pt-0 space-y-4">
          {/* Quick Profile Select */}
          <div>
            <label className="block text-[11px] font-semibold text-[#667568] mb-1">
              {t("side.quick") || "Preset Focus Profile"}
            </label>
            <select
              value={profile}
              onChange={handleProfileChange}
              className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-[#1A3324] text-xs rounded-xl px-2.5 py-1.5 font-medium focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45] cursor-pointer"
            >
              <option value="Balanced">Balanced (Equal weights)</option>
              {Object.keys(profiles).map((p) => (
                <option key={p} value={p}>
                  {t(`profile.${p}`) || p}
                </option>
              ))}
            </select>
          </div>

          {/* Environmental Group */}
          <div>
            <div className="text-[10px] font-bold uppercase tracking-wider text-[#2F6B45] mb-2">
              {t("ui.grp_env") || "Environmental & Soil Health"}
            </div>
            <div className="space-y-2.5">
              {envPriorities.map((key) => (
                <div key={key}>
                  <div className="flex justify-between items-center text-xs mb-1">
                    <span className="font-medium text-[#38453A]">
                      {t(`p.${key}`) || key}
                    </span>
                    <span className="font-mono text-xs font-semibold text-[#2F6B45] bg-[#EBF3ED] px-1.5 py-0.5 rounded">
                      {weights[key] ?? 5}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    step="1"
                    value={weights[key] ?? 5}
                    onChange={(e) => setWeight(key, parseFloat(e.target.value))}
                    className="w-full accent-[#2F6B45] cursor-pointer"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Economic Group */}
          <div className="pt-2 border-t border-[#EAE6DC]">
            <div className="text-[10px] font-bold uppercase tracking-wider text-[#2F6B45] mb-2">
              {t("ui.grp_econ") || "Economic & Livestock"}
            </div>
            <div className="space-y-2.5">
              {econPriorities.map((key) => (
                <div key={key}>
                  <div className="flex justify-between items-center text-xs mb-1">
                    <span className="font-medium text-[#38453A]">
                      {t(`p.${key}`) || key}
                    </span>
                    <span className="font-mono text-xs font-semibold text-[#2F6B45] bg-[#EBF3ED] px-1.5 py-0.5 rounded">
                      {weights[key] ?? 5}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    step="1"
                    value={weights[key] ?? 5}
                    onChange={(e) => setWeight(key, parseFloat(e.target.value))}
                    className="w-full accent-[#2F6B45] cursor-pointer"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
