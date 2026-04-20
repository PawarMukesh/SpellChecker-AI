function Toolbar({ onRewrite, isBusy }) {
    return (
        <div className="toolbar">
            <button type="button" onClick={() => onRewrite('rephrase')} disabled={isBusy}>
                Rephrase
            </button>
            <button type="button" className="secondary" onClick={() => onRewrite('formal')} disabled={isBusy}>
                Formal
            </button>
            <button type="button" className="tertiary" onClick={() => onRewrite('informal')} disabled={isBusy}>
                Informal
            </button>
        </div>
    );
}

export default Toolbar;