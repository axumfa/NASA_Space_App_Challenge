"use client";

import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { RotationOption } from "@/types";

interface FitByYearTypeChartProps {
  options: RotationOption[];
}

export default function FitByYearTypeChart({ options }: FitByYearTypeChartProps) {
  const { t, language } = useTranslation();

  const data = options.map((opt, i) => {
    const name = opt.is_current ? (t("o.current") || "Current") : `Opt #${i}`;
    const crops = (language === "uz" ? opt.crop_names_uz : opt.crop_names_en).join(" → ");
    return {
      name,
      fullName: `${name}: ${crops}`,
      Dry: opt.fit_dry,
      Normal: opt.fit_normal,
      Wet: opt.fit_wet,
    };
  });

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("ui.sec_fit_years") || "Climate Resilience: Fit Across Dry, Normal & Wet Years"}
          </h4>
          <p className="text-[11px] text-[#7B8A7C]">
            Measures how each rotation performs under severe drought (dry years) vs. normal and wet years.
          </p>
        </div>
      </div>

      <div className="w-full h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
            <XAxis dataKey="name" tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} domain={[0, 100]} unit=" pts" />
            <Tooltip
              formatter={(val) => [`${Number(val).toFixed(0)} pts`, ""]}
              contentStyle={{
                backgroundColor: "#FFFFFF",
                borderRadius: "12px",
                border: "1px solid #D5D0C5",
                fontSize: "12px",
              }}
            />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
            <Bar dataKey="Dry" name="Dry Years (Drought)" fill="#D97706" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Normal" name="Normal Years" fill="#2F6B45" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Wet" name="Wet Years" fill="#3A6EA5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
