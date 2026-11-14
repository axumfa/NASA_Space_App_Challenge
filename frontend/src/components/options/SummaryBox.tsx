"use client";

import React from "react";
import { Award, AlertTriangle, CheckCircle, Info } from "lucide-react";
import { useTranslation } from "@/lib/i18n";
import type { EvaluateResponse } from "@/types";

interface SummaryBoxProps {
  summaryBox: EvaluateResponse["summary_box"];
}

export default function SummaryBox({ summaryBox }: SummaryBoxProps) {
  const { language } = useTranslation();

  const title = language === "uz" ? summaryBox.title_uz : summaryBox.title_en;
  const best = language === "uz" ? summaryBox.best_uz : summaryBox.best_en;
  const reason = language === "uz" ? summaryBox.reason_uz : summaryBox.reason_en;
  const tradeoff = language === "uz" ? summaryBox.tradeoff_uz : summaryBox.tradeoff_en;
  const check = language === "uz" ? summaryBox.check_uz : summaryBox.check_en;
  const caveat = language === "uz" ? summaryBox.caveat_uz : summaryBox.caveat_en;

  return (
    <div className="bg-[#FAFDFB] rounded-2xl border border-[#CCE0D1] p-5 shadow-xs space-y-3">
      <div className="flex items-center gap-2">
        <div className="w-7 h-7 rounded-lg bg-[#2F6B45] text-white flex items-center justify-center shrink-0">
          <Award className="w-4 h-4" />
        </div>
        <h3 className="text-base font-bold text-[#1A3324]">{title}</h3>
      </div>

      <div className="space-y-2 text-xs text-[#38453A] leading-relaxed">
        <div className="flex items-start gap-2">
          <CheckCircle className="w-4 h-4 text-[#2F6B45] shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-[#1A3324]">Recommended: </span>
            {best}
          </div>
        </div>

        <div className="flex items-start gap-2">
          <Info className="w-4 h-4 text-[#3A6EA5] shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-[#1A3324]">Why it fits: </span>
            {reason}
          </div>
        </div>

        {tradeoff && (
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-[#D97706] shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-[#1A3324]">Trade-off: </span>
              {tradeoff}
            </div>
          </div>
        )}

        {check && (
          <div className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-[#2F6B45] shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-[#1A3324]">Check locally: </span>
              {check}
            </div>
          </div>
        )}
      </div>

      {caveat && (
        <div className="pt-2 border-t border-[#CCE0D1]/60 text-[11px] text-[#7B8A7C] italic">
          {caveat}
        </div>
      )}
    </div>
  );
}
