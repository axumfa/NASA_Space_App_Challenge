"use client";

import React, { useState } from "react";
import { BookOpen, Database, Search, ChevronDown, ChevronUp } from "lucide-react";
import { useTranslation } from "@/lib/i18n";

interface GlossaryViewProps {
  glossary: [string, string, string][];
}

export default function GlossaryView({ glossary }: GlossaryViewProps) {
  const { t, language } = useTranslation();
  const [search, setSearch] = useState("");
  const [openItems, setOpenItems] = useState<Record<string, boolean>>({
    et0: true,
    gdd: true,
  });

  const toggleItem = (gid: string) => {
    setOpenItems((prev) => ({ ...prev, [gid]: !prev[gid] }));
  };

  const filtered = glossary.filter(([gid]) => {
    const title = t(`gl.${gid}.t`) || gid;
    const desc = t(`gl.${gid}.d`) || "";
    const q = search.toLowerCase();
    return title.toLowerCase().includes(q) || desc.toLowerCase().includes(q);
  });

  const sources = [
    {
      source: "NASA POWER (MERRA-2, CERES-SYN)",
      usage: t("g.power_for") || "Daily radiation, temperature, rainfall, wind, humidity",
      res: t("g.power_res") || "0.5° × 0.625°",
      period: "2001–2025",
      status: t("g.used") || "Used directly",
    },
    {
      source: "ISRIC SoilGrids",
      usage: t("g.soil_for") || "Physical and chemical soil parameters (0–30 cm)",
      res: "250 m",
      period: t("g.static") || "Static map",
      status: t("g.soil_status") || "REST API / fallback",
    },
    {
      source: "MODIS NDVI (MOD13Q1)",
      usage: t("g.ndvi_for") || "Vegetation index for crop greenness and bare windows",
      res: t("g.res_ndvi") || "250 m (16-day)",
      period: "2015–present",
      status: t("g.ndvi_used") || "Used where available",
    },
    {
      source: "SMAP Radiometer",
      usage: t("g.smap_for") || "Surface soil moisture active/passive radar",
      res: "~9 km",
      period: "2015–present",
      status: t("g.smap_used") || "Used where available",
    },
    {
      source: "GPM IMERG / SRTM",
      usage: t("g.other_for") || "Precipitation calibration and digital elevation model",
      res: "10 km / 30 m",
      period: "–",
      status: t("g.not_yet") || "Planned expansion",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="bg-white rounded-2xl border border-[#E3DFD3] p-5 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-[#2F6B45]" />
            <h3 className="text-base font-bold text-[#1A3324]">
              {t("g.title") || "Agronomic Glossary & NASA Data Science Definitions"}
            </h3>
          </div>

          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-[#7B8A7C] absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search concepts..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-xs rounded-xl pl-8 pr-3 py-1.5 text-[#1A3324] placeholder-[#7B8A7C] focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45]"
            />
          </div>
        </div>

        {/* Glossary Accordions */}
        <div className="space-y-2">
          {filtered.map(([gid]) => {
            const isOpen = !!openItems[gid];
            const title = t(`gl.${gid}.t`) || gid;
            const desc = t(`gl.${gid}.d`) || "";

            return (
              <div
                key={gid}
                className="border border-[#EAE6DC] rounded-xl overflow-hidden"
              >
                <button
                  onClick={() => toggleItem(gid)}
                  className="w-full p-3 bg-[#FAF9F5] flex items-center justify-between text-left text-xs font-bold text-[#1A3324] hover:bg-[#F2EFE8] transition-colors cursor-pointer"
                >
                  <span>{title}</span>
                  {isOpen ? (
                    <ChevronUp className="w-3.5 h-3.5 text-[#7B8A7C]" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-[#7B8A7C]" />
                  )}
                </button>
                {isOpen && (
                  <div className="p-3.5 bg-white text-xs text-[#4E5E50] leading-relaxed border-t border-[#EAE6DC]">
                    {desc}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* NASA Data Sources Table */}
      <div className="bg-white rounded-2xl border border-[#E3DFD3] p-5 shadow-xs overflow-x-auto">
        <div className="flex items-center gap-2 mb-3">
          <Database className="w-4 h-4 text-[#2F6B45]" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#1A3324]">
            {t("g.data") || "NASA & SoilGrids Data Provenance"}
          </h4>
        </div>

        <table className="w-full text-xs text-left border-collapse min-w-[600px]">
          <thead>
            <tr className="border-b border-[#E3DFD3] bg-[#FAF9F5]">
              <th className="py-2.5 px-3 font-semibold text-[#526356]">
                {t("g.col_source") || "Data Source"}
              </th>
              <th className="py-2.5 px-3 font-semibold text-[#526356]">
                {t("g.col_for") || "Parameters Measured"}
              </th>
              <th className="py-2.5 px-3 font-semibold text-[#526356]">
                {t("g.col_res") || "Resolution"}
              </th>
              <th className="py-2.5 px-3 font-semibold text-[#526356]">
                {t("g.col_period") || "Temporal Span"}
              </th>
              <th className="py-2.5 px-3 font-semibold text-[#526356]">
                {t("g.col_status") || "Integration Status"}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#EAE6DC]">
            {sources.map((s, idx) => (
              <tr key={idx} className="hover:bg-[#FAF9F5]/50">
                <td className="py-2.5 px-3 font-bold text-[#1A3324]">{s.source}</td>
                <td className="py-2.5 px-3 text-[#4E5E50]">{s.usage}</td>
                <td className="py-2.5 px-3 font-mono text-[#667568]">{s.res}</td>
                <td className="py-2.5 px-3 font-mono text-[#667568]">{s.period}</td>
                <td className="py-2.5 px-3">
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#EBF3ED] text-[#2F6B45]">
                    {s.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
