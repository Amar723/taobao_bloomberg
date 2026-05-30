BLOOMBERG_LAYOUT = dict(
    paper_bgcolor="#0a0a0a",
    plot_bgcolor="#0a0a0a",
    font=dict(color="white", family="monospace"),
    scene=dict(
        xaxis=dict(
            title="Moneyness (%)",
            gridcolor="#333",
            zerolinecolor="#555",
            backgroundcolor="#111",
            showbackground=True,
            ticksuffix="%",
        ),
        yaxis=dict(
            title="Expiry (years)",
            gridcolor="#333",
            backgroundcolor="#111",
            showbackground=True,
            tickvals=[0.25, 0.5, 1.0, 1.5, 2.0],
            ticktext=["3M", "6M", "1Y", "18M", "2Y"],
        ),
        zaxis=dict(
            title="Implied Vol (%)",
            gridcolor="#333",
            backgroundcolor="#111",
            showbackground=True,
            ticksuffix="%",
        ),
        camera=dict(eye=dict(x=1.8, y=-1.8, z=0.5)),  # low wide angle like Bloomberg
        bgcolor="#111111",
    ),
    margin=dict(l=0, r=0, t=40, b=0),
)