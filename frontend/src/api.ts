/** Minimal API client. Falls back to returning null when the backend is unreachable. */

const API_BASE = "http://127.0.0.1:8000";

export type TrialAssignment = {
  trial_id: string;
  trial_index: number;
  face_id: string;
  image_url: string;
};

export type SessionResult = {
  session_id: string;
  assigned_trials: TrialAssignment[];
};

async function post<T>(path: string, body: unknown): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export async function createSession(
  participantAge: number,
  participantGender: string,
  experimentVersion: string,
  hasChildExposure: boolean | null,
  childAgeBins: string[],
): Promise<SessionResult | null> {
  return post<SessionResult>("/api/session", {
    participant_age: participantAge,
    participant_gender: participantGender,
    experiment_version: experimentVersion,
    has_child_exposure: hasChildExposure,
    child_age_bins: childAgeBins,
    device_type: window.matchMedia("(max-width: 700px)").matches ? "mobile" : "desktop",
  });
}

export async function submitResponse(
  sessionId: string,
  trialId: string,
  faceId: string,
  predictedAge: number,
  responseTimeMs: number,
  clientOrderIndex: number,
): Promise<boolean> {
  const res = await post<{ ok: boolean }>("/api/response", {
    session_id: sessionId,
    trial_id: trialId,
    face_id: faceId,
    predicted_age: predictedAge,
    response_time_ms: responseTimeMs,
    client_order_index: clientOrderIndex,
  });
  return res?.ok === true;
}

export async function completeSession(sessionId: string): Promise<boolean> {
  const res = await post<{ ok: boolean }>("/api/session/complete", {
    session_id: sessionId,
  });
  return res?.ok === true;
}

export async function fetchAnalytics(): Promise<Record<string, unknown> | null> {
  try {
    const res = await fetch(`${API_BASE}/api/analytics`);
    if (!res.ok) return null;
    return (await res.json()) as Record<string, unknown>;
  } catch {
    return null;
  }
}
