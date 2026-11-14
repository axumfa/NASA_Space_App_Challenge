"use client";

import React, { useState } from "react";
import {
  Trophy,
  Droplets,
  Calendar,
  Sparkles,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  HelpCircle,
  FileText,
} from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import RadarScoreChart from "@/components/charts/RadarScoreChart";
import type { RotationOption } from "@/types";

interface RotationOptionCardProps {
  option: RotationOption;
  currentOption: RotationOption;
  colorIndex: number;
}

const PALETTE = ["#2F6B45", "#3A6EA5", "#7C3AED", "#D97706", "#059669"];

export default function RotationOptionCard({
  option,
  currentOption,
  colorIndex,
}: RotationOptionCardProps) {
  const { t, language } = useTranslation();
  const [openSection, setOpenSection] = useState<string | null>("why");

  const cropNames = (language === "uz" ? option.crop_names_uz : option.crop_names_en).join(" → ");
  const ruleDesc = language === "uz" ? option.rule_desc_uz : option.rule_desc_en;
  const color = PALETTE[colorIndex % PALETTE.length];

  const toggleSection = (s: string) => {
    setOpenSection(openSection === s ? null : s);
  };

  return (
    <div
      className={`bg-white rounded-2xl border p-4 shadow-xs flex flex-col justify-between transition-all ${
        option.is_best_fit
          ? "border-[#2F6B45] ring-2 ring-[#2F6B45]/15"
          : "border-[#E3DFD3]"
      }`}
    >
      <div>
        {/* Card Header */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div>
            <div className="flex flex-wrap items-center gap-1.5 mb-1">
              <span
                className={`text-[10px] font-extrabold uppercase tracking-wide px-2 py-0.5 rounded-full ${
                  option.is_current
                    ? "bg-[#F0EFEB] text-[#4E5E50]"
                    : "bg-[#EBF3ED] text-[#2F6B45] border border-[#CCE0D1]"
                }`}
              >
                {option.is_current ? t("o.current") || "Current Rotation" : `Option #${option.index}`}
              </span>
              {option.is_best_fit && (
                <span className="flex items-center gap-1 text-[10px] font-extrabold uppercase tracking-wide px-2 py-0.5 rounded-full bg-[#2F6B45] text-white">
                  <Trophy className="w-2.5 h-2.5" /> Best Fit
                </span>
              )}
            </div>
            <h3 className="text-base font-extrabold text-[#1A3324] tracking-tight">
              {cropNames}
            </h3>
            {ruleDesc && (
              <p className="text-[11px] text-[#7B8A7C] font-medium mt-0.5">
                {ruleDesc}
              </p>
            )}
          </div>

          {/* Fit Score Badge */}
          <div className="text-right shrink-0">
            <div className="text-xl font-mono font-extrabold text-[#2F6B45]">
              {option.fit_score.toFixed(0)}
            </div>
            <div className="text-[9px] font-bold uppercase tracking-wider text-[#7B8A7C]">
              Fit Score
            </div>
          </div>
        </div>

        {/* Telemetry Stats Strip */}
        <div className="grid grid-cols-2 gap-2 my-3 p-2.5 rounded-xl bg-[#FAF9F5] border border-[#EAE6DC] text-xs">
          <div>
            <span className="text-[10px] text-[#7B8A7C] flex items-center gap-1">
              <Droplets className="w-3 h-3 text-[#3A6EA5]" /> Irrigation Demand
            </span>
            <div className="font-mono font-bold text-[#1A3324]">
              {option.irrigation_demand_mm.toFixed(0)} mm
              {option.irrigation_delta_pct !== null && (
                <span
                  className={`text-[10px] font-semibold ml-1 ${
                    option.irrigation_delta_pct <= 0 ? "text-[#2F6B45]" : "text-[#C84B31]"
                  }`}
                >
                  ({option.irrigation_delta_pct > 0 ? "+" : ""}{option.irrigation_delta_pct}%)
                </span>
              )}
            </div>
          </div>

          <div>
            <span className="text-[10px] text-[#7B8A7C] flex items-center gap-1">
              <Calendar className="w-3 h-3 text-[#D97706]" /> Bare Days / Year
            </span>
            <div className="font-mono font-bold text-[#1A3324]">
              {option.bare_days_per_year.toFixed(0)} days
            </div>
          </div>

          <div>
            <span className="text-[10px] text-[#7B8A7C] flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-[#2F6B45]" /> Nitrogen Credit
            </span>
            <div className="font-mono font-bold text-[#1A3324]">
              {option.nitrogen_kg_median.toFixed(0)} kg N/ha
            </div>
          </div>

          <div>
            <span className="text-[10px] text-[#7B8A7C] flex items-center gap-1">
              <AlertTriangle className="w-3 h-3 text-[#C84B31]" /> Yield Loss Risk
            </span>
            <div className="font-mono font-bold text-[#1A3324]">
              {option.yield_loss_median_pct.toFixed(0)}% median
            </div>
          </div>
        </div>

        {/* Radar Chart */}
        <div className="border-t border-[#EAE6DC] pt-2">
          <div className="text-[10px] font-bold uppercase tracking-wider text-[#7B8A7C] text-center mb-1">
            Fit to Farmer Priorities (6 Dimensions)
          </div>
          <RadarScoreChart
            currentOption={currentOption}
            candidateOption={option}
            candidateColor={color}
          />
        </div>
      </div>

      {/* Explanations Accordions */}
      <div className="border-t border-[#EAE6DC] pt-3 mt-3 space-y-1.5 text-xs">
        {/* Why this was suggested */}
        {option.explanations.why && option.explanations.why.length > 0 && (
          <div className="border border-[#EAE6DC] rounded-xl overflow-hidden">
            <button
              onClick={() => toggleSection("why")}
              className="w-full px-3 py-2 bg-[#FAF9F5] flex items-center justify-between text-left font-semibold text-[#1A3324] cursor-pointer"
            >
              <span className="flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-[#2F6B45]" />
                {t("ex.why") || "Why this was suggested"}
              </span>
              {openSection === "why" ? (
                <ChevronUp className="w-3.5 h-3.5 text-[#7B8A7C]" />
              ) : (
                <ChevronDown className="w-3.5 h-3.5 text-[#7B8A7C]" />
              )}
            </button>
            {openSection === "why" && (
              <ul className="p-3 bg-white space-y-1 text-[#4E5E50] border-t border-[#EAE6DC]">
                {option.explanations.why.map((it, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-[#2F6B45] font-bold">•</span>
                    <span>{language === "uz" ? it.uz : it.en}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* Evidence & Numbers */}
        {option.explanations.evidence && option.explanations.evidence.length > 0 && (
          <div className="border border-[#EAE6DC] rounded-xl overflow-hidden">
            <button
              onClick={() => toggleSection("evidence")}
              className="w-full px-3 py-2 bg-[#FAF9F5] flex items-center justify-between text-left font-semibold text-[#1A3324] cursor-pointer"
            >
              <span>{t("ex.evidence") || "Evidence & Numbers"}</span>
              {openSection === "evidence" ? (
                <ChevronUp className="w-3.5 h-3.5 text-[#7B8A7C]" />
              ) : (
                <ChevronDown className="w-3.5 h-3.5 text-[#7B8A7C]" />
              )}
            </button>
            {openSection === "evidence" && (
              <ul className="p-3 bg-white space-y-1 text-[#4E5E50] border-t border-[#EAE6DC]">
                {option.explanations.evidence.map((it, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-[#3A6EA5] font-bold">•</span>
                    <span>{language === "uz" ? it.uz : it.en}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* Benefits & Tradeoffs */}
        {option.explanations.benefits && option.explanations.benefits.length > 0 && (
          <div className="border border-[#EAE6DC] rounded-xl overflow-hidden">
            <button
              onClick={() => toggleSection("benefits")}
              className="w-full px-3 py-2 bg-[#FAF9F5] flex items-center justify-between text-left font-semibold text-[#1A3324] cursor-pointer"
            >
              <span>{t("ex.benefits") || "Benefits & Trade-offs"}</span>
              {openSection === "benefits" ? (
                <ChevronUp className="w-3.5 h-3.5 text-[#7B8A7C]" />
              ) : (
                <ChevronDown className="w-3.5 h-3.5 text-[#7B8A7C]" />
              )}
            </button>
            {openSection === "benefits" && (
              <ul className="p-3 bg-white space-y-1 text-[#4E5E50] border-t border-[#EAE6DC]">
                {option.explanations.benefits.map((it, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-[#2F6B45] font-bold">•</span>
                    <span>{language === "uz" ? it.uz : it.en}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* Agronomic Risks */}
        {option.explanations.risks && option.explanations.risks.length > 0 && (
          <div className="border border-[#EAE6DC] rounded-xl overflow-hidden">
            <button
              onClick={() => toggleSection("risks")}
              className="w-full px-3 py-2 bg-[#FAF9F5] flex items-center justify-between text-left font-semibold text-[#1A3324] cursor-pointer"
            >
              <span className="flex items-center gap-1.5 text-[#C84B31]">
                <AlertTriangle className="w-3.5 h-3.5" />
                {t("ex.risks") || "Local Agronomic Risks"}
              </span>
              {openSection === "risks" ? (
                <ChevronUp className="w-3.5 h-3.5 text-[#7B8A7C]" />
              ) : (
                <ChevronDown className="w-3.5 h-3.5 text-[#7B8A7C]" />
              )}
            </button>
            {openSection === "risks" && (
              <ul className="p-3 bg-white space-y-1 text-[#4E5E50] border-t border-[#EAE6DC]">
                {option.explanations.risks.map((it, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-[#C84B31] font-bold">•</span>
                    <span>{language === "uz" ? it.uz : it.en}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
