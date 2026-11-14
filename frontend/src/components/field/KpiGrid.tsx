"use client";

import React from "react";
import { Droplet, Sun, Thermometer, Snowflake, Calendar, TrendingUp } from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import type { AnnualKpis } from "@/types";

interface KpiGridProps {
  kpis: AnnualKpis;
}

export default function KpiGrid({ kpis }: KpiGridProps) {
  const { t } = useTranslation();

  const cards = [
    {
      title: t("ui.kpi_rain") || "Annual Precipitation",
      value: `${kpis.rain_median.toFixed(0)}`,
      unit: "mm",
      sub: `${kpis.rain_p10.toFixed(0)} – ${kpis.rain_p90.toFixed(0)} mm (10–90%)`,
      icon: Droplet,
      iconColor: "text-[#3A6EA5]",
      bgColor: "bg-[#F0F5FA]",
    },
    {
      title: t("ui.kpi_et0") || "Reference Evapotranspiration (ET₀)",
      value: `${kpis.et0_median.toFixed(0)}`,
      unit: "mm",
      sub: kpis.is_deficit
        ? `Deficit of ${kpis.gap_mm.toFixed(0)} mm/yr`
        : `Surplus of ${(-kpis.gap_mm).toFixed(0)} mm/yr`,
      icon: Sun,
      iconColor: "text-[#D97706]",
      bgColor: "bg-[#FEF8ED]",
      warn: kpis.is_deficit,
    },
    {
      title: t("ui.kpi_temp") || "Annual Mean Temperature",
      value: `${kpis.temp_median.toFixed(1)}`,
      unit: "°C",
      sub: `Trend: ${kpis.temp_trend_slope > 0 ? "+" : ""}${kpis.temp_trend_slope.toFixed(2)} °C / decade`,
      icon: Thermometer,
      iconColor: "text-[#C84B31]",
      bgColor: "bg-[#FDF0ED]",
    },
    {
      title: t("ui.kpi_last") || "Last Spring Frost Date",
      value: kpis.last_spring_frost_median || "None",
      unit: "",
      sub: `Typical window: ${kpis.last_spring_frost_p10} – ${kpis.last_spring_frost_p90}`,
      icon: Snowflake,
      iconColor: "text-[#0284C7]",
      bgColor: "bg-[#F0F9FF]",
    },
    {
      title: t("ui.kpi_first") || "First Autumn Frost Date",
      value: kpis.first_autumn_frost_median || "None",
      unit: "",
      sub: `Typical window: ${kpis.first_autumn_frost_p10} – ${kpis.first_autumn_frost_p90}`,
      icon: Snowflake,
      iconColor: "text-[#0284C7]",
      bgColor: "bg-[#F0F9FF]",
    },
    {
      title: t("ui.kpi_free") || "Frost-Free Growing Season",
      value: `${kpis.frost_free_days_median.toFixed(0)}`,
      unit: "days",
      sub: `${kpis.frost_free_days_p10.toFixed(0)} – ${kpis.frost_free_days_p90.toFixed(0)} days range`,
      icon: Calendar,
      iconColor: "text-[#2F6B45]",
      bgColor: "bg-[#EBF3ED]",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <div
            key={i}
            className="bg-white rounded-2xl border border-[#E3DFD3] p-3.5 shadow-xs flex flex-col justify-between"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold text-[#58685A] line-clamp-1">
                {c.title}
              </span>
              <div className={`w-6 h-6 rounded-lg ${c.bgColor} ${c.iconColor} flex items-center justify-center shrink-0`}>
                <Icon className="w-3.5 h-3.5" />
              </div>
            </div>

            <div>
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-extrabold text-[#1A3324] font-mono tracking-tight">
                  {c.value}
                </span>
                {c.unit && (
                  <span className="text-xs font-semibold text-[#7B8A7C]">
                    {c.unit}
                  </span>
                )}
              </div>
              <div className={`text-[10px] mt-1 font-medium ${c.warn ? "text-[#C84B31] font-semibold" : "text-[#7B8A7C]"}`}>
                {c.sub}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
