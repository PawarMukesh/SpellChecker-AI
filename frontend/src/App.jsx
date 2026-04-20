import { useState } from 'react';
import Editor from './components/Editor';
import SuggestionBox from './components/SuggestionBox';
import Toolbar from './components/Toolbar';
import { rewriteText } from './services/api';

const initialSuggestions = {
    corrected_text: '',
    spelling_suggestions: [],
    grammar_suggestions: [],
    next_word_predictions: [],
};

function App() {
    const [text, setText] = useState('');
    const [cursorPosition, setCursorPosition] = useState(0);
    const [suggestions, setSuggestions] = useState(initialSuggestions);
    const [isRewriting, setIsRewriting] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const metrics = [
        { label: 'Rewrite engine', value: 'Qwen endpoint' },
        { label: 'Suggestion latency', value: '300ms debounce' },
        { label: 'API shape', value: 'FastAPI + Vite' },
    ];

    const handleInsertPrediction = (prediction) => {
        const beforeCursor = text.slice(0, cursorPosition);
        const afterCursor = text.slice(cursorPosition);
        const spacer = beforeCursor.endsWith(' ') || beforeCursor.length === 0 ? '' : ' ';
        const nextText = `${beforeCursor}${spacer}${prediction} ${afterCursor}`;

        setText(nextText);
        setCursorPosition(beforeCursor.length + spacer.length + prediction.length + 1);
    };

    const handleRewrite = async (mode) => {
        if (!text.trim()) {
            return;
        }

        try {
            setIsRewriting(true);
            setErrorMessage('');
            const response = await rewriteText({ text, mode });
            setText(response.rewritten_text);
            setCursorPosition(response.rewritten_text.length);
        } catch (error) {
            setErrorMessage(error.message || 'Failed to rewrite text.');
        } finally {
            setIsRewriting(false);
        }
    };

    return (
        <main className="app-shell">
            <section className="hero-panel">
                <div className="hero-badge-row">
                    <p className="eyebrow">Enterprise Writing Assistant</p>
                    <span className="hero-badge">Production-ready scaffold</span>
                </div>
                <h1>Compose faster with live corrections and Qwen-powered rewriting.</h1>
                <p className="hero-copy">
                    Spell correction, grammar guidance, autocomplete, and rewrite actions run through a modular FastAPI backend connected to a configurable Qwen-compatible model endpoint.
                </p>
                <div className="metrics-row">
                    {metrics.map((metric) => (
                        <div key={metric.label} className="metric-card">
                            <span>{metric.label}</span>
                            <strong>{metric.value}</strong>
                        </div>
                    ))}
                </div>
            </section>

            <section className="workspace-panel">
                <div className="workspace-header">
                    <div>
                        <p className="section-kicker">Compose</p>
                        <h2>Rewrite, refine, and predict as you type.</h2>
                    </div>
                    <div className="workspace-pill">Local model only</div>
                </div>
                <Toolbar onRewrite={handleRewrite} isBusy={isRewriting} />
                <Editor
                    text={text}
                    setText={setText}
                    cursorPosition={cursorPosition}
                    setCursorPosition={setCursorPosition}
                    suggestions={suggestions}
                    setSuggestions={setSuggestions}
                    setErrorMessage={setErrorMessage}
                />
                <SuggestionBox
                    predictions={suggestions.next_word_predictions}
                    spellingSuggestions={suggestions.spelling_suggestions}
                    grammarSuggestions={suggestions.grammar_suggestions}
                    onInsertPrediction={handleInsertPrediction}
                />
                {errorMessage ? <div className="status-banner error">{errorMessage}</div> : null}
            </section>
        </main>
    );
}

export default App;