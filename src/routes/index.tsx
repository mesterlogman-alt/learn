import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return (
    <main className="lingo-shell">
      <div className="lingo-fallback">
        <div>
          <h1>Lingo</h1>
          <p>منصة تعلم إنجليزية تعمل محليًا — صنع بواسطة لقمان</p>
        </div>
      </div>
      <iframe
        src="/lingo.html"
        title="Lingo Memory"
        allow="clipboard-read; clipboard-write; fullscreen; microphone"
      />
    </main>
  );
}
