import { useEffect, useRef, useState } from 'react';
import { suggestText } from '../services/api';

function renderHighlightedText(text, spellingSuggestions) {
    if (!text) {
        return <span className="highlight-empty">Start typing to see inline highlights.</span>;
    }

    if (!spellingSuggestions.length) {
        return <span>{text}</span>;
    }

    const segments = [];
    let currentIndex = 0;

    spellingSuggestions
        .slice()
        .sort((left, right) => left.start_index - right.start_index)
        .forEach((item) => {
            if (item.start_index > currentIndex) {
                segments.push(
                    <span key={`text-${currentIndex}`}>{text.slice(currentIndex, item.start_index)}</span>,
                );
            }

            const originalText = text.slice(item.start_index, item.end_index);
            segments.push(
                <mark
                    key={`mark-${item.start_index}-${item.end_index}`}
                    className="inline-highlight"
                    title={`Suggestion: ${item.suggestion}`}
                >
                    {originalText}
                </mark>,
            );

            currentIndex = item.end_index;
        });

    if (currentIndex < text.length) {
        segments.push(<span key={`tail-${currentIndex}`}>{text.slice(currentIndex)}</span>);
    }

    return segments;
}

function Editor({
    text,
    setText,
    cursorPosition,
    setCursorPosition,
    suggestions,
    setSuggestions,
    setErrorMessage,
}) {
    const [isLoading, setIsLoading] = useState(false);
    const debounceRef = useRef(null);

    const applyCorrectedText = () => {
        if (!suggestions.corrected_text) {
            return;
        }

        setText(suggestions.corrected_text);
        setCursorPosition(suggestions.corrected_text.length);
    };

    useEffect(() => {
        window.clearTimeout(debounceRef.current);

        if (!text.trim()) {
            setSuggestions({
                corrected_text: '',
                spelling_suggestions: [],
                grammar_suggestions: [],
                next_word_predictions: [],
            });
            return undefined;
        }

        debounceRef.current = window.setTimeout(async () => {
            try {
                setIsLoading(true);
                setErrorMessage('');
                const response = await suggestText({ text, cursor_position: cursorPosition });
                setSuggestions(response);
            } catch (error) {
                setErrorMessage(error.message || 'Failed to fetch suggestions.');
            } finally {
                setIsLoading(false);
            }
        }, 300);

        return () => window.clearTimeout(debounceRef.current);
    }, [text, cursorPosition, setSuggestions, setErrorMessage]);

    const handleChange = (event) => {
        setText(event.target.value);
        setCursorPosition(event.target.selectionStart ?? event.target.value.length);
    };

    const handleSelection = (event) => {
        setCursorPosition(event.target.selectionStart ?? 0);
    };

    return (
        <section className="editor">
            <textarea
                value={text}
                onChange={handleChange}
                onClick={handleSelection}
                onKeyUp={handleSelection}
                placeholder="Start typing to receive spelling, grammar, and autocomplete suggestions..."
            />
            <div className="editor-status">
                <span>{isLoading ? 'Refreshing suggestions...' : 'Suggestions up to date'}</span>
                <span>
                    {text.length} characters | cursor at {cursorPosition}
                </span>
            </div>

            <section className="inline-insights">
                <div className="inline-insights-header">
                    <div>
                        <p className="section-kicker">Inline Assist</p>
                        <h3>Correction map inside the writing flow</h3>
                    </div>
                    {suggestions.corrected_text && suggestions.corrected_text !== text ? (
                        <button type="button" className="apply-fixes-button" onClick={applyCorrectedText}>
                            Apply all spelling fixes
                        </button>
                    ) : null}
                </div>

                <div className="inline-preview-card">
                    <div className="inline-preview-copy">
                        {renderHighlightedText(text, suggestions.spelling_suggestions)}
                    </div>
                </div>

                <div className="inline-caption-row">
                    <span>
                        {suggestions.spelling_suggestions.length
                            ? `${suggestions.spelling_suggestions.length} spelling issue(s) highlighted`
                            : 'No spelling issues highlighted'}
                    </span>
                    <span>
                        {suggestions.grammar_suggestions.length
                            ? `${suggestions.grammar_suggestions.length} grammar hint(s) available`
                            : 'Grammar looks clean'}
                    </span>
                </div>
            </section>
        </section>
    );
}

export default Editor;