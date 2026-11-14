"use client";

import React from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { FrostWeekPoint, HeatMonthPoint } from "@/types";

interface FrostHeatChartProps {
  frost: FrostWeekPoint[];
  heat: HeatMonthPoint[];
}

export default function FrostHeatChart({ frost, heat }: FrostHeatChartProps) {
  const { t } = useTranslation();
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const heatData = heat.map((h) => ({
    ...h,
    month_name: monthNames[h.month - 1] || `${h.month}`,
  }));

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      {/* Frost Probability by Week */}
      <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
        <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324] mb-1">
          {t("ui.sec_frost") || "Weekly Frost Occurrence Risk"}
        </h4>
        <p className="text-[11px] text-[#7B8A7C] mb-3">
          Probability of minimum temperature falling below 0 °C by calendar week.
        </p>
        <div className="w-full h-[180px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={frost} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
              <XAxis dataKey="week" tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} unit="w" />
              <YAxis tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} domain={[0, 1]} />
              <Tooltip
                formatter={(val) => [`${(Number(val) * 100).toFixed(1)}%`, "Frost Risk"]}
                contentStyle={{
                  backgroundColor: "#FFFFFF",
                  borderRadius: "10px",
                  border: "1px solid #D5D0C5",
                  fontSize: "11px",
                }}
              />
              <Area type="monotone" dataKey="frost_prob" stroke="#0284C7" fill="#E0F2FE" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Extreme Heat Days */}
      <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
        <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324] mb-1">
          {t("ui.sec_heat") || "Extreme Heat Days per Month (≥ 35 °C)"}
        </h4>
        <p className="text-[11px] text-[#7B8A7C] mb-3">
          Average count of scorching heat days inducing crop thermal stress.
        </p>
        <div className="w-full h-[180px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={heatData} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
              <XAxis dataKey="month_name" tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} />
              <YAxis tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} />
              <Tooltip
                formatter={(val) => [`${Number(val).toFixed(1)} days`, "Days ≥ 35°C"]}
                contentStyle={{
                  backgroundColor: "#FFFFFF",
                  borderRadius: "10px",
                  border: "1px solid #D5D0C5",
                  fontSize: "11px",
                }}
              />
              <Bar dataKey="heat_days" fill="#DC2626" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
