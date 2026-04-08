import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SafeAreaView,
  Share,
  StyleSheet,
  Text,
  View,
} from "react-native";
import {
  REMOVE_ADS_PRICE_LABEL,
  usePurchaseState,
} from "./purchases";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const ANSWER_OPTIONS = [
  { value: "yes", label: "Yes" },
  { value: "probably_yes", label: "Probably" },
  { value: "i_dont_know", label: "Don't Know" },
  { value: "probably_no", label: "Probably Not" },
  { value: "no", label: "No" },
] as const;

type AnswerValue = (typeof ANSWER_OPTIONS)[number]["value"];

type QuestionPayload = {
  id: string;
  text: string;
  attribute_key: string;
};

type GuessPayload = {
  id: string;
  name: string;
};

type StartResponse = {
  session_id: string;
  question: QuestionPayload;
};

type AnswerResponse = {
  status: "question" | "guess";
  next_question?: QuestionPayload | null;
  guess?: GuessPayload | null;
  remaining_candidates: number;
};

type Screen = "home" | "question" | "guess" | "result" | "interstitial";

export default function App() {
  const { adsRemoved, isReady, removeAds, restorePurchases } =
    usePurchaseState();

  const [screen, setScreen] = useState<Screen>("home");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<QuestionPayload | null>(null);
  const [guess, setGuess] = useState<GuessPayload | null>(null);
  const [remaining, setRemaining] = useState<number>(0);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [answerHistory, setAnswerHistory] = useState<{ question_id: string; answer: string }[]>([]);

  function resetGame() {
    setScreen("home");
    setSessionId(null);
    setQuestion(null);
    setGuess(null);
    setRemaining(0);
    setQuestionNumber(0);
    setError(null);
    setAnswerHistory([]);
  }

  async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || `Request failed (${response.status})`);
    }
    return response.json();
  }

  function handleAnswerResponse(data: AnswerResponse) {
    setRemaining(data.remaining_candidates);
    if (data.status === "guess" && data.guess) {
      setGuess(data.guess);
      setQuestion(null);
      setScreen("guess");
    } else if (data.next_question) {
      setQuestion(data.next_question);
      setQuestionNumber((n) => n + 1);
    }
  }

  async function startGame() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch<StartResponse>(`${API_BASE_URL}/start`, {
        method: "POST",
      });
      setSessionId(data.session_id);
      setQuestion(data.question);
      setQuestionNumber(1);
      setAnswerHistory([]);
      setScreen("question");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start game.");
    } finally {
      setIsLoading(false);
    }
  }

  async function submitAnswer(answer: AnswerValue) {
    if (!sessionId || !question) return;
    const questionId = question.id;
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch<AnswerResponse>(`${API_BASE_URL}/answer`, {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, answer }),
      });
      setAnswerHistory((prev) => [...prev, { question_id: questionId, answer }]);
      handleAnswerResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleWrongGuess() {
    if (!sessionId) return;
    sendFeedback(false, guess?.id);
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch<AnswerResponse>(`${API_BASE_URL}/continue`, {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId }),
      });
      handleAnswerResponse(data);
      if (data.status === "question") {
        setScreen("question");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to continue.");
    } finally {
      setIsLoading(false);
    }
  }

  function sendFeedback(wasCorrect: boolean, correctEntityId?: string) {
    if (!sessionId) return;
    fetch(`${API_BASE_URL}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        correct_entity_id: correctEntityId ?? null,
        was_correct: wasCorrect,
        questions_asked: answerHistory,
      }),
    }).catch(() => {});
  }

  function handleCorrectGuess() {
    sendFeedback(true, guess?.id);
    if (adsRemoved) {
      setScreen("result");
    } else {
      setScreen("interstitial");
    }
  }

  async function handleShare() {
    if (!guess) return;
    await Share.share({
      message: `Trace guessed ${guess.name} in ${questionNumber} questions! Can you stump it?`,
    });
  }

  async function handleRemoveAds() {
    setIsLoading(true);
    setError(null);
    try {
      await removeAds();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Purchase failed.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleRestorePurchases() {
    setIsLoading(true);
    setError(null);
    try {
      const result = await restorePurchases();
      if (!result.restored) {
        setError("No previous purchase found.");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Restore failed.");
    } finally {
      setIsLoading(false);
    }
  }

  if (!isReady) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.center}>
          <ActivityIndicator size="large" color="#111827" />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* HOME */}
        {screen === "home" && (
          <View style={styles.hero}>
            <Text style={styles.title}>Trace</Text>
            <Text style={styles.subtitle}>
              Think of a famous person and I'll guess who it is.
            </Text>
            <PrimaryButton
              label="Start Game"
              onPress={startGame}
              disabled={isLoading}
            />
            {!adsRemoved && (
              <SecondaryButton
                label={`Remove Ads — ${REMOVE_ADS_PRICE_LABEL}`}
                onPress={() => void handleRemoveAds()}
                disabled={isLoading}
              />
            )}
            <SecondaryButton
              label="Restore Purchases"
              onPress={() => void handleRestorePurchases()}
              disabled={isLoading}
            />
          </View>
        )}

        {/* QUESTION */}
        {screen === "question" && question && (
          <View style={styles.card}>
            <Text style={styles.question}>{formatQuestionText(question.text)}</Text>
            <View style={styles.answers}>
              <View style={styles.answerRow}>
                <AnswerButton label="Yes" onPress={() => submitAnswer("yes")} disabled={isLoading} />
                <AnswerButton label="Probably" onPress={() => submitAnswer("probably_yes")} disabled={isLoading} />
              </View>
              <View style={styles.answerRow}>
                <AnswerButton label="Don't Know" onPress={() => submitAnswer("i_dont_know")} disabled={isLoading} variant="neutral" />
              </View>
              <View style={styles.answerRow}>
                <AnswerButton label="Probably Not" onPress={() => submitAnswer("probably_no")} disabled={isLoading} variant="negative" />
                <AnswerButton label="No" onPress={() => submitAnswer("no")} disabled={isLoading} variant="negative" />
              </View>
            </View>
          </View>
        )}

        {/* GUESS */}
        {screen === "guess" && guess && (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>My Guess</Text>
            <Text style={styles.guess}>{guess.name}</Text>
            <Text style={styles.meta}>
              After {questionNumber} question{questionNumber !== 1 ? "s" : ""}
            </Text>
            <Text style={styles.guessPrompt}>Was I right?</Text>
            <View style={styles.answers}>
              <PrimaryButton
                label="Yes!"
                onPress={handleCorrectGuess}
                disabled={isLoading}
              />
              <SecondaryButton
                label="No, keep trying"
                onPress={() => void handleWrongGuess()}
                disabled={isLoading}
              />
            </View>
          </View>
        )}

        {/* RESULT (correct guess) */}
        {screen === "result" && guess && (
          <View style={styles.card}>
            <Text style={styles.resultEmoji}>🎯</Text>
            <Text style={styles.guess}>{guess.name}</Text>
            <Text style={styles.meta}>
              Guessed in {questionNumber} question{questionNumber !== 1 ? "s" : ""}
            </Text>
            <View style={styles.answers}>
              <PrimaryButton label="Share" onPress={() => void handleShare()} />
              <SecondaryButton label="Play Again" onPress={() => void startGame()} />
            </View>
          </View>
        )}

        {/* INTERSTITIAL (ad placeholder before result) */}
        {screen === "interstitial" && (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>Sponsored</Text>
            <Text style={styles.meta}>Your ad would appear here.</Text>
            <View style={styles.answers}>
              <PrimaryButton label="Continue" onPress={() => setScreen("result")} />
              <SecondaryButton
                label={`Remove Ads Forever — ${REMOVE_ADS_PRICE_LABEL}`}
                onPress={() => void handleRemoveAds()}
                disabled={isLoading}
              />
            </View>
          </View>
        )}

        {/* LOADING OVERLAY */}
        {isLoading && (
          <View style={styles.loadingOverlay}>
            <ActivityIndicator size="small" color="#111827" />
          </View>
        )}

        {/* ERROR */}
        {error && (
          <View style={styles.errorBlock}>
            <Text style={styles.error}>{error}</Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

function formatQuestionText(text: string) {
  if (text === "Is this person female?") return "Is this person a woman?";
  if (text === "Is this person male?") return "Is this person a man?";
  return text;
}

type ButtonProps = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
};

function PrimaryButton({ label, onPress, disabled = false }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        disabled && styles.buttonDisabled,
        pressed && !disabled && styles.buttonPressed,
      ]}
    >
      <Text style={styles.buttonText}>{label}</Text>
    </Pressable>
  );
}

type AnswerButtonProps = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: "positive" | "neutral" | "negative";
};

function AnswerButton({ label, onPress, disabled = false, variant = "positive" }: AnswerButtonProps) {
  const bg = variant === "negative" ? "#fef2f2" : variant === "neutral" ? "#f3f4f6" : "#f0fdf4";
  const fg = variant === "negative" ? "#991b1b" : variant === "neutral" ? "#374151" : "#166534";
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.answerButton,
        { backgroundColor: bg },
        disabled && styles.buttonDisabled,
        pressed && !disabled && styles.buttonPressed,
      ]}
    >
      <Text style={[styles.answerButtonText, { color: fg }]}>{label}</Text>
    </Pressable>
  );
}

function SecondaryButton({ label, onPress, disabled = false }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.secondaryButton,
        disabled && styles.buttonDisabled,
        pressed && !disabled && styles.buttonPressed,
      ]}
    >
      <Text style={styles.secondaryButtonText}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8fafc",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    gap: 24,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  hero: {
    gap: 16,
  },
  title: {
    fontSize: 40,
    fontWeight: "700",
    color: "#111827",
    textAlign: "center",
  },
  subtitle: {
    fontSize: 18,
    lineHeight: 26,
    color: "#4b5563",
    textAlign: "center",
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 20,
    padding: 20,
    gap: 16,
    shadowColor: "#111827",
    shadowOpacity: 0.08,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 8 },
    elevation: 2,
  },
  eyebrow: {
    fontSize: 14,
    fontWeight: "600",
    letterSpacing: 0.4,
    color: "#475569",
    textAlign: "center",
    textTransform: "uppercase",
  },
  question: {
    fontSize: 28,
    fontWeight: "600",
    color: "#111827",
    textAlign: "center",
    lineHeight: 36,
  },
  guess: {
    fontSize: 34,
    fontWeight: "700",
    color: "#111827",
    textAlign: "center",
  },
  guessPrompt: {
    fontSize: 20,
    fontWeight: "500",
    color: "#4b5563",
    textAlign: "center",
  },
  resultEmoji: {
    fontSize: 48,
    textAlign: "center",
  },
  meta: {
    fontSize: 15,
    color: "#4b5563",
    textAlign: "center",
  },
  answers: {
    gap: 10,
  },
  answerRow: {
    flexDirection: "row",
    gap: 10,
  },
  answerButton: {
    flex: 1,
    borderRadius: 14,
    paddingVertical: 14,
    paddingHorizontal: 12,
  },
  answerButtonText: {
    fontSize: 16,
    fontWeight: "600",
    textAlign: "center",
  },
  button: {
    backgroundColor: "#111827",
    borderRadius: 14,
    paddingVertical: 16,
    paddingHorizontal: 18,
  },
  buttonPressed: {
    opacity: 0.85,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: "#ffffff",
    fontSize: 17,
    fontWeight: "600",
    textAlign: "center",
  },
  secondaryButton: {
    backgroundColor: "#e5e7eb",
    borderRadius: 14,
    paddingVertical: 16,
    paddingHorizontal: 18,
  },
  secondaryButtonText: {
    color: "#111827",
    fontSize: 17,
    fontWeight: "600",
    textAlign: "center",
  },
  loadingOverlay: {
    position: "absolute",
    top: 16,
    right: 16,
  },
  errorBlock: {
    paddingVertical: 8,
  },
  error: {
    color: "#b91c1c",
    fontSize: 15,
    textAlign: "center",
  },
});
