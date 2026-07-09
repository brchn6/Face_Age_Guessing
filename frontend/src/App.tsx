import { FormEvent, useEffect, useMemo, useState } from "react";

const EXPERIMENT_VERSION = "mvp_003";
const TRIAL_COUNT = 10;
const LATEST_RESULT_STORAGE_KEY = "face_age_guessing_latest_result";
const MOCK_FACE_CREATED_AT = "2026-07-09T00:00:00.000Z";

const GENDER_VALUES = ["female", "male", "other", "prefer_not_to_say"] as const;
const CHILD_AGE_BINS = ["0-2", "3-5", "6-8", "9-12", "13-17", "18+"] as const;

type Language = "en" | "he";
type Screen = "landing" | "consent" | "details" | "childExposure" | "trial" | "thanks" | "dashboard";
type ParticipantGender = (typeof GENDER_VALUES)[number];
type ChildAgeBin = (typeof CHILD_AGE_BINS)[number];
type ChildExposureChoice = "no" | "yes" | "prefer_not_to_say";
type FaceGender = "female" | "male" | "other" | "unknown";
type SessionStatus = "created" | "active" | "completed" | "abandoned" | "invalid";
type DetailsError = "age" | "gender" | "";
type ChildExposureError = "choice" | "bins" | "";
type GuessError = "guess" | "";

type TextBundle = {
  languageToggleLabel: string;
  english: string;
  hebrew: string;
  consoleLabel: string;
  landingEyebrow: string;
  landingTitle: string;
  landingCopy: string;
  landingTime: string;
  countdown: {
    landing: string;
    consent: string;
    detailsDefault: string;
    detailsAdult: string;
    childExposure: string;
  };
  start: string;
  consentEyebrow: string;
  consentTitle: string;
  consentCopy: string[];
  continue: string;
  detailsEyebrow: string;
  detailsTitle: string;
  ageLabel: string;
  agePlaceholder: string;
  genderLabel: string;
  chooseOne: string;
  genderOptions: Record<ParticipantGender, string>;
  childExposureEyebrow: string;
  childExposureTitle: string;
  childExposureQuestion: string;
  childExposureOptions: Record<ChildExposureChoice, string>;
  childAgeBinsQuestion: string;
  startGuessing: string;
  imageAlt: string;
  trialQuestion: string;
  trialHint: string;
  decreaseGuess: string;
  increaseGuess: string;
  guessedAge: string;
  guessMicrocopy: string;
  finish: string;
  completeEyebrow: string;
  thankYouTitle: string;
  thankYouCopy: string;
  continuePrompt: string;
  doTenMore: string;
  dashboardLink: string;
  dashboardEyebrow: string;
  dashboardTitle: string;
  dashboardCopy: string;
  noRecentResult: string;
  backToThanks: string;
  sessionIdLabel: string;
  statusLabel: string;
  completedAtLabel: string;
  averageResponseTimeLabel: string;
  latestResponsesLabel: string;
  orderLabel: string;
  faceIdLabel: string;
  guessedAgeLabel: string;
  responseTimeLabel: string;
  finalJsonOutput: string;
  responsesLabel: string;
  errors: {
    detailsAge: string;
    detailsGender: string;
    childExposureChoice: string;
    childAgeBins: string;
    guess: string;
  };
};

type FaceImage = {
  face_id: string;
  image_url: string;
  true_age: number;
  true_age_bin: string;
  face_gender: FaceGender;
  source_dataset: string;
  license_type: string;
  is_active: boolean;
  quality_score: number;
  created_at: string;
};

type ParticipantSession = {
  session_id: string;
  participant_age: number;
  participant_age_group: string;
  participant_gender: ParticipantGender;
  has_child_exposure: boolean | null;
  experiment_version: string;
  device_type: "mobile" | "desktop";
  started_at: string;
  completed_at: string | null;
  status: SessionStatus;
};

type ParticipantChildExposure = {
  session_id: string;
  child_age_bin: ChildAgeBin;
};

type TrialAssignment = {
  trial_id: string;
  session_id: string;
  face_id: string;
  trial_index: number;
  assigned_at: string;
};

type TrialResponse = {
  response_id: string;
  trial_id: string;
  session_id: string;
  face_id: string;
  predicted_age: number;
  response_time_ms: number;
  submitted_at: string;
  client_order_index: number;
};

type ExperimentOutput = {
  experiment_version: string;
  participant_sessions: ParticipantSession;
  participant_child_exposure: ParticipantChildExposure[];
  face_images: FaceImage[];
  trial_assignments: TrialAssignment[];
  responses: TrialResponse[];
};

const TEXT: Record<Language, TextBundle> = {
  en: {
    languageToggleLabel: "Language",
    english: "English",
    hebrew: "עברית",
    consoleLabel: "Face Age Guessing MVP output",
    landingEyebrow: "Anonymous research game",
    landingTitle: "Guess Their Age",
    landingCopy: "You’ll see 10 face images. For each one, guess how old the person is.",
    landingTime: "It takes less than a minute.",
    countdown: {
      landing: "Game starts after 2 quick steps.",
      consent: "2 quick steps before the game.",
      detailsDefault: "1 quick step before the game.",
      detailsAdult: "After this, just 1 short question before the game.",
      childExposure: "Last question — the game starts next.",
    },
    start: "Start",
    consentEyebrow: "Before you start",
    consentTitle: "Quick note",
    consentCopy: [
      "This is an anonymous research experiment about how people estimate age from faces.",
      "We do not ask for your name, email, or account.",
      "You can stop at any time.",
    ],
    continue: "Continue",
    detailsEyebrow: "About you",
    detailsTitle: "Two details",
    ageLabel: "Age",
    agePlaceholder: "Enter age",
    genderLabel: "Gender",
    chooseOne: "Choose one",
    genderOptions: {
      female: "Female",
      male: "Male",
      other: "Other",
      prefer_not_to_say: "Prefer not to say",
    },
    childExposureEyebrow: "One short question",
    childExposureTitle: "Regular contact",
    childExposureQuestion: "Are there children you are in close regular contact with?",
    childExposureOptions: {
      no: "No",
      yes: "Yes",
      prefer_not_to_say: "Prefer not to say",
    },
    childAgeBinsQuestion: "Which age ranges? Select all that apply.",
    startGuessing: "Start guessing",
    imageAlt: "Face for age guessing",
    trialQuestion: "How old is this person?",
    trialHint: "Not sure? Make your best guess.",
    decreaseGuess: "Decrease guess by one year",
    increaseGuess: "Increase guess by one year",
    guessedAge: "Guessed age",
    guessMicrocopy: "Slide to choose an age. Use − / + to fine-tune.",
    finish: "Finish",
    completeEyebrow: "Complete",
    thankYouTitle: "Thank you",
    thankYouCopy: "Your 10 guesses were recorded in this local prototype.",
    continuePrompt: "Want to do 10 more? It starts right away with a fresh 10-image session.",
    doTenMore: "Do 10 more",
    dashboardLink: "View recent result dashboard",
    dashboardEyebrow: "Local dashboard",
    dashboardTitle: "Most recent result",
    dashboardCopy: "This local prototype dashboard shows the most recent completed session in this browser.",
    noRecentResult: "No completed result found yet.",
    backToThanks: "Back to thank you",
    sessionIdLabel: "Session",
    statusLabel: "Status",
    completedAtLabel: "Completed",
    averageResponseTimeLabel: "Average response time",
    latestResponsesLabel: "Latest responses",
    orderLabel: "#",
    faceIdLabel: "Face ID",
    guessedAgeLabel: "Guess",
    responseTimeLabel: "Time",
    finalJsonOutput: "Dashboard JSON preview",
    responsesLabel: "responses",
    errors: {
      detailsAge: "Enter an age from 4 to 100.",
      detailsGender: "Choose a gender option.",
      childExposureChoice: "Choose one option.",
      childAgeBins: "Select at least one age range.",
      guess: "Enter a whole-number age from 1 to 100.",
    },
  },
  he: {
    languageToggleLabel: "שפה",
    english: "English",
    hebrew: "עברית",
    consoleLabel: "פלט אבטיפוס ניחוש גיל לפי פנים",
    landingEyebrow: "משחק מחקר אנונימי",
    landingTitle: "נחשו את הגיל",
    landingCopy: "יוצגו לכם 10 תמונות פנים. בכל תמונה, נחשו בן/בת כמה האדם.",
    landingTime: "זה לוקח פחות מדקה.",
    countdown: {
      landing: "המשחק מתחיל אחרי 2 שלבים קצרים.",
      consent: "עוד 2 שלבים קצרים לפני המשחק.",
      detailsDefault: "עוד שלב קצר אחד לפני המשחק.",
      detailsAdult: "אחרי זה רק עוד שאלה קצרה אחת לפני המשחק.",
      childExposure: "שאלה אחרונה — המשחק מתחיל מיד אחריה.",
    },
    start: "התחלה",
    consentEyebrow: "לפני שמתחילים",
    consentTitle: "הערה קצרה",
    consentCopy: [
      "זהו ניסוי מחקר אנונימי על האופן שבו אנשים מעריכים גיל לפי פנים.",
      "לא נבקש שם, אימייל או חשבון.",
      "אפשר להפסיק בכל שלב.",
    ],
    continue: "המשך",
    detailsEyebrow: "עליך",
    detailsTitle: "שני פרטים",
    ageLabel: "גיל",
    agePlaceholder: "הזנת גיל",
    genderLabel: "מגדר",
    chooseOne: "בחרו אפשרות",
    genderOptions: {
      female: "אישה",
      male: "גבר",
      other: "אחר",
      prefer_not_to_say: "מעדיף/ה לא לומר",
    },
    childExposureEyebrow: "שאלה קצרה אחת",
    childExposureTitle: "קשר קבוע",
    childExposureQuestion: "האם יש ילדים שאתם בקשר קרוב וקבוע איתם?",
    childExposureOptions: {
      no: "לא",
      yes: "כן",
      prefer_not_to_say: "מעדיף/ה לא לומר",
    },
    childAgeBinsQuestion: "אילו טווחי גיל? אפשר לבחור יותר מאחד.",
    startGuessing: "להתחיל לנחש",
    imageAlt: "פנים לניחוש גיל",
    trialQuestion: "בן/בת כמה האדם הזה?",
    trialHint: "לא בטוחים? נחשו כמיטב יכולתכם.",
    decreaseGuess: "להקטין את הניחוש בשנה אחת",
    increaseGuess: "להגדיל את הניחוש בשנה אחת",
    guessedAge: "גיל משוער",
    guessMicrocopy: "הזיזו את הסליידר כדי לבחור גיל. השתמשו ב־− / + לכוונון.",
    finish: "סיום",
    completeEyebrow: "הושלם",
    thankYouTitle: "תודה",
    thankYouCopy: "10 הניחושים נשמרו באבטיפוס המקומי הזה.",
    continuePrompt: "רוצים לעשות עוד 10? זה מתחיל מיד עם סשן חדש של 10 תמונות.",
    doTenMore: "עוד 10 ניחושים",
    dashboardLink: "צפייה בדשבורד התוצאה האחרונה",
    dashboardEyebrow: "דשבורד מקומי",
    dashboardTitle: "התוצאה האחרונה",
    dashboardCopy: "דשבורד האבטיפוס המקומי מציג את הסשן האחרון שהושלם בדפדפן הזה.",
    noRecentResult: "עדיין אין תוצאה שהושלמה.",
    backToThanks: "חזרה למסך התודה",
    sessionIdLabel: "סשן",
    statusLabel: "סטטוס",
    completedAtLabel: "הושלם",
    averageResponseTimeLabel: "זמן תגובה ממוצע",
    latestResponsesLabel: "התשובות האחרונות",
    orderLabel: "#",
    faceIdLabel: "מזהה פנים",
    guessedAgeLabel: "ניחוש",
    responseTimeLabel: "זמן",
    finalJsonOutput: "תצוגת JSON לדשבורד",
    responsesLabel: "תשובות",
    errors: {
      detailsAge: "הזינו גיל בין 4 ל־100.",
      detailsGender: "בחרו אפשרות מגדר.",
      childExposureChoice: "בחרו אפשרות אחת.",
      childAgeBins: "בחרו לפחות טווח גיל אחד.",
      guess: "הזינו גיל במספר שלם בין 1 ל־100.",
    },
  },
};

function makeMockFaceSvg(seed: number, skin: string, hair: string, shirt: string): string {
  const eyebrowOffset = seed % 2 === 0 ? 0 : 4;
  const smile = seed % 3 === 0 ? "M122 162 Q150 178 178 162" : "M124 164 Q150 170 176 164";
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 360" role="img">
      <defs>
        <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0" stop-color="#eef2ff" />
          <stop offset="1" stop-color="#f8fafc" />
        </linearGradient>
      </defs>
      <rect width="300" height="360" rx="32" fill="url(#bg)" />
      <circle cx="150" cy="138" r="82" fill="${hair}" />
      <circle cx="150" cy="154" r="72" fill="${skin}" />
      <path d="M82 138 Q150 48 218 138 Q190 86 150 82 Q110 86 82 138Z" fill="${hair}" />
      <circle cx="125" cy="148" r="7" fill="#111827" />
      <circle cx="175" cy="148" r="7" fill="#111827" />
      <path d="M112 ${132 + eyebrowOffset} Q125 ${126 + eyebrowOffset} 138 ${132 + eyebrowOffset}" fill="none" stroke="#111827" stroke-width="5" stroke-linecap="round" />
      <path d="M162 ${132 - eyebrowOffset} Q175 ${126 - eyebrowOffset} 188 ${132 - eyebrowOffset}" fill="none" stroke="#111827" stroke-width="5" stroke-linecap="round" />
      <path d="M150 153 Q144 172 158 172" fill="none" stroke="#9f6b53" stroke-width="5" stroke-linecap="round" />
      <path d="${smile}" fill="none" stroke="#991b1b" stroke-width="5" stroke-linecap="round" />
      <path d="M70 344 Q86 238 150 238 Q214 238 230 344Z" fill="${shirt}" />
    </svg>`;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

const MOCK_FACE_IMAGES: FaceImage[] = [
  ["face_mock_01", 5, "4-6", "unknown", "#f4c7a1", "#7c2d12", "#6366f1"],
  ["face_mock_02", 8, "7-9", "unknown", "#e9b98f", "#3f2a1d", "#0ea5e9"],
  ["face_mock_03", 11, "10-12", "unknown", "#c98f68", "#111827", "#10b981"],
  ["face_mock_04", 15, "13-17", "unknown", "#f1c39f", "#92400e", "#f59e0b"],
  ["face_mock_05", 22, "18-24", "unknown", "#d8a47f", "#1f2937", "#ef4444"],
  ["face_mock_06", 29, "25-31", "unknown", "#8d5b3f", "#111827", "#8b5cf6"],
  ["face_mock_07", 35, "32-38", "unknown", "#f0b98d", "#4b5563", "#14b8a6"],
  ["face_mock_08", 42, "39-45", "unknown", "#b77955", "#374151", "#f97316"],
  ["face_mock_09", 49, "46-52", "unknown", "#e0aa7c", "#6b7280", "#2563eb"],
  ["face_mock_10", 58, "53-60", "unknown", "#c9926b", "#9ca3af", "#64748b"],
].map(([face_id, true_age, true_age_bin, face_gender, skin, hair, shirt], index) => ({
  face_id: String(face_id),
  image_url: makeMockFaceSvg(index + 1, String(skin), String(hair), String(shirt)),
  true_age: Number(true_age),
  true_age_bin: String(true_age_bin),
  face_gender: face_gender as FaceGender,
  source_dataset: "internal_mock_svg_placeholders",
  license_type: "internal_mock_only_not_research_data",
  is_active: true,
  quality_score: 1,
  created_at: MOCK_FACE_CREATED_AT,
}));

function createId(prefix: string): string {
  return `${prefix}_${crypto.randomUUID()}`;
}

function getParticipantAgeGroup(age: number): string {
  if (age <= 12) return "4-12";
  if (age <= 17) return "13-17";
  if (age <= 24) return "18-24";
  if (age <= 34) return "25-34";
  if (age <= 44) return "35-44";
  if (age <= 54) return "45-54";
  if (age <= 64) return "55-64";
  return "65+";
}

function getDeviceType(): "mobile" | "desktop" {
  return window.matchMedia("(max-width: 700px)").matches ? "mobile" : "desktop";
}

function parseInteger(value: string): number | null {
  if (!/^\d+$/.test(value.trim())) return null;
  return Number(value);
}

function shuffle<T>(items: T[]): T[] {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}

function getDirection(language: Language): "ltr" | "rtl" {
  return language === "he" ? "rtl" : "ltr";
}

function readLatestResult(): ExperimentOutput | null {
  try {
    const stored = window.localStorage.getItem(LATEST_RESULT_STORAGE_KEY);
    return stored ? (JSON.parse(stored) as ExperimentOutput) : null;
  } catch {
    return null;
  }
}

function saveLatestResult(result: ExperimentOutput): void {
  try {
    window.localStorage.setItem(LATEST_RESULT_STORAGE_KEY, JSON.stringify(result));
  } catch {
    // Local storage is best-effort only in the frontend prototype.
  }
}

function getAverageResponseTimeMs(responses: TrialResponse[]): number {
  if (responses.length === 0) return 0;
  return Math.round(
    responses.reduce((total, response) => total + response.response_time_ms, 0) / responses.length,
  );
}

function createDashboardPreview(result: ExperimentOutput) {
  return {
    experiment_version: result.experiment_version,
    participant_sessions: result.participant_sessions,
    participant_child_exposure: result.participant_child_exposure,
    trial_assignments: result.trial_assignments,
    responses: result.responses,
  };
}

export default function App() {
  const [language, setLanguage] = useState<Language>("en");
  const [screen, setScreen] = useState<Screen>("landing");
  const [participantAge, setParticipantAge] = useState("");
  const [participantGender, setParticipantGender] = useState<ParticipantGender | "">("");
  const [detailsError, setDetailsError] = useState<DetailsError>("");
  const [childExposureChoice, setChildExposureChoice] = useState<ChildExposureChoice | "">("");
  const [selectedChildBins, setSelectedChildBins] = useState<ChildAgeBin[]>([]);
  const [childExposureError, setChildExposureError] = useState<ChildExposureError>("");
  const [output, setOutput] = useState<ExperimentOutput | null>(null);
  const [latestResult, setLatestResult] = useState<ExperimentOutput | null>(null);
  const [currentTrialIndex, setCurrentTrialIndex] = useState(0);
  const [guess, setGuess] = useState("");
  const [trialStartedAt, setTrialStartedAt] = useState<number | null>(null);
  const [guessError, setGuessError] = useState<GuessError>("");

  const text = TEXT[language];
  const direction = getDirection(language);
  const parsedParticipantAge = parseInteger(participantAge);
  const detailsCountdown =
    parsedParticipantAge !== null && parsedParticipantAge >= 18
      ? text.countdown.detailsAdult
      : text.countdown.detailsDefault;
  const currentAssignment = output?.trial_assignments[currentTrialIndex] ?? null;
  const currentFace = currentAssignment
    ? output?.face_images.find((face) => face.face_id === currentAssignment.face_id) ?? null
    : null;
  const guessNumber = parseInteger(guess);
  const canSubmitGuess = guessNumber !== null && guessNumber >= 1 && guessNumber <= 100;

  const dashboardResult = output?.participant_sessions.status === "completed" ? output : latestResult;
  const dashboardAverageResponseTimeMs = dashboardResult
    ? getAverageResponseTimeMs(dashboardResult.responses)
    : 0;

  const dashboardJson = useMemo(() => {
    if (!dashboardResult) return "";
    return JSON.stringify(createDashboardPreview(dashboardResult), null, 2);
  }, [dashboardResult]);

  useEffect(() => {
    setLatestResult(readLatestResult());
    if (window.location.hash === "#dashboard") {
      setScreen("dashboard");
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = direction;
    document.title = text.landingTitle;
  }, [direction, language, text.landingTitle]);

  useEffect(() => {
    if (screen !== "trial" || !output) return;

    const nextAssignment = output.trial_assignments[currentTrialIndex + 1];
    if (!nextAssignment) return;

    const nextFace = output.face_images.find((face) => face.face_id === nextAssignment.face_id);
    if (!nextFace) return;

    const nextImage = new Image();
    nextImage.src = nextFace.image_url;
  }, [currentTrialIndex, output, screen]);

  function languageToggle() {
    return (
      <div className="language-toggle" role="group" aria-label={text.languageToggleLabel}>
        <button
          aria-pressed={language === "en"}
          className="language-option"
          type="button"
          onClick={() => setLanguage("en")}
        >
          {text.english}
        </button>
        <button
          aria-pressed={language === "he"}
          className="language-option"
          type="button"
          onClick={() => setLanguage("he")}
        >
          {text.hebrew}
        </button>
      </div>
    );
  }

  function startExperiment(
    age: number,
    gender: ParticipantGender,
    hasChildExposure: boolean | null,
    childAgeBins: ChildAgeBin[],
  ) {
    const sessionId = createId("session");
    const assignedAt = new Date().toISOString();
    const assignedFaces = shuffle(MOCK_FACE_IMAGES).slice(0, TRIAL_COUNT);
    const trialAssignments = assignedFaces.map((face, index) => ({
      trial_id: createId("trial"),
      session_id: sessionId,
      face_id: face.face_id,
      trial_index: index + 1,
      assigned_at: assignedAt,
    }));

    const nextOutput: ExperimentOutput = {
      experiment_version: EXPERIMENT_VERSION,
      participant_sessions: {
        session_id: sessionId,
        participant_age: age,
        participant_age_group: getParticipantAgeGroup(age),
        participant_gender: gender,
        has_child_exposure: hasChildExposure,
        experiment_version: EXPERIMENT_VERSION,
        device_type: getDeviceType(),
        started_at: assignedAt,
        completed_at: null,
        status: "active",
      },
      participant_child_exposure: childAgeBins.map((child_age_bin) => ({
        session_id: sessionId,
        child_age_bin,
      })),
      face_images: MOCK_FACE_IMAGES,
      trial_assignments: trialAssignments,
      responses: [],
    };

    setOutput(nextOutput);
    setCurrentTrialIndex(0);
    setGuess("");
    setGuessError("");
    setTrialStartedAt(Date.now());
    setScreen("trial");
  }

  function handleDetailsSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const age = parseInteger(participantAge);

    if (age === null || age < 4 || age > 100) {
      setDetailsError("age");
      return;
    }

    if (!participantGender) {
      setDetailsError("gender");
      return;
    }

    setDetailsError("");

    if (age >= 18) {
      setScreen("childExposure");
      return;
    }

    startExperiment(age, participantGender, null, []);
  }

  function handleChildExposureSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const age = parseInteger(participantAge);

    if (age === null || !participantGender) {
      setScreen("details");
      return;
    }

    if (!childExposureChoice) {
      setChildExposureError("choice");
      return;
    }

    if (childExposureChoice === "yes" && selectedChildBins.length === 0) {
      setChildExposureError("bins");
      return;
    }

    setChildExposureError("");
    startExperiment(
      age,
      participantGender,
      childExposureChoice === "yes" ? true : childExposureChoice === "no" ? false : null,
      childExposureChoice === "yes" ? selectedChildBins : [],
    );
  }

  function toggleChildBin(childAgeBin: ChildAgeBin) {
    setSelectedChildBins((current) =>
      current.includes(childAgeBin)
        ? current.filter((existingBin) => existingBin !== childAgeBin)
        : [...current, childAgeBin],
    );
  }

  function updateGuess(nextValue: number) {
    const clampedValue = Math.max(1, Math.min(100, nextValue));
    setGuess(String(clampedValue));
    setGuessError("");
  }

  function handleGuessSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!output || !currentAssignment || !currentFace || trialStartedAt === null) return;

    if (!canSubmitGuess || guessNumber === null) {
      setGuessError("guess");
      return;
    }

    const submittedAt = new Date().toISOString();
    const nextResponse: TrialResponse = {
      response_id: createId("response"),
      trial_id: currentAssignment.trial_id,
      session_id: output.participant_sessions.session_id,
      face_id: currentFace.face_id,
      predicted_age: guessNumber,
      response_time_ms: Date.now() - trialStartedAt,
      submitted_at: submittedAt,
      client_order_index: currentTrialIndex + 1,
    };

    const nextResponses = [...output.responses, nextResponse];
    const isFinalTrial = nextResponses.length === TRIAL_COUNT;
    const nextOutput: ExperimentOutput = {
      ...output,
      participant_sessions: {
        ...output.participant_sessions,
        completed_at: isFinalTrial ? submittedAt : output.participant_sessions.completed_at,
        status: isFinalTrial ? "completed" : output.participant_sessions.status,
      },
      responses: nextResponses,
    };

    setOutput(nextOutput);

    if (isFinalTrial) {
      saveLatestResult(nextOutput);
      setLatestResult(nextOutput);
      console.log(text.consoleLabel, nextOutput);
      setScreen("thanks");
      return;
    }

    setCurrentTrialIndex((current) => current + 1);
    setGuess("");
    setGuessError("");
    setTrialStartedAt(Date.now());
  }

  function handleDoTenMore() {
    if (!output) return;

    const childAgeBins = output.participant_child_exposure.map(
      (childExposure) => childExposure.child_age_bin,
    );

    startExperiment(
      output.participant_sessions.participant_age,
      output.participant_sessions.participant_gender,
      output.participant_sessions.has_child_exposure,
      childAgeBins,
    );
  }

  function openDashboard() {
    window.location.hash = "dashboard";
    setLatestResult(readLatestResult());
    setScreen("dashboard");
  }

  return (
    <main className="app-shell" dir={direction} lang={language}>
      {screen === "landing" && (
        <section className="card hero-card" aria-labelledby="landing-title">
          {languageToggle()}
          <p className="eyebrow">{text.landingEyebrow}</p>
          <h1 id="landing-title">{text.landingTitle}</h1>
          <p className="lede">{text.landingCopy}</p>
          <p className="time-note">{text.landingTime}</p>
          <p className="countdown-pill">{text.countdown.landing}</p>
          <button className="primary-button" type="button" onClick={() => setScreen("consent")}>
            {text.start}
          </button>
        </section>
      )}

      {screen === "consent" && (
        <section className="card" aria-labelledby="consent-title">
          {languageToggle()}
          <p className="eyebrow">{text.consentEyebrow}</p>
          <h1 id="consent-title">{text.consentTitle}</h1>
          <p className="countdown-pill">{text.countdown.consent}</p>
          <div className="copy-stack">
            {text.consentCopy.map((copy) => (
              <p key={copy}>{copy}</p>
            ))}
          </div>
          <button className="primary-button" type="button" onClick={() => setScreen("details")}>
            {text.continue}
          </button>
        </section>
      )}

      {screen === "details" && (
        <section className="card" aria-labelledby="details-title">
          {languageToggle()}
          <p className="eyebrow">{text.detailsEyebrow}</p>
          <h1 id="details-title">{text.detailsTitle}</h1>
          <p className="countdown-pill">{detailsCountdown}</p>
          <form className="form-stack" onSubmit={handleDetailsSubmit} noValidate>
            <label className="field-label" htmlFor="participant-age">
              {text.ageLabel}
              <input
                id="participant-age"
                className="text-input"
                inputMode="numeric"
                min="4"
                max="100"
                pattern="[0-9]*"
                placeholder={text.agePlaceholder}
                type="number"
                value={participantAge}
                onChange={(event) => {
                  setParticipantAge(event.target.value);
                  setDetailsError("");
                }}
              />
            </label>

            <label className="field-label" htmlFor="participant-gender">
              {text.genderLabel}
              <select
                id="participant-gender"
                className="text-input"
                value={participantGender}
                onChange={(event) => {
                  setParticipantGender(event.target.value as ParticipantGender | "");
                  setDetailsError("");
                }}
              >
                <option value="">{text.chooseOne}</option>
                {GENDER_VALUES.map((gender) => (
                  <option key={gender} value={gender}>
                    {text.genderOptions[gender]}
                  </option>
                ))}
              </select>
            </label>

            {detailsError && (
              <p className="error-text">
                {detailsError === "age" ? text.errors.detailsAge : text.errors.detailsGender}
              </p>
            )}

            <button className="primary-button" type="submit">
              {text.continue}
            </button>
          </form>
        </section>
      )}

      {screen === "childExposure" && (
        <section className="card" aria-labelledby="child-exposure-title">
          {languageToggle()}
          <p className="eyebrow">{text.childExposureEyebrow}</p>
          <h1 id="child-exposure-title">{text.childExposureTitle}</h1>
          <p className="countdown-pill">{text.countdown.childExposure}</p>
          <form className="form-stack" onSubmit={handleChildExposureSubmit} noValidate>
            <fieldset className="fieldset">
              <legend>{text.childExposureQuestion}</legend>
              <label className="choice-row">
                <input
                  checked={childExposureChoice === "no"}
                  name="child-exposure"
                  type="radio"
                  value="no"
                  onChange={() => {
                    setChildExposureChoice("no");
                    setSelectedChildBins([]);
                    setChildExposureError("");
                  }}
                />
                {text.childExposureOptions.no}
              </label>
              <label className="choice-row">
                <input
                  checked={childExposureChoice === "yes"}
                  name="child-exposure"
                  type="radio"
                  value="yes"
                  onChange={() => {
                    setChildExposureChoice("yes");
                    setChildExposureError("");
                  }}
                />
                {text.childExposureOptions.yes}
              </label>
              <label className="choice-row">
                <input
                  checked={childExposureChoice === "prefer_not_to_say"}
                  name="child-exposure"
                  type="radio"
                  value="prefer_not_to_say"
                  onChange={() => {
                    setChildExposureChoice("prefer_not_to_say");
                    setSelectedChildBins([]);
                    setChildExposureError("");
                  }}
                />
                {text.childExposureOptions.prefer_not_to_say}
              </label>
            </fieldset>

            {childExposureChoice === "yes" && (
              <fieldset className="fieldset">
                <legend>{text.childAgeBinsQuestion}</legend>
                <div className="bin-grid">
                  {CHILD_AGE_BINS.map((childAgeBin) => (
                    <label className="bin-choice" key={childAgeBin}>
                      <input
                        checked={selectedChildBins.includes(childAgeBin)}
                        type="checkbox"
                        value={childAgeBin}
                        onChange={() => {
                          toggleChildBin(childAgeBin);
                          setChildExposureError("");
                        }}
                      />
                      <span dir="ltr">{childAgeBin}</span>
                    </label>
                  ))}
                </div>
              </fieldset>
            )}

            {childExposureError && (
              <p className="error-text">
                {childExposureError === "choice"
                  ? text.errors.childExposureChoice
                  : text.errors.childAgeBins}
              </p>
            )}

            <button className="primary-button" type="submit">
              {text.startGuessing}
            </button>
          </form>
        </section>
      )}

      {screen === "trial" && currentAssignment && currentFace && (
        <section className="trial-card" aria-labelledby="trial-title">
          {languageToggle()}
          <div className="progress-row" aria-label={`${currentTrialIndex + 1} / ${TRIAL_COUNT}`}>
            <span dir="ltr">
              {currentTrialIndex + 1} / {TRIAL_COUNT}
            </span>
            <span className="progress-track" aria-hidden="true">
              <span
                className="progress-fill"
                style={{ width: `${((currentTrialIndex + 1) / TRIAL_COUNT) * 100}%` }}
              />
            </span>
          </div>

          <img className="face-image" src={currentFace.image_url} alt={text.imageAlt} />

          <form className="guess-form" onSubmit={handleGuessSubmit} noValidate>
            <div>
              <h1 id="trial-title" className="trial-title">
                {text.trialQuestion}
              </h1>
              <p className="hint-text">{text.trialHint}</p>
            </div>

            <div className="slider-picker" aria-label={text.guessedAge}>
              <div className="guess-readout" aria-live="polite" dir="ltr">
                {guessNumber ?? "?"}
              </div>
              <input
                aria-label={text.guessedAge}
                className={`age-slider ${guessNumber === null ? "is-empty" : ""}`}
                dir="ltr"
                max="100"
                min="1"
                step="1"
                type="range"
                value={guessNumber ?? 50}
                onChange={(event) => updateGuess(Number(event.target.value))}
              />
              <div className="slider-labels" aria-hidden="true" dir="ltr">
                <span>1</span>
                <span>100</span>
              </div>
              <div className="stepper-row">
                <button
                  aria-label={text.decreaseGuess}
                  className="stepper-button"
                  disabled={guessNumber === null || guessNumber <= 1}
                  type="button"
                  onClick={() => guessNumber !== null && updateGuess(guessNumber - 1)}
                >
                  −
                </button>
                <button
                  aria-label={text.increaseGuess}
                  className="stepper-button"
                  disabled={guessNumber === null || guessNumber >= 100}
                  type="button"
                  onClick={() => guessNumber !== null && updateGuess(guessNumber + 1)}
                >
                  +
                </button>
              </div>
            </div>

            <p className="microcopy">{text.guessMicrocopy}</p>
            {guessError && <p className="error-text">{text.errors.guess}</p>}

            <button className="primary-button" disabled={!canSubmitGuess} type="submit">
              {currentTrialIndex + 1 === TRIAL_COUNT ? text.finish : text.continue}
            </button>
          </form>
        </section>
      )}

      {screen === "thanks" && output && (
        <section className="card" aria-labelledby="thanks-title">
          {languageToggle()}
          <p className="eyebrow">{text.completeEyebrow}</p>
          <h1 id="thanks-title">{text.thankYouTitle}</h1>
          <div className="copy-stack">
            <p className="lede">{text.thankYouCopy}</p>
            <p>{text.continuePrompt}</p>
          </div>
          <div className="completion-actions">
            <button className="primary-button" type="button" onClick={handleDoTenMore}>
              {text.doTenMore}
            </button>
            <a
              className="secondary-button link-button"
              href="#dashboard"
              onClick={(event) => {
                event.preventDefault();
                openDashboard();
              }}
            >
              {text.dashboardLink}
            </a>
          </div>
        </section>
      )}

      {screen === "dashboard" && (
        <section className="card output-card" aria-labelledby="dashboard-title">
          {languageToggle()}
          <p className="eyebrow">{text.dashboardEyebrow}</p>
          <h1 id="dashboard-title">{text.dashboardTitle}</h1>
          <p className="lede">{text.dashboardCopy}</p>

          {!dashboardResult && <p className="dashboard-empty">{text.noRecentResult}</p>}

          {dashboardResult && (
            <>
              <dl className="dashboard-stats">
                <div>
                  <dt>{text.sessionIdLabel}</dt>
                  <dd dir="ltr">{dashboardResult.participant_sessions.session_id}</dd>
                </div>
                <div>
                  <dt>{text.statusLabel}</dt>
                  <dd>{dashboardResult.participant_sessions.status}</dd>
                </div>
                <div>
                  <dt>{text.completedAtLabel}</dt>
                  <dd dir="ltr">{dashboardResult.participant_sessions.completed_at ?? "—"}</dd>
                </div>
                <div>
                  <dt>{text.averageResponseTimeLabel}</dt>
                  <dd dir="ltr">{dashboardAverageResponseTimeMs} ms</dd>
                </div>
              </dl>

              <div className="output-header">
                <span>{text.latestResponsesLabel}</span>
                <span>
                  {dashboardResult.responses.length} {text.responsesLabel}
                </span>
              </div>
              <div className="responses-table" role="table" aria-label={text.latestResponsesLabel}>
                <div className="responses-row responses-head" role="row">
                  <span role="columnheader">{text.orderLabel}</span>
                  <span role="columnheader">{text.faceIdLabel}</span>
                  <span role="columnheader">{text.guessedAgeLabel}</span>
                  <span role="columnheader">{text.responseTimeLabel}</span>
                </div>
                {dashboardResult.responses.map((response) => (
                  <div className="responses-row" role="row" key={response.response_id}>
                    <span role="cell" dir="ltr">{response.client_order_index}</span>
                    <span role="cell" dir="ltr">{response.face_id}</span>
                    <span role="cell" dir="ltr">{response.predicted_age}</span>
                    <span role="cell" dir="ltr">{response.response_time_ms} ms</span>
                  </div>
                ))}
              </div>

              <div className="output-header">
                <span>{text.finalJsonOutput}</span>
              </div>
              <pre className="json-output" dir="ltr" lang="en">
                {dashboardJson}
              </pre>
            </>
          )}

          <button
            className="secondary-button"
            type="button"
            onClick={() => {
              window.history.replaceState(null, "", window.location.pathname);
              setScreen(output ? "thanks" : "landing");
            }}
          >
            {output ? text.backToThanks : text.start}
          </button>
        </section>
      )}
    </main>
  );
}
