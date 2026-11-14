"use client";

import React, { useState } from "react";
import { CloudRain, Thermometer, Droplets, ChevronDown, ChevronUp } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";

export default function WhatIfForm() {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const whatIf = useAppStore((s) => s.whatIf);
  const setWhatIf = useAppStore((s) => s.setWhatIf);

  // Local state until applied
  const [rain, setRain] = useState(whatIf.rainPct);
  const [temp, setTemp] = useState(whatIf.tempC);
  const [supply, setSupply] = useState(Math.round(whatIf.supply * 100));

  const handleApply = (e: React.FormEvent) => {
    e.preventDefault();
    setWhatIf(rain, temp, supply / 100);
  };

  const isScenarioActive = whatIf.rainPct !== 0 || whatIf.tempC !== 0 || whatIf.supply < 1.0;

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] shadow-xs overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between text-left hover:bg-[#FAF9F5] transition-colors cursor-pointer"
      >
        <div className="flex items-center gap-2">
          <CloudRain className="w-4 h-4 text-[#2F6B45]" />
          <div>
            <h3 className="text-sm font-bold text-[#1A3324]">
              {t("side.whatif") || "What-If Climate Scenarios"}
            </h3>
            {isScenarioActive && (
              <span className="text-[10px] text-[#A65B17] font-semibold">
                ● Active scenario applied
              </span>
            )}
          </div>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-[#7B8A7C]" />
        ) : (
          <ChevronDown className="w-4 h-4 text-[#7B8A7C]" />
        )}
      </button>

      {isOpen && (
        <form onSubmit={handleApply} className="p-4 pt-0 space-y-3.5">
          {/* Rainfall change */}
          <div>
            <div className="flex justify-between items-center text-xs mb-1">
              <span className="font-medium text-[#38453A] flex items-center gap-1">
                <CloudRain className="w-3.5 h-3.5 text-[#3A6EA5]" />
                {t("side.rain") || "Rainfall shift"}
              </span>
              <span className="font-mono text-xs font-semibold text-[#1A3324] bg-[#F0EFEB] px-1.5 py-0.5 rounded">
                {rain > 0 ? `+${rain}%` : `${rain}%`}
              </span>
            </div>
            <input
              type="range"
              min="-30"
              max="20"
              step="5"
              value={rain}
              onChange={(e) => setRain(parseInt(e.target.value, 10))}
              className="w-full accent-[#3A6EA5] cursor-pointer"
            />
          </div>

          {/* Temperature change */}
          <div>
            <div className="flex justify-between items-center text-xs mb-1">
              <span className="font-medium text-[#38453A] flex items-center gap-1">
                <Thermometer className="w-3.5 h-3.5 text-[#C84B31]" />
                {t("side.temp") || "Temperature anomaly"}
              </span>
              <span className="font-mono text-xs font-semibold text-[#1A3324] bg-[#F0EFEB] px-1.5 py-0.5 rounded">
                +{temp.toFixed(1)} °C
              </span>
            </div>
            <input
              type="range"
              min="0.0"
              max="3.0"
              step="0.5"
              value={temp}
              onChange={(e) => setTemp(parseFloat(e.target.value))}
              className="w-full accent-[#C84B31] cursor-pointer"
            />
          </div>

          {/* Irrigation supply limit */}
          <div>
            <div className="flex justify-between items-center text-xs mb-1">
              <span className="font-medium text-[#38453A] flex items-center gap-1">
                <Droplets className="w-3.5 h-3.5 text-[#2F6B45]" />
                {t("side.supply") || "Irrigation water quota"}
              </span>
              <span className="font-mono text-xs font-semibold text-[#1A3324] bg-[#F0EFEB] px-1.5 py-0.5 rounded">
                {supply}%
              </span>
            </div>
            <input
              type="range"
              min="40"
              max="100"
              step="5"
              value={supply}
              onChange={(e) => setSupply(parseInt(e.target.value, 10))}
              className="w-full accent-[#2F6B45] cursor-pointer"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-[#2F6B45] hover:bg-[#235335] text-white text-xs font-bold rounded-xl shadow-xs transition-colors cursor-pointer"
          >
            {t("side.apply") || "Simulate Scenario"}
          </button>
        </form>
      )}
    </div>
  );
}
