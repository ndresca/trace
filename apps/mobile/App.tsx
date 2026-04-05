import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import {
  REMOVE_ADS_PRICE_LABEL,
  usePurchaseState,
} from "./purchases";

const API_BASE_URL = "http://127.0.0.1:8000";
const ANSWER_OPTIONS = [
  { value: "yes", label: "Yes" },
  { value: "probably_yes", label: "Probably Yes" },
  { value: "i_dont_know", label: "I Don't Know" },
  { value: "probably_no", label: "Probably No" },
  { value: "no", label: "No" },
] as const;

type AnswerValue = (typeof ANSWER_OPTIONS)[number]["value"];

type QuestionPayload = {
  id: string;
  text: string;
  attribute_key: string;
};

type StartSessionResponse = {
  session_id: string;
  question: QuestionPayload;
};

type AnswerResponse = {
  status: "question" | "guess";
  next_question?: QuestionPayload | null;
  guess?: {
    id: string;
    name: string;
  } | null;
  remaining_candidates: number;
};

export default function App() {
  const { adsRemoved, isReady, removeAds, restorePurchases } =
    usePurchaseState();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<QuestionPayload | null>(null);
  const [guessName, setGuessName] = useState<string | null>(null);
  const [remainingCandidates, setRemainingCandidates] = useState<number | null>(
    null,
  );
  const [questionNumber, setQuestionNumber] = useState<number>(0);
  const [showInterstitial, setShowInterstitial] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingLabel, setLoadingLabel] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function resetGameState() {
    setSessionId(null);
    setQuestion(null);
    setGuessName(null);
    setRemainingCandidates(null);
    setQuestionNumber(0);
    setShowInterstitial(false);
    setError(null);
    setLoadingLabel(null);
  }

  async function handleRemoveAds() {
    setIsLoading(true);
    setLoadingLabel("Purchasing Remove Ads...");
    setError(null);

    try {
      await removeAds();
      resetGameState();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to update your purchase right now.",
      );
    } finally {
      setIsLoading(false);
      setLoadingLabel(null);
    }
  }

  async function handleRestorePurchases() {
    setIsLoading(true);
    setLoadingLabel("Restoring purchases...");
    setError(null);

    try {
      const result = await restorePurchases();
      if (result.restored) {
        resetGameState();
        return;
      }

      setError("No previous Remove Ads purchase was found.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to restore purchases.");
    } finally {
      setIsLoading(false);
      setLoadingLabel(null);
    }
  }

  function handleContinueAfterGuess() {
    if (adsRemoved) {
      resetGameState();
      return;
    }

    setShowInterstitial(true);
  }

  function handleSkipInterstitial() {
    resetGameState();
  }

  async function startGame() {
    setIsLoading(true);
    setLoadingLabel("Starting game...");
    setError(null);
    setQuestion(null);
    setGuessName(null);
    setRemainingCandidates(null);
    setQuestionNumber(0);

    try {
      const response = await fetch(`${API_BASE_URL}/session/start`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Unable to start game.");
      }

      const data: StartSessionResponse = await response.json();
      setSessionId(data.session_id);
      setQuestion(data.question);
      setQuestionNumber(1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
      setLoadingLabel(null);
    }
  }

  async function submitAnswer(answer: AnswerValue) {
    if (!sessionId) {
      return;
    }

    setIsLoading(true);
    setLoadingLabel("Submitting answer...");
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/session/${sessionId}/answer`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ answer }),
        },
      );

      if (!response.ok) {
        throw new Error("Unable to submit answer.");
      }

      const data: AnswerResponse = await response.json();
      setRemainingCandidates(data.remaining_candidates);

      if (data.status === "question" && data.next_question) {
        setQuestion(data.next_question);
        setQuestionNumber((current) => current + 1);
        return;
      }

      setQuestion(null);
      setGuessName(data.guess?.name ?? "Unknown");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
      setLoadingLabel(null);
    }
  }

  const hasStarted =
    sessionId !== null ||
    question !== null ||
    guessName !== null ||
    showInterstitial;
  const progressLabel = questionNumber > 0 ? `Question ${questionNumber}` : "Question";
  const displayQuestionText = question ? formatQuestionText(question.text) : null;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {!isReady ? (
          <View style={styles.loadingBlock}>
            <ActivityIndicator size="large" color="#111827" />
            <Text style={styles.meta}>Loading...</Text>
          </View>
        ) : null}

        {showInterstitial ? (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>Sponsored</Text>
            <Text style={styles.guessLead}>Your ad would appear here</Text>
            <Text style={styles.meta}>
              This is a placeholder for the future interstitial ad experience.
            </Text>
            <View style={styles.actions}>
              <PrimaryButton
                label="Skip"
                onPress={handleSkipInterstitial}
                disabled={isLoading}
              />
              <SecondaryButton
                label={`Remove Ads Forever — ${REMOVE_ADS_PRICE_LABEL}`}
                onPress={() => {
                  void handleRemoveAds();
                }}
                disabled={isLoading}
              />
            </View>
          </View>
        ) : null}

        {isReady && !hasStarted && !guessName ? (
          <View style={styles.hero}>
            <Text style={styles.title}>Trace</Text>
            <Text style={styles.subtitle}>
              Think of a famous person and I&apos;ll guess who it is.
            </Text>
            <PrimaryButton
              label="Start Game"
              onPress={startGame}
              disabled={isLoading}
            />
            {!adsRemoved ? (
              <SecondaryButton
                label={`Remove Ads — ${REMOVE_ADS_PRICE_LABEL}`}
                onPress={() => {
                  void handleRemoveAds();
                }}
                disabled={isLoading}
              />
            ) : null}
            <SecondaryButton
              label="Restore Purchases"
              onPress={() => {
                void handleRestorePurchases();
              }}
              disabled={isLoading}
            />
          </View>
        ) : null}

        {isLoading ? (
          <View style={styles.loadingBlock}>
            <ActivityIndicator size="large" color="#111827" />
            <Text style={styles.meta}>{loadingLabel ?? "Loading..."}</Text>
          </View>
        ) : null}

        {error ? (
          <View style={styles.errorBlock}>
            <Text style={styles.error}>{error}</Text>
            <View style={styles.actions}>
              <PrimaryButton
                label={sessionId ? "Retry" : "Start Game"}
                onPress={startGame}
                disabled={isLoading}
              />
              <SecondaryButton
                label="Restart"
                onPress={resetGameState}
                disabled={isLoading}
              />
            </View>
          </View>
        ) : null}

        {question && !showInterstitial ? (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>{progressLabel}</Text>
            <Text style={styles.question}>{displayQuestionText}</Text>
            {remainingCandidates !== null ? (
              <Text style={styles.meta}>
                Remaining candidates: {remainingCandidates}
              </Text>
            ) : null}

            <View style={styles.answers}>
              {ANSWER_OPTIONS.map((answer) => (
                <PrimaryButton
                  key={answer.value}
                  label={answer.label}
                  onPress={() => submitAnswer(answer.value)}
                  disabled={isLoading}
                />
              ))}
            </View>
          </View>
        ) : null}

        {guessName && !showInterstitial ? (
          <View style={styles.card}>
            <Text style={styles.guessLead}>I think it is...</Text>
            <Text style={styles.guess}>{guessName}</Text>
            <PrimaryButton
              label="Play Again"
              onPress={handleContinueAfterGuess}
              disabled={isLoading}
            />
          </View>
        ) : null}
      </View>
    </SafeAreaView>
  );
}

type PrimaryButtonProps = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
};

function formatQuestionText(text: string) {
  if (text === "Is this person female?") {
    return "Is this person a woman?";
  }

  if (text === "Is this person male?") {
    return "Is this person a man?";
  }

  return text;
}

function PrimaryButton({ label, onPress, disabled = false }: PrimaryButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        disabled ? styles.buttonDisabled : null,
        pressed && !disabled ? styles.buttonPressed : null,
      ]}
    >
      <Text style={styles.buttonText}>{label}</Text>
    </Pressable>
  );
}

function SecondaryButton({
  label,
  onPress,
  disabled = false,
}: PrimaryButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.secondaryButton,
        disabled ? styles.buttonDisabled : null,
        pressed && !disabled ? styles.buttonPressed : null,
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
  loadingBlock: {
    alignItems: "center",
    gap: 12,
  },
  errorBlock: {
    gap: 12,
  },
  actions: {
    gap: 10,
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
    fontSize: 30,
    fontWeight: "600",
    color: "#111827",
    textAlign: "center",
    lineHeight: 38,
  },
  guessLead: {
    fontSize: 22,
    fontWeight: "600",
    color: "#111827",
    textAlign: "center",
  },
  guess: {
    fontSize: 34,
    fontWeight: "700",
    color: "#111827",
    textAlign: "center",
  },
  meta: {
    fontSize: 15,
    color: "#4b5563",
    textAlign: "center",
  },
  answers: {
    gap: 14,
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
  error: {
    color: "#b91c1c",
    fontSize: 15,
    textAlign: "center",
  },
});
