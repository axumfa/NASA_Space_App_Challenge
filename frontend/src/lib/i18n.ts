import { useAppStore } from "./store";

function formatParam(value: any, spec?: string): string {
  if (value === undefined || value === null) return "";
  if (typeof value === "number" && spec) {
    const match = spec.match(/([+])?(?:\.(\d+))?([fd])?/);
    if (match) {
      const showSign = match[1] === "+";
      const decimals = match[2] !== undefined ? parseInt(match[2], 10) : undefined;
      let formatted: string;
      if (decimals !== undefined) {
        formatted = value.toFixed(decimals);
      } else if (match[3] === "d") {
        formatted = Math.round(value).toString();
      } else {
        formatted = String(value);
      }
      if (showSign && value > 0) {
        formatted = `+${formatted}`;
      }
      return formatted;
    }
  }
  return String(value);
}

export function useTranslation() {
  const language = useAppStore((s) => s.language);
  const translations = useAppStore((s) => s.translations);

  const t = (key: string, params?: Record<string, string | number>): string => {
    const entry = translations[key];
    if (!entry) return key;

    let text = language === "uz" ? (entry.uz || entry.en) : entry.en;
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        const regex = new RegExp(`\\{${k}(?::([^}]+))?\\}`, "g");
        text = text.replace(regex, (_, spec) => formatParam(v, spec));
      }
    }
    return text;
  };

  return { t, language };
}
