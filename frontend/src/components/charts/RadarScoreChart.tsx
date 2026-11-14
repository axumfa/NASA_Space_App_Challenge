"use client";

import React from "react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  Tooltip,
} from "recharts";
import { useTranslation } from "@/lib/i18n";
import type { RotationOption } from "@/types";

interface RadarScoreChartProps {
  currentOption: RotationOption;
  candidateOption: RotationOption;
  candidateColor?: string;
}

export default function RadarScoreChart({
  currentOption,
  candidateOption,
  candidateColor = "#2F6B45",
}: RadarScoreChartProps) {
  const { t } = useTranslation();

  const metrics = [
    { key: "water_saving", label: t("p.water_saving") || "Water Saving" },
    { key: "soil_om", label: t("p.soil_om") || "Soil OM" },
    { key: "nitrogen", label: t("p.nitrogen") || "Nitrogen" },
    { key: "erosion", label: t("p.erosion") || "Erosion Reduction" },
    { key: "forage", label: t("p.forage") || "Forage Value" },
    { key: "income", label: t("p.income") || "Income Tier" },
  ];

  const data = metrics.map((m) => ({
    metric: m.label,
    Current: currentOption.radar_scores[m.key] ?? 50,
    Candidate: candidateOption.radar_scores[m.key] ?? 50,
  }));

  const isCurrent = candidateOption.is_current;

  return (
    <div className="w-full h-[220px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 10 }}>
          <PolarGrid stroke="#E3DFD3" />
          <PolarAngleAxis
            dataKey="metric"
            tick={{ fontSize: 10, fill: "#4E5E50", fontWeight: 600 }}
          />
          <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
          {!isCurrent && (
            <Radar
              name="Current Rotation"
              dataKey="Current"
              stroke="#9CA3AF"
              fill="#9CA3AF"
              fillOpacity={0.2}
            />
          )}
          <Radar
            name={isCurrent ? "Current Rotation" : "This Option"}
            dataKey="Candidate"
            stroke={candidateColor}
            fill={candidateColor}
            fillOpacity={0.4}
          />
          <Tooltip
            formatter={(val) => [`${Number(val).toFixed(0)} / 100`, "Score"]}
            contentStyle={{
              backgroundColor: "#FFFFFF",
              borderRadius: "10px",
              border: "1px solid #D5D0C5",
              fontSize: "11px",
            }}
          />
          <Legend wrapperStyle={{ fontSize: "11px" }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
