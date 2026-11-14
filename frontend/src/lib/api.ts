import type {
  ConfigResponse,
  ContextResponse,
  EvaluateResponse,
  GibsLayerItem,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";

export async function fetchConfig(): Promise<ConfigResponse> {
  const res = await fetch(`${BASE_URL}/api/config`);
  if (!res.ok) {
    throw new Error(`Failed to fetch config: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchContext(
  lat: number,
  lon: number,
  rainPct: number = 0,
  tempC: number = 0.0
): Promise<ContextResponse> {
  const res = await fetch(`${BASE_URL}/api/context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      lat,
      lon,
      rain_pct: rainPct,
      temp_c: tempC,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Failed to fetch climate context");
  }
  return res.json();
}

export async function fetchEvaluateRotations(
  lat: number,
  lon: number,
  rainPct: number,
  tempC: number,
  currentCrops: string[],
  irrigationSupply: number,
  weights: Record<string, number>
): Promise<EvaluateResponse> {
  const res = await fetch(`${BASE_URL}/api/rotations/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      lat,
      lon,
      rain_pct: rainPct,
      temp_c: tempC,
      current_crops: currentCrops,
      irrigation_supply: irrigationSupply,
      weights,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Failed to evaluate rotations");
  }
  return res.json();
}

export async function fetchGibsLayers(): Promise<GibsLayerItem[]> {
  const res = await fetch(`${BASE_URL}/api/layers/gibs`);
  if (!res.ok) {
    throw new Error(`Failed to fetch GIBS layers: ${res.statusText}`);
  }
  return res.json();
}
