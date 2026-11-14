"use client";

import React from "react";
import { MapPin, SlidersHorizontal, BookOpen } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { useTranslation } from "@/lib/i18n";

export default function ViewTabs() {
  const view = useAppStore((s) => s.view);
  const setView = useAppStore((s) => s.setView);
  const { t } = useTranslation();

  const tabs = [
    {
      id: "field" as const,
      label: t("view.field") || "Your Field",
      icon: MapPin,
    },
    {
      id: "options" as const,
      label: t("view.options") || "Rotation Options",
      icon: SlidersHorizontal,
    },
    {
      id: "glossary" as const,
      label: t("view.glossary") || "Glossary & Data",
      icon: BookOpen,
    },
  ];

  return (
    <nav className="flex items-center gap-1.5 p-1 bg-[#EDEBE4] rounded-xl border border-[#DEDAD1]">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = view === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setView(tab.id)}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer ${
              isActive
                ? "bg-white text-[#1A3324] shadow-sm border border-[#D5D0C5]"
                : "text-[#586358] hover:text-[#1A3324] hover:bg-[#E5E2D9]"
            }`}
          >
            <Icon className={`w-3.5 h-3.5 ${isActive ? "text-[#2F6B45]" : "text-[#7B8A7C]"}`} />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
