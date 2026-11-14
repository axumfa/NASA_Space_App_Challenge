"use client";

import React from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { ClimatologyPoint } from "@/types";

interface WaterBalanceChartProps {
  data: ClimatologyPoint[];
}

export default function WaterBalanceChart({ data }: WaterBalanceChartProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("ui.sec_wb") || "Monthly Water Balance: Precipitation vs. ET₀"}
          </h4>
          <p className="text-[11px] text-[#7B8A7C]">
            Compares water supply (Rainfall) against crop evaporative demand (ET₀).
          </p>
        </div>
      </div>

      <div className="w-full h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
            <XAxis dataKey="month_name" tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} unit=" mm" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#FFFFFF",
                borderRadius: "12px",
                border: "1px solid #D5D0C5",
                fontSize: "12px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              }}
            />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
            <Bar dataKey="rain_mm" name="Rainfall (mm)" fill="#3A6EA5" radius={[4, 4, 0, 0]} />
            <Line
              type="monotone"
              dataKey="et0_mm"
              name="ET₀ Demand (mm)"
              stroke="#D97706"
              strokeWidth={2.5}
              dot={{ r: 3, fill: "#D97706" }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
