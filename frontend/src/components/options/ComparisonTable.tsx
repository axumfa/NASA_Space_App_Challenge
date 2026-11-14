"use client";

import React from "react";
import { Table, Trophy } from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import type { RotationOption } from "@/types";

interface ComparisonTableProps {
  options: RotationOption[];
  bestFitIndex: number;
}

export default function ComparisonTable({
  options,
  bestFitIndex,
}: ComparisonTableProps) {
  const { t, language } = useTranslation();

  const getCropNames = (r: RotationOption) => {
    const list = language === "uz" ? r.crop_names_uz : r.crop_names_en;
    return list.join(" → ");
  };

  const getBestIdx = (values: number[], higherIsBetter: boolean): number[] => {
    if (values.length < 2) return [];
    const target = higherIsBetter ? Math.max(...values) : Math.min(...values);
    return values
      .map((v, i) => (Math.abs(v - target) < 1e-4 ? i : -1))
      .filter((i) => i !== -1);
  };

  const fitScores = options.map((o) => o.fit_score);
  const bestFitIdxs = getBestIdx(fitScores, true);

  const irrValues = options.map((o) => o.irrigation_demand_mm);
  const bestIrrIdxs = getBestIdx(irrValues, false);

  const bareValues = options.map((o) => o.bare_days_per_year);
  const bestBareIdxs = getBestIdx(bareValues, false);

  const nValues = options.map((o) => o.nitrogen_kg_median);
  const bestNIdxs = getBestIdx(nValues, true);

  const yldValues = options.map((o) => o.yield_loss_median_pct);
  const bestYldIdxs = getBestIdx(yldValues, false);

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs overflow-x-auto">
      <div className="flex items-center gap-2 mb-3">
        <Table className="w-4 h-4 text-[#2F6B45]" />
        <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
          {t("ui.sec_compare") || "At-A-Glance Rotation Trade-Off Matrix"}
        </h4>
      </div>

      <table className="w-full text-xs text-left border-collapse min-w-[650px]">
        <thead>
          <tr className="border-b border-[#E3DFD3] bg-[#FAF9F5]">
            <th className="py-2.5 px-3 font-semibold text-[#526356] w-48">
              {t("ui.tbl_metric") || "Agronomic Metric"}
            </th>
            {options.map((opt, i) => (
              <th
                key={opt.index}
                className={`py-2.5 px-3 font-bold ${
                  i === bestFitIndex
                    ? "text-[#2F6B45] bg-[#EBF3ED]/50 border-x border-[#CCE0D1]"
                    : "text-[#1A3324]"
                }`}
              >
                <div className="flex items-center gap-1.5">
                  <span>{opt.is_current ? t("o.current") || "Current" : `Option #${i}`}</span>
                  {i === bestFitIndex && (
                    <span className="flex items-center gap-0.5 px-1.5 py-0.5 rounded-full bg-[#2F6B45] text-white text-[9px] font-extrabold uppercase">
                      <Trophy className="w-2.5 h-2.5" /> Best
                    </span>
                  )}
                </div>
                <div className="text-[11px] font-normal text-[#667568] mt-0.5 line-clamp-1">
                  {getCropNames(opt)}
                </div>
              </th>
            ))}
          </tr>
        </thead>

        <tbody className="divide-y divide-[#EAE6DC]">
          {/* Group: Core Fit */}
          <tr className="bg-[#FAF9F5]/60 font-bold text-[10px] text-[#2F6B45] uppercase tracking-wider">
            <td colSpan={options.length + 1} className="py-1 px-3">
              {t("ui.g_main") || "Fit & Climate Resilience"}
            </td>
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_fit") || "Overall Fit Score (0–100)"}
            </td>
            {options.map((opt, i) => {
              const isBest = bestFitIdxs.includes(i);
              return (
                <td
                  key={i}
                  className={`py-2 px-3 font-mono font-bold ${
                    isBest ? "text-[#2F6B45] bg-[#EBF3ED]/40" : "text-[#1A3324]"
                  }`}
                >
                  {opt.fit_score.toFixed(0)}
                </td>
              );
            })}
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_dry") || "Dry / Normal / Wet Year Fit"}
            </td>
            {options.map((opt, i) => (
              <td key={i} className="py-2 px-3 font-mono text-[#526356]">
                {opt.fit_dry.toFixed(0)} / {opt.fit_normal.toFixed(0)} / {opt.fit_wet.toFixed(0)}
              </td>
            ))}
          </tr>

          {/* Group: Water & Yield */}
          <tr className="bg-[#FAF9F5]/60 font-bold text-[10px] text-[#2F6B45] uppercase tracking-wider">
            <td colSpan={options.length + 1} className="py-1 px-3">
              {t("ui.g_water") || "Water & Productivity"}
            </td>
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_irr") || "Irrigation Demand (mm/yr)"}
            </td>
            {options.map((opt, i) => {
              const isBest = bestIrrIdxs.includes(i);
              return (
                <td
                  key={i}
                  className={`py-2 px-3 font-mono font-bold ${
                    isBest ? "text-[#2F6B45] bg-[#EBF3ED]/40" : "text-[#1A3324]"
                  }`}
                >
                  {opt.irrigation_demand_mm.toFixed(0)} mm
                  {opt.irrigation_delta_pct !== null && (
                    <span className="text-[10px] font-normal text-[#7B8A7C] ml-1">
                      ({opt.irrigation_delta_pct > 0 ? "+" : ""}{opt.irrigation_delta_pct}%)
                    </span>
                  )}
                </td>
              );
            })}
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_yield") || "Yield Loss Risk (Median / P90)"}
            </td>
            {options.map((opt, i) => {
              const isBest = bestYldIdxs.includes(i);
              return (
                <td
                  key={i}
                  className={`py-2 px-3 font-mono ${
                    isBest ? "text-[#2F6B45] font-bold bg-[#EBF3ED]/40" : "text-[#1A3324]"
                  }`}
                >
                  {opt.yield_loss_median_pct.toFixed(0)}% / {opt.yield_loss_p90_pct.toFixed(0)}%
                </td>
              );
            })}
          </tr>

          {/* Group: Soil & Nutrients */}
          <tr className="bg-[#FAF9F5]/60 font-bold text-[10px] text-[#2F6B45] uppercase tracking-wider">
            <td colSpan={options.length + 1} className="py-1 px-3">
              {t("ui.g_soil") || "Soil Health & Nutrient Balance"}
            </td>
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_bare") || "Bare Soil Days / Year"}
            </td>
            {options.map((opt, i) => {
              const isBest = bestBareIdxs.includes(i);
              return (
                <td
                  key={i}
                  className={`py-2 px-3 font-mono font-bold ${
                    isBest ? "text-[#2F6B45] bg-[#EBF3ED]/40" : "text-[#1A3324]"
                  }`}
                >
                  {opt.bare_days_per_year.toFixed(0)} d
                </td>
              );
            })}
          </tr>
          <tr>
            <td className="py-2 px-3 font-medium text-[#38453A]">
              {t("ui.tbl_n") || "Nitrogen Balance (kg N/ha)"}
            </td>
            {options.map((opt, i) => {
              const isBest = bestNIdxs.includes(i);
              return (
                <td
                  key={i}
                  className={`py-2 px-3 font-mono font-bold ${
                    isBest ? "text-[#2F6B45] bg-[#EBF3ED]/40" : "text-[#1A3324]"
                  }`}
                >
                  {opt.nitrogen_kg_median.toFixed(0)} kg
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
