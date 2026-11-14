"use client";

import React from "react";
import { Compass, MapPin } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";
import type { DemoFieldItem } from "@/types";

interface LocationBarProps {
  demoFields: Record<string, DemoFieldItem>;
}

export default function LocationBar({ demoFields }: LocationBarProps) {
  const { t, language } = useTranslation();
  const fieldChoice = useAppStore((s) => s.fieldChoice);
  const lat = useAppStore((s) => s.lat);
  const lon = useAppStore((s) => s.lon);
  const selectField = useAppStore((s) => s.selectField);
  const setCoordinates = useAppStore((s) => s.setCoordinates);

  const handleSelectField = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const key = e.target.value;
    if (key === "own") {
      setCoordinates(lat, lon);
    } else {
      const f = demoFields[key];
      if (f) {
        selectField(f.key, f.name, f.lat, f.lon, f.rotation);
      }
    }
  };

  const getFieldLabel = (key: string, name: string) => {
    if (key === "own") return t("side.own") || "My own location";
    const trKey = `field.${key}`;
    const translated = t(trKey);
    return translated !== trKey ? translated : name;
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E3DFD3] p-3.5 shadow-xs">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
        {/* Preset Selector */}
        <div className="md:col-span-6">
          <label className="block text-xs font-semibold text-[#526356] mb-1.5 flex items-center gap-1.5">
            <Compass className="w-3.5 h-3.5 text-[#2F6B45]" />
            <span>{t("ui.field_label") || "Target Farmland Location"}</span>
          </label>
          <div className="relative">
            <select
              value={fieldChoice}
              onChange={handleSelectField}
              className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-[#1A3324] text-sm rounded-xl px-3 py-2 pr-8 font-medium focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45] cursor-pointer"
            >
              {Object.entries(demoFields).map(([key, f]) => (
                <option key={key} value={key}>
                  {getFieldLabel(key, f.name)}
                </option>
              ))}
              <option value="own">
                {t("side.own") || "My own location (coordinates below)"}
              </option>
            </select>
          </div>
        </div>

        {/* Latitude */}
        <div className="md:col-span-3">
          <label className="block text-xs font-semibold text-[#526356] mb-1.5 flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-[#2F6B45]" />
            <span>{t("side.lat") || "Latitude (°N/S)"}</span>
          </label>
          <input
            type="number"
            step="0.01"
            min="-60"
            max="70"
            value={lat}
            onChange={(e) => setCoordinates(parseFloat(e.target.value) || 0, lon)}
            className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-[#1A3324] text-sm rounded-xl px-3 py-2 font-mono font-medium focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45]"
          />
        </div>

        {/* Longitude */}
        <div className="md:col-span-3">
          <label className="block text-xs font-semibold text-[#526356] mb-1.5 flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-[#2F6B45]" />
            <span>{t("side.lon") || "Longitude (°E/W)"}</span>
          </label>
          <input
            type="number"
            step="0.01"
            min="-180"
            max="180"
            value={lon}
            onChange={(e) => setCoordinates(lat, parseFloat(e.target.value) || 0)}
            className="w-full bg-[#FAF9F5] border border-[#D5D0C5] text-[#1A3324] text-sm rounded-xl px-3 py-2 font-mono font-medium focus:outline-none focus:ring-2 focus:ring-[#2F6B45]/20 focus:border-[#2F6B45]"
          />
        </div>
      </div>
    </div>
  );
}
