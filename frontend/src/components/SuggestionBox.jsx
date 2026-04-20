function SuggestionBox({
    predictions,
    spellingSuggestions,
    grammarSuggestions,
    onInsertPrediction,
}) {
    return (
        <section className="suggestion-grid">
            <article className="card">
                <h3>Next word predictions</h3>
                <div className="prediction-list">
                    {predictions.length ? (
                        predictions.map((prediction) => (
                            <button
                                key={prediction}
                                type="button"
                                className="prediction-chip"
                                onClick={() => onInsertPrediction(prediction)}
                            >
                                {prediction}
                            </button>
                        ))
                    ) : (
                        <div className="suggestion-item">No predictions yet.</div>
                    )}
                </div>
            </article>

            <article className="card">
                <h3>Spelling guidance</h3>
                <div className="hint-list">
                    {spellingSuggestions.length ? (
                        spellingSuggestions.map((item) => (
                            <div key={`${item.start_index}-${item.end_index}`} className="suggestion-item">
                                Replace <strong>{item.original}</strong> with <strong>{item.suggestion}</strong>
                            </div>
                        ))
                    ) : (
                        <div className="suggestion-item">No spelling corrections detected.</div>
                    )}
                </div>
            </article>

            <article className="card">
                <h3>Grammar guidance</h3>
                <div className="hint-list">
                    {grammarSuggestions.length ? (
                        grammarSuggestions.map((item, index) => (
                            <div key={`${item.message}-${index}`} className="suggestion-item">
                                <strong>{item.message}</strong>
                                <div>{item.suggestion}</div>
                            </div>
                        ))
                    ) : (
                        <div className="suggestion-item">No grammar issues detected.</div>
                    )}
                    <div className="suggestion-item corrected-text">
                        Inline highlights in the editor now show where spelling corrections apply.
                    </div>
                </div>
            </article>
        </section>
    );
}

export default SuggestionBox;