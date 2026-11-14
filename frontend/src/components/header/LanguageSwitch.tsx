"use client";

import React from "react";
import { Globe } from "lucide-react";
import { useAppStore } from "@/lib/store";

export default function LanguageSwitch() {
  const language = useAppStore((s) => s.language);
  const setLanguage = useAppStore((s) => s.setLanguage);

  return (
    <div className="flex items-center gap-1.5 p-1 bg-[#EDEBE4] rounded-xl border border-[#DEDAD1]">
      <div className="pl-2 pr-1 text-[#667568]">
        <Globe className="w-3.5 h-3.5" />
      </div>
      <button
        onClick={() => setLanguage("en")}
        className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
          language === "en"
            ? "bg-white text-[#1A3324] shadow-sm border border-[#D5D0C5]"
            : "text-[#586358] hover:text-[#1A3324]"
        }`}
      >
        English
      </button>
      <button
        onClick={() => setLanguage("uz")}
        className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
          language === "uz"
            ? "bg-white text-[#1A3324] shadow-sm border border-[#D5D0C5]"
            : "text-[#586358] hover:text-[#1A3324]"
        }`}
      >
        O'zbekcha
      </button>
    </div>
  );
}
