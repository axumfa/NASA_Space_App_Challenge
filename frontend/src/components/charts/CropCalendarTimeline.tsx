"use client";

import React from "react";
import { Calendar, Clock } from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import type { PlantingPeriod } from "@/types";

interface CropCalendarTimelineProps {
  plantings: PlantingPeriod[];
  bareDays: number;
}

const CROP_COLORS = ["#2F6B45", "#3A6EA5", "#D97706", "#7C3AED"];

export default function CropCalendarTimeline({
  plantings,
  bareDays,
}: CropCalendarTimelineProps) {
  const { t, language } = useTranslation();

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-4 shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324] flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-[#2F6B45]" />
            <span>{t("ui.sec_season") || "Annual Cropping Calendar & Ground Cover"}</span>
          </h4>
          <p className="text-[11px] text-[#7B8A7C]">
            Timeline of vegetative growth stages and bare soil exposure windows throughout the 365-day year.
          </p>
        </div>

        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-[#F0EFEB] text-[#4E5E50] text-xs font-semibold">
          <Clock className="w-3.5 h-3.5" />
          <span>{bareDays} bare soil days / year</span>
        </div>
      </div>

      {/* Visual Gantt Bar for the 365-day cycle */}
      <div className="relative w-full h-10 bg-[#EAE6DC] rounded-xl overflow-hidden flex my-3 border border-[#D5D0C5]">
        {plantings.map((p, idx) => {
          const widthPct = Math.min(100, Math.max(5, (p.duration_days / 365) * 100));
          const color = CROP_COLORS[idx % CROP_COLORS.length];
          const name = language === "uz" ? p.crop_name_uz : p.crop_name_en;

          return (
            <div
              key={p.crop_id + idx}
              style={{ width: `${widthPct}%`, backgroundColor: color }}
              className="h-full flex items-center justify-center text-white text-[11px] font-bold px-2 truncate border-r border-white/20 transition-all hover:brightness-110"
              title={`${name}: Day ${p.start_doy} to ${p.end_doy} (${p.duration_days} days)`}
            >
              {name}
            </div>
          );
        })}
      </div>

      {/* Detail Cards per Planting */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 pt-1">
        {plantings.map((p, idx) => {
          const color = CROP_COLORS[idx % CROP_COLORS.length];
          const name = language === "uz" ? p.crop_name_uz : p.crop_name_en;
          const sDate = language === "uz" ? p.start_date_uz : p.start_date_en;
          const eDate = language === "uz" ? p.end_date_uz : p.end_date_en;

          return (
            <div
              key={p.crop_id + idx}
              className="p-2.5 rounded-xl border border-[#E8E4DA] bg-[#FAF9F5] flex items-center justify-between"
            >
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full shrink-0"
                  style={{ backgroundColor: color }}
                />
                <div>
                  <div className="text-xs font-bold text-[#1A3324]">{name}</div>
                  <div className="text-[10px] text-[#7B8A7C]">
                    {sDate} → {eDate}
                  </div>
                </div>
              </div>
              <span className="text-[10px] font-mono font-bold text-[#4E5E50] bg-white px-1.5 py-0.5 rounded border border-[#DEDAD1]">
                {p.duration_days} d
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
