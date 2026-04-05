import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";


const API_BASE_URL = "http://127.0.0.1:8000";
const ANSWERS = [
  "yes",
  "probably_yes",
  "i_dont_know",
  "probably_no",
  "no",
] as const;

type AnswerValue = (typeof ANSWERS)[number];

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
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<QuestionPayload | null>(null);
  const [guessName, setGuessName] = useState<string | null>(null);
  const [remainingCandidates, setRemainingCandidates] = useState<number | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function startGame() {
    setIsLoading(true);
    setError(null);
    setGuessName(null);
    setRemainingCandidates(null);

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
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  async function submitAnswer(answer: AnswerValue) {
    if (!sessionId) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/session/${sessionId}/answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answer }),
      });

      if (!response.ok) {
        throw new Error("Unable to submit answer.");
      }

      const data: AnswerResponse = await response.json();
      setRemainingCandidates(data.remaining_candidates);

      if (data.status === "question" && data.next_question) {
        setQuestion(data.next_question);
        return;
      }

      setQuestion(null);
      setGuessName(data.guess?.name ?? "Unknown");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Trace</Text>

        {!sessionId && !isLoading ? (
          <PrimaryButton label="Start Game" onPress={startGame} />
        ) : null}

        {isLoading ? <ActivityIndicator size="large" color="#111827" /> : null}

        {error ? <Text style={styles.error}>{error}</Text> : null}

        {question ? (
          <View style={styles.block}>
            <Text style={styles.question}>{question.text}</Text>
            {remainingCandidates !== null ? (
              <Text style={styles.meta}>
                Remaining candidates: {remainingCandidates}
              </Text>
            ) : null}

            <View style={styles.answers}>
              {ANSWERS.map((answer) => (
                <PrimaryButton
                  key={answer}
                  label={answer}
                  onPress={() => submitAnswer(answer)}
                  disabled={isLoading}
                />
              ))}
            </View>
          </View>
        ) : null}

        {guessName ? (
          <View style={styles.block}>
            <Text style={styles.guess}>I think it is: {guessName}</Text>
            {remainingCandidates !== null ? (
              <Text style={styles.meta}>
                Remaining candidates: {remainingCandidates}
              </Text>
            ) : null}
            <PrimaryButton label="Play Again" onPress={startGame} disabled={isLoading} />
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

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f3f4f6",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    gap: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: "700",
    color: "#111827",
    textAlign: "center",
  },
  block: {
    gap: 16,
  },
  question: {
    fontSize: 28,
    fontWeight: "600",
    color: "#111827",
    textAlign: "center",
  },
  guess: {
    fontSize: 30,
    fontWeight: "700",
    color: "#111827",
    textAlign: "center",
  },
  meta: {
    fontSize: 14,
    color: "#4b5563",
    textAlign: "center",
  },
  answers: {
    gap: 12,
  },
  button: {
    backgroundColor: "#111827",
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
  },
  buttonPressed: {
    opacity: 0.85,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "600",
    textAlign: "center",
  },
  error: {
    color: "#b91c1c",
    fontSize: 14,
    textAlign: "center",
  },
});
