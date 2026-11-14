"use client";

import React from "react";
import { ArrowRight, CheckCircle2, AlertCircle, HelpCircle, Layers } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";
import type { ContextResponse } from "@/types";

interface HeroStatusProps {
  context: ContextResponse;
}

export default function HeroStatus({ context }: HeroStatusProps) {
  const { t, language } = useTranslation();
  const setView = useAppStore((s) => s.setView);
  const currentCrops = useAppStore((s) => s.currentCrops);
  const translations = useAppStore((s) => s.translations);

  const getCropName = (id: string) => {
    const trKey = `crop.${id}`;
    const entry = translations[trKey];
    return (language === "uz" ? entry?.uz : entry?.en) || id;
  };

  const lat = context.lat;
  const lon = context.lon;
  const coords = `${Math.abs(lat).toFixed(2)}° ${lat >= 0 ? "N" : "S"} · ${Math.abs(lon).toFixed(2)}° ${lon >= 0 ? "E" : "W"}`;

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-5 shadow-xs">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Left Column: Field Overview & Navigation */}
        <div className="lg:col-span-7 space-y-3.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-[#2F6B45] bg-[#EBF3ED] px-2.5 py-0.5 rounded-full border border-[#CCE0D1]">
              {t("ui.selected") || "Active Field"}
            </span>
            <span className="text-xs font-mono font-medium text-[#7B8A7C]">
              {coords} · {t("ui.elev", { m: Math.round(context.elevation_m) }) || `${Math.round(context.elevation_m)} m elevation`}
            </span>
          </div>

          <h2 className="text-2xl font-extrabold text-[#1A3324] tracking-tight">
            {context.field_name}
          </h2>

          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-xs font-semibold text-[#526356]">
              {t("ui.grows") || "Current cycle:"}
            </span>
            {currentCrops.map((c) => (
              <span
                key={c}
                className="px-2.5 py-1 rounded-xl bg-[#F0EFEB] text-[#2F6B45] text-xs font-bold border border-[#DEDAD1]"
              >
                {getCropName(c)}
              </span>
            ))}
          </div>

          <p className="text-xs text-[#586358] leading-relaxed pt-1">
            {t("ui.hero") || "Evaluated against 24 years of NASA POWER daily weather, SoilGrids physics, and MODIS/SMAP satellite observations."}
          </p>

          <div className="pt-2">
            <button
              onClick={() => setView("options")}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#2F6B45] hover:bg-[#235335] text-white text-xs font-bold shadow-xs transition-all cursor-pointer"
            >
              <span>{t("ui.cta") || "Explore Crop Rotation Alternatives"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Right Column: Data Provenance Grid */}
        <div className="lg:col-span-5 bg-[#FAF9F5] rounded-xl border border-[#EAE6DC] p-4">
          <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-[#4E5E50] mb-3">
            <Layers className="w-3.5 h-3.5 text-[#2F6B45]" />
            <span>{t("ui.data_h") || "Satellite & Data Telemetry"}</span>
          </div>

          <div className="space-y-2">
            {context.sources.map((src) => {
              const isOk = src.status === "ok";
              const isMiss = src.status === "miss";

              return (
                <div
                  key={src.name}
                  className="flex items-center justify-between p-2 rounded-lg bg-white border border-[#E8E4DA] text-xs"
                >
                  <div className="flex items-center gap-2">
                    {isOk ? (
                      <CheckCircle2 className="w-4 h-4 text-[#2F6B45] shrink-0" />
                    ) : isMiss ? (
                      <AlertCircle className="w-4 h-4 text-[#C84B31] shrink-0" />
                    ) : (
                      <HelpCircle className="w-4 h-4 text-[#8C9B8E] shrink-0" />
                    )}
                    <div>
                      <div className="font-semibold text-[#1A3324]">{src.name}</div>
                      <div className="text-[10px] text-[#7B8A7C]">{src.date_range}</div>
                    </div>
                  </div>

                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      isOk
                        ? "bg-[#EBF3ED] text-[#2F6B45]"
                        : isMiss
                        ? "bg-[#FDF0ED] text-[#C84B31]"
                        : "bg-[#F0EFEB] text-[#7B8A7C]"
                    }`}
                  >
                    {isOk ? "Active" : isMiss ? "Unavailable" : "N/A"}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
