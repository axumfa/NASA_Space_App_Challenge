"use client";

import React from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { SatelliteData } from "@/types";

interface NdviCurveChartProps {
  satellite: SatelliteData;
}

export default function NdviCurveChart({ satellite }: NdviCurveChartProps) {
  const { t } = useTranslation();

  if (!satellite.has_ndvi || !satellite.ndvi_curve) {
    return null;
  }

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("ui.sec_ndvi") || "MODIS NDVI Seasonal Vegetation Dynamics"}
          </h4>
          <p className="text-[11px] text-[#7B8A7C]">
            Remote sensing greenness curve (250 m resolution, 16-day composites) vs. bare ground baseline (0.2).
          </p>
        </div>

        {satellite.observed_bare_days !== null && (
          <div className="text-xs font-semibold px-2.5 py-1 rounded-xl bg-[#EBF3ED] text-[#2F6B45] border border-[#CCE0D1]">
            Observed bare days: {satellite.observed_bare_days} d
          </div>
        )}
      </div>

      <div className="w-full h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={satellite.ndvi_curve}
            margin={{ top: 5, right: 10, left: -25, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#EAE6DC" vertical={false} />
            <XAxis dataKey="doy" tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} unit=" DOY" />
            <YAxis tick={{ fontSize: 10, fill: "#58685A" }} tickLine={false} domain={[0, 1]} />
            <Tooltip
              formatter={(val) => [Number(val).toFixed(3), "NDVI"]}
              contentStyle={{
                backgroundColor: "#FFFFFF",
                borderRadius: "10px",
                border: "1px solid #D5D0C5",
                fontSize: "11px",
              }}
            />
            <ReferenceLine y={0.2} stroke="#DC2626" strokeDasharray="3 3" label={{ value: "Bare threshold (0.2)", fill: "#DC2626", fontSize: 10 }} />
            <Line
              type="monotone"
              dataKey="median"
              stroke="#2F6B45"
              strokeWidth={2.5}
              dot={{ r: 2 }}
              name="Median NDVI"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
