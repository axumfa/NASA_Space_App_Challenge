"use client";

import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { ClimatologyPoint } from "@/types";

interface TemperatureChartProps {
  data: ClimatologyPoint[];
}

export default function TemperatureChart({ data }: TemperatureChartProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("ui.sec_temp") || "Monthly Temperature Climatology"}
          </h4>
          <p className="text-[11px] text-[#7B8A7C]">
            Historical 24-year daily air temperature envelope (Min, Mean, Max).
          </p>
        </div>
      </div>

      <div className="w-full h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
            <XAxis dataKey="month_name" tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: "#58685A" }} tickLine={false} unit="°C" />
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
            <Line
              type="monotone"
              dataKey="t_max"
              name="T Max (°C)"
              stroke="#DC2626"
              strokeWidth={2}
              dot={{ r: 2.5 }}
            />
            <Line
              type="monotone"
              dataKey="t_mean"
              name="T Mean (°C)"
              stroke="#4B5563"
              strokeWidth={2}
              dot={{ r: 2.5 }}
            />
            <Line
              type="monotone"
              dataKey="t_min"
              name="T Min (°C)"
              stroke="#2563EB"
              strokeWidth={2}
              dot={{ r: 2.5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
