from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import pandas as pd  # type: ignore
import plotly.graph_objects as go  # type: ignore
import requests  # type: ignore
import streamlit as st  # type: ignore

from dashboard.paths import ensure_project_cwd
from dashboard.theme import (
    COLORS,
    apply_plotly_theme,
    horizon_label,
    inject_futuristic_theme,
    render_advice_panel,
    render_empty_state,
    render_forecast_summary_compact,
    render_forecast_telemetry,
    render_future_outlook_panel,
    render_horizon_comparison_table,
    render_login_brand,
    render_market_stats_strip,
    render_prediction_history_table,
    render_prediction_metrics,
    render_profile_panel,
    render_raw_data_summary,
    render_raw_data_table,
    render_risk_summary_panel,
    render_sidebar_footer,
    render_topbar,
    render_watchlist_snapshot,
)
from dashboard.user_store import (
    add_prediction_history,
    authenticate_user,
    get_or_create_demo_user,
    init_user_store,
    load_prediction_history,
    load_preferences,
    load_watchlist,
    register_user,
    save_preferences,
    save_watchlist,
)

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

COMPANY_NAMES: dict[str, str] = {
    "RELIANCE.NS": "Reliance Industries",
    "INFY.NS": "Infosys",
    "TCS.NS": "Tata Consultancy Services",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet",
}


def symbol_label(symbol: str) -> str:
    company = COMPANY_NAMES.get(symbol.upper())
    return f"{symbol} — {company}" if company else symbol


def get_json(path: str, params: dict) -> Any:
    r = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
    if r.status_code >= 400:
        detail: Any
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        raise RuntimeError(f"API {path} failed ({r.status_code}): {detail}")
    return r.json()


def api_ok() -> bool:
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        return r.status_code == 200 and bool(r.json().get("ok"))
    except Exception:
        return False


def load_trained_symbols() -> list[str]:
    env_symbols = [s.strip().upper() for s in os.getenv("SYMBOLS", "RELIANCE.NS,INFY.NS,TCS.NS").split(",") if s.strip()]
    try:
        payload = get_json("/meta/symbols", {})
        api_symbols = [s.strip().upper() for s in payload.get("symbols", []) if s]
        if api_symbols:
            merged = env_symbols.copy()
            for sym in api_symbols:
                if sym not in merged:
                    merged.append(sym)
            return merged
    except Exception:
        pass
    return env_symbols


def horizon_to_timedelta(horizon: str) -> pd.Timedelta:
    h = horizon.lower().strip()
    if h.endswith("m"):
        return pd.Timedelta(minutes=int(h[:-1]))
    if h.endswith("d"):
        return pd.Timedelta(days=int(h[:-1]))
    return pd.Timedelta(minutes=5)


def build_advice(exp_return: float, p_up: float | None, risk_payload: dict[str, Any]) -> tuple[str, str]:
    p_down_2 = float(risk_payload.get("p_return_below_minus_2pct", 0.0))
    p_down_1 = float(risk_payload.get("p_return_below_minus_1pct", 0.0))
    p_up_val = 0.5 if p_up is None else float(p_up)

    if exp_return >= 0.002 and p_up_val >= 0.58 and p_down_2 < 0.25:
        return "Buy", "Positive expected return with supportive direction confidence and controlled downside risk."
    if exp_return <= -0.002 or p_down_2 >= 0.45:
        return "Sell / Reduce", "Negative expected move or elevated downside tail risk detected."
    if p_down_1 > 0.35:
        return "Cautious Hold", "Signal is mixed and short-horizon downside probability is meaningful."
    return "Hold", "No strong edge from the current forecast–confidence–risk combination."


def add_indicators(df: pd.DataFrame, ma_fast: int, ma_slow: int) -> pd.DataFrame:
    out = df.copy()
    out["ma_fast"] = out["close"].rolling(ma_fast).mean()
    out["ma_slow"] = out["close"].rolling(ma_slow).mean()
    out["ret_1"] = out["close"].pct_change(1)
    out["ret_5"] = out["close"].pct_change(5)
    return out


def build_price_figure(df: pd.DataFrame, chart_style: str, show_ma: bool, *, symbol: str) -> go.Figure:
    fig = go.Figure()
    if chart_style == "Candlestick":
        fig.add_trace(
            go.Candlestick(
                x=df["ts_utc"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="OHLC",
                increasing_line_color=COLORS["success"],
                decreasing_line_color=COLORS["danger"],
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df["ts_utc"],
                y=df["close"],
                mode="lines",
                name="Close",
                line=dict(width=2, color=COLORS["accent"]),
            )
        )

    if show_ma and "ma_fast" in df.columns and "ma_slow" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["ts_utc"],
                y=df["ma_fast"],
                mode="lines",
                name="MA fast",
                line=dict(width=1.5, color=COLORS["magenta"]),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["ts_utc"],
                y=df["ma_slow"],
                mode="lines",
                name="MA slow",
                line=dict(width=1.5, color=COLORS["violet"]),
            )
        )

    return apply_plotly_theme(fig, height=420, title=f"{symbol} price")


def build_volume_figure(df: pd.DataFrame, *, symbol: str) -> go.Figure:
    fig = go.Figure()
    colors = [
        COLORS["success"] if c >= o else COLORS["danger"]
        for c, o in zip(df["close"], df["open"], strict=False)
    ]
    fig.add_trace(
        go.Bar(
            x=df["ts_utc"],
            y=df["volume"],
            name="Volume",
            marker=dict(color=colors, opacity=0.75),
        )
    )
    return apply_plotly_theme(fig, height=220, title=f"{symbol} volume")


def build_risk_band_figure(
    *,
    last_close: float,
    expected_price: float,
    interval_low: float,
    interval_high: float,
    symbol: str,
) -> go.Figure:
    low_price = last_close * (1.0 + interval_low)
    high_price = last_close * (1.0 + interval_high)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Last close", "Band low", "Forecast", "Band high"],
            y=[last_close, low_price, expected_price, high_price],
            marker=dict(color=[COLORS["accent"], COLORS["violet"], COLORS["magenta"], COLORS["violet"]]),
            text=[f"${v:,.2f}" for v in [last_close, low_price, expected_price, high_price]],
            textposition="outside",
        )
    )
    return apply_plotly_theme(fig, height=320, title=f"{symbol} price levels")


def fetch_horizon_rows(symbol: str, horizons: list[str], *, force_update: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for horizon in horizons:
        timeframe = "1m" if horizon.endswith("m") else "1d"
        try:
            pred = get_json(
                "/predictions/latest",
                {"symbol": symbol, "horizon": horizon, "timeframe": timeframe, "force_update": force_update},
            )
            rows.append(pred)
        except RuntimeError:
            continue
    return rows


def fetch_watchlist_rows(
    symbols: list[str],
    *,
    horizon: str,
    timeframe: str,
    force_update: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sym in symbols[:6]:
        try:
            pred = get_json(
                "/predictions/latest",
                {"symbol": sym, "horizon": horizon, "timeframe": timeframe, "force_update": force_update},
            )
            risk = get_json(
                "/risk/latest",
                {"symbol": sym, "horizon": horizon, "timeframe": timeframe, "force_update": force_update},
            )
            advice, _ = build_advice(
                exp_return=float(pred["expected_return"]),
                p_up=pred.get("p_up"),
                risk_payload=risk,
            )
            rows.append({**pred, "advice": advice})
        except RuntimeError:
            continue
    return rows


def market_stats_from_df(df: pd.DataFrame) -> tuple[float, float, float | None, int]:
    if df.empty:
        return 0.0, 0.0, None, 0
    period_return = float(df["close"].iloc[-1] / df["close"].iloc[0] - 1.0)
    volatility = float(df["ret_1"].std()) if "ret_1" in df.columns and df["ret_1"].notna().any() else 0.0
    avg_volume = None
    if "volume" in df.columns and df["volume"].notna().any():
        avg_volume = float(df["volume"].dropna().mean())
    return period_return, volatility, avg_volume, len(df)


def init_session() -> None:
    st.session_state.setdefault("auth_user", None)
    st.session_state.setdefault("last_history_key", None)


def maybe_log_prediction(user_id: int, pred: dict[str, Any], *, force: bool) -> None:
    key = (pred["symbol"], pred["horizon"], pred["timeframe"], force)
    if st.session_state.get("last_history_key") == key and not force:
        return
    add_prediction_history(
        user_id,
        {
            "symbol": pred["symbol"],
            "horizon": pred["horizon"],
            "timeframe": pred["timeframe"],
            "expected_return": pred["expected_return"],
            "expected_price": pred["expected_price"],
            "p_up": pred.get("p_up"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    st.session_state["last_history_key"] = key


def render_login_page() -> dict[str, Any] | None:
    inject_futuristic_theme()
    render_login_brand()

    tab_login, tab_register = st.tabs(["Sign in", "Create account"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="your username")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            user = authenticate_user(username, password)
            if user is None:
                st.error("Invalid username or password.")
            else:
                st.session_state["auth_user"] = user
                st.rerun()
        if st.button("Continue as demo", use_container_width=True):
            st.session_state["auth_user"] = get_or_create_demo_user()
            st.rerun()

    with tab_register:
        with st.form("register_form", clear_on_submit=False):
            new_username = st.text_input("Username", key="reg_user", placeholder="pick a username")
            new_password = st.text_input("Password", type="password", key="reg_pass")
            new_password_2 = st.text_input("Confirm password", type="password", key="reg_pass2")
            create = st.form_submit_button("Create account", use_container_width=True)
        if create:
            if new_password != new_password_2:
                st.error("Passwords do not match.")
            else:
                ok, msg = register_user(new_username, new_password)
                st.success(msg) if ok else st.error(msg)

    return st.session_state.get("auth_user")


def user_index(values: list[str], preferred: str | None, fallback: int = 0) -> int:
    if preferred and preferred in values:
        return values.index(preferred)
    return fallback


def render_sidebar_controls(
    user: dict[str, Any],
    symbols: list[str],
    horizons: list[str],
    prefs: dict[str, Any],
    saved_watchlist: list[str],
) -> dict[str, Any]:
    with st.sidebar:
        st.markdown("### Account")
        st.caption(f"Signed in as **{user['username']}**")
        if st.button("Sign out", use_container_width=True):
            st.session_state["auth_user"] = None
            st.session_state["last_history_key"] = None
            st.rerun()

        st.divider()
        st.markdown("### India market")
        symbol = st.selectbox(
            "Symbol",
            symbols,
            index=user_index(symbols, prefs.get("favorite_symbol"), 0),
            format_func=symbol_label,
        )
        horizon = st.selectbox(
            "Forecast horizon",
            horizons,
            index=user_index(horizons, prefs.get("favorite_horizon"), 0),
            format_func=horizon_label,
        )

        watchlist = st.multiselect(
            "Watchlist",
            symbols,
            default=[s for s in saved_watchlist if s in symbols],
            help="Saved with your preferences.",
        )

        st.divider()
        st.markdown("### Chart")
        chart_style_options = ["Line", "Candlestick"]
        chart_style = st.selectbox(
            "Chart type",
            chart_style_options,
            index=user_index(chart_style_options, prefs.get("chart_style"), 0),
        )
        window_options = ["Short", "Medium", "Long"]
        window_label = st.selectbox(
            "History window",
            window_options,
            index=user_index(window_options, prefs.get("window_label"), 1),
        )
        show_ma = st.toggle("Moving averages", value=bool(prefs.get("show_ma", True)))
        if show_ma:
            ma_fast = st.slider("Fast MA", min_value=5, max_value=40, value=int(prefs.get("ma_fast", 20)))
            ma_slow = st.slider("Slow MA", min_value=20, max_value=120, value=int(prefs.get("ma_slow", 60)), step=5)
        else:
            ma_fast = int(prefs.get("ma_fast", 20))
            ma_slow = int(prefs.get("ma_slow", 60))

        st.divider()
        st.markdown("### Actions")
        force_update = st.toggle("Force fresh prediction", value=False)
        save_clicked = st.button("Save preferences", use_container_width=True, type="primary")
        refresh_clicked = st.button("Refresh data", use_container_width=True)

        if save_clicked:
            save_preferences(
                user["id"],
                {
                    "favorite_symbol": symbol,
                    "favorite_horizon": horizon,
                    "chart_style": chart_style,
                    "window_label": window_label,
                    "show_ma": show_ma,
                    "ma_fast": ma_fast,
                    "ma_slow": ma_slow,
                },
            )
            save_watchlist(user["id"], watchlist)
            st.toast("Preferences saved.")

        if refresh_clicked:
            st.session_state["last_history_key"] = None
            st.rerun()

        st.divider()
        render_sidebar_footer(symbol_count=len(symbols), api_base=API_BASE)

    return {
        "symbol": symbol,
        "horizon": horizon,
        "chart_style": chart_style,
        "window_label": window_label,
        "show_ma": show_ma,
        "ma_fast": ma_fast,
        "ma_slow": ma_slow,
        "force_update": force_update,
        "watchlist": watchlist,
    }


def main():
    ensure_project_cwd()
    st.set_page_config(
        page_title="Aegis Analytics",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_user_store()
    init_session()

    user = st.session_state.get("auth_user")
    if user is None:
        user = render_login_page()
        if user is None:
            return

    online = api_ok()
    if not online:
        inject_futuristic_theme()
        st.error(f"Cannot reach the API at `{API_BASE}`.")
        st.markdown(
            "Start the backend from the project root:\n\n"
            "```powershell\npython -m uvicorn backend.app:app --host 127.0.0.1 --port 8000\n```"
        )
        st.caption("If port 8000 is in use, stop the old process or change the port and set `API_BASE_URL`.")
        st.stop()

    inject_futuristic_theme()
    prefs = load_preferences(user["id"])
    saved_watchlist = load_watchlist(user["id"])

    symbols = load_trained_symbols()
    if not symbols:
        st.error("No trained models found. Run: `python -m ml.train --symbols AAPL`")
        st.stop()

    horizons = ["5m", "15m", "60m", "1d"]
    controls = render_sidebar_controls(user, symbols, horizons, prefs, saved_watchlist)

    symbol = controls["symbol"]
    horizon = controls["horizon"]
    chart_style = controls["chart_style"]
    window_label = controls["window_label"]
    show_ma = controls["show_ma"]
    ma_fast = controls["ma_fast"]
    ma_slow = controls["ma_slow"]
    force_update = controls["force_update"]
    watchlist = controls["watchlist"]

    render_topbar(
        title=f"Hello, {user['username']}",
        subtitle="Forecasts, price charts, and risk metrics for India stock symbols.",
        symbol=symbol,
        company_name=COMPANY_NAMES.get(symbol),
        horizon=horizon,
        api_online=online,
    )

    timeframe = "1m" if horizon.endswith("m") else "1d"
    limit = (
        {"Short": 120, "Medium": 300, "Long": 600}[window_label]
        if timeframe == "1m"
        else {"Short": 60, "Medium": 180, "Long": 365}[window_label]
    )

    try:
        bars = get_json("/bars/recent", {"symbol": symbol, "timeframe": timeframe, "limit": limit})
        pred = get_json(
            "/predictions/latest",
            {"symbol": symbol, "horizon": horizon, "timeframe": timeframe, "force_update": force_update},
        )
        risk = get_json(
            "/risk/latest",
            {"symbol": symbol, "horizon": horizon, "timeframe": timeframe, "force_update": force_update},
        )
    except RuntimeError as e:
        st.error(str(e))
        if "503" in str(e) and "Missing model artifact" in str(e):
            st.info(f"Train models for `{symbol}`:\n\n`python -m ml.train --symbols {symbol}`")
        st.stop()

    maybe_log_prediction(user["id"], pred, force=force_update)
    history_rows = load_prediction_history(user["id"], limit=20)

    df = pd.DataFrame(bars["bars"])
    if not df.empty:
        df["ts_utc"] = pd.to_datetime(df["ts_utc"])
        df = add_indicators(df, ma_fast=ma_fast, ma_slow=ma_slow)

    exp_return = pred["expected_return"]
    exp_price = pred["expected_price"]
    p_up = pred.get("p_up")
    interval_low = pred["interval_low"]
    interval_high = pred["interval_high"]
    last_close = float(pred["last_close"])

    period_return, volatility, avg_volume, bar_count = market_stats_from_df(df)
    compare_symbols = list(dict.fromkeys([symbol, *[s for s in watchlist if s in symbols]]))[:6]
    horizon_rows = fetch_horizon_rows(symbol, horizons, force_update=force_update)
    watchlist_rows = fetch_watchlist_rows(
        compare_symbols,
        horizon=horizon,
        timeframe=timeframe,
        force_update=force_update,
    )

    render_prediction_metrics(
        expected_return=exp_return,
        expected_price=exp_price,
        p_up=p_up,
        downside_risk=float(risk["p_return_below_minus_2pct"]),
    )

    tab_markets, tab_forecast, tab_risk, tab_account, tab_data = st.tabs(
        ["Markets", "Forecast", "Risk", "Account", "Data"]
    )

    with tab_markets:
        chart_col, summary_col = st.columns([1.65, 1], gap="medium")
        with chart_col:
            if not df.empty:
                st.plotly_chart(
                    build_price_figure(df, chart_style=chart_style, show_ma=show_ma, symbol=symbol),
                    width="stretch",
                )
                if "volume" in df.columns and df["volume"].notna().any():
                    st.plotly_chart(build_volume_figure(df, symbol=symbol), width="stretch")
                render_market_stats_strip(
                    period_return=period_return,
                    volatility=volatility,
                    avg_volume=avg_volume,
                    bar_count=bar_count,
                )
            else:
                render_empty_state("No price data", "Bars will appear once the API loads market data.")

        with summary_col:
            render_forecast_summary_compact(
                symbol=symbol,
                company_name=COMPANY_NAMES.get(symbol),
                horizon=horizon,
                timeframe=timeframe,
                last_close=last_close,
                expected_return=exp_return,
                expected_price=exp_price,
                interval_low=interval_low,
                interval_high=interval_high,
                p_up=p_up,
                model_version=pred.get("model_version"),
                model_trained_at=str(pred.get("model_timestamp_utc") or ""),
            )
            advice_label, advice_reason = build_advice(exp_return=exp_return, p_up=p_up, risk_payload=risk)
            st.markdown("##### Signal")
            render_advice_panel(advice_label, advice_reason)
            render_future_outlook_panel(
                symbol=symbol,
                horizon=horizon,
                timeframe=timeframe,
                last_close=last_close,
                expected_return=exp_return,
                expected_price=exp_price,
                interval_low=interval_low,
                interval_high=interval_high,
                p_up=p_up,
                last_timestamp=str(df["ts_utc"].iloc[-1]) if not df.empty else "—",
            )
            st.caption("Model-assisted guidance only — not financial advice.")
            render_watchlist_snapshot(watchlist_rows, current_symbol=symbol, horizon=horizon)

    with tab_forecast:
        render_forecast_telemetry(
            symbol=symbol,
            horizon=horizon,
            timeframe=timeframe,
            last_close=last_close,
            expected_return=exp_return,
            expected_price=exp_price,
            interval_low=interval_low,
            interval_high=interval_high,
            p_up=p_up,
            model_version=pred.get("model_version"),
        )
        render_horizon_comparison_table(horizon_rows, current_horizon=horizon)

        if not df.empty:
            last_ts = pd.to_datetime(df["ts_utc"].iloc[-1])
            future_ts = last_ts + horizon_to_timedelta(horizon)
            pred_low_price = last_close * (1.0 + interval_low)
            pred_high_price = last_close * (1.0 + interval_high)

            pred_fig = go.Figure()
            pred_fig.add_trace(
                go.Scatter(
                    x=df["ts_utc"],
                    y=df["close"],
                    mode="lines",
                    name="History",
                    line=dict(width=2, color=COLORS["accent"]),
                )
            )
            pred_fig.add_trace(
                go.Scatter(
                    x=[future_ts],
                    y=[exp_price],
                    mode="markers",
                    name="Forecast",
                    marker=dict(size=11, color=COLORS["magenta"], line=dict(width=1.5, color="#fff")),
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=[max(0.0, pred_high_price - exp_price)],
                        arrayminus=[max(0.0, exp_price - pred_low_price)],
                        visible=True,
                        color=COLORS["violet"],
                    ),
                )
            )
            pred_fig.add_trace(
                go.Scatter(
                    x=[last_ts, future_ts],
                    y=[last_close, exp_price],
                    mode="lines",
                    name="Projection",
                    line=dict(dash="dot", width=1.5, color=COLORS["violet"]),
                )
            )
            apply_plotly_theme(pred_fig, height=400, title=f"{symbol} · {horizon_label(horizon)} projection")
            st.plotly_chart(pred_fig, width="stretch")

            if "ret_1" in df.columns:
                hist_fig = go.Figure()
                hist_fig.add_trace(
                    go.Histogram(
                        x=(df["ret_1"].dropna() * 100),
                        nbinsx=36,
                        name="1-bar return (%)",
                        marker=dict(color=COLORS["violet"], line=dict(color=COLORS["accent"], width=0.3)),
                    )
                )
                apply_plotly_theme(hist_fig, height=260, title="Return distribution")
                st.plotly_chart(hist_fig, width="stretch")
        else:
            render_empty_state("No chart", "Need price history to draw the forecast projection.")

    with tab_risk:
        render_risk_summary_panel(
            last_close=last_close,
            expected_return=exp_return,
            expected_price=exp_price,
            interval_low=interval_low,
            interval_high=interval_high,
            p_down_1=float(risk["p_return_below_minus_1pct"]),
            p_down_2=float(risk["p_return_below_minus_2pct"]),
            p_up=p_up,
        )

        risk_left, risk_right = st.columns([1.1, 1], gap="medium")
        with risk_left:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("P(return < −1%)", f"{risk['p_return_below_minus_1pct'] * 100:.2f}%")
            with c2:
                st.metric("P(return < −2%)", f"{risk['p_return_below_minus_2pct'] * 100:.2f}%")

            conf_val = 50.0 if p_up is None else float(p_up) * 100
            gauge_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=conf_val,
                    number={"font": {"family": "IBM Plex Mono", "color": COLORS["accent"], "size": 32}},
                    title={
                        "text": "Direction confidence (P up)",
                        "font": {"family": "IBM Plex Sans", "color": COLORS["muted"], "size": 13},
                    },
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": COLORS["muted"]},
                        "bar": {"color": COLORS["accent"]},
                        "bgcolor": "rgba(10,16,30,0.8)",
                        "borderwidth": 1,
                        "bordercolor": COLORS["border"],
                        "steps": [
                            {"range": [0, 40], "color": "rgba(251,113,133,0.2)"},
                            {"range": [40, 60], "color": "rgba(251,191,36,0.15)"},
                            {"range": [60, 100], "color": "rgba(52,211,153,0.2)"},
                        ],
                    },
                )
            )
            apply_plotly_theme(gauge_fig, height=280)
            st.plotly_chart(gauge_fig, width="stretch")

        with risk_right:
            st.plotly_chart(
                build_risk_band_figure(
                    last_close=last_close,
                    expected_price=exp_price,
                    interval_low=interval_low,
                    interval_high=interval_high,
                    symbol=symbol,
                ),
                width="stretch",
            )
            render_horizon_comparison_table(horizon_rows, current_horizon=horizon)

    with tab_account:
        left, right = st.columns([1, 1.4], gap="medium")
        with left:
            render_profile_panel(
                username=user["username"],
                favorite_symbol=prefs.get("favorite_symbol"),
                favorite_horizon=prefs.get("favorite_horizon"),
                watchlist=watchlist,
                current_symbol=symbol,
                current_horizon=horizon,
            )
            st.markdown("##### Quick links")
            st.link_button("API docs", f"{API_BASE}/docs", use_container_width=True)
            st.link_button("Health check", f"{API_BASE}/health", use_container_width=True)
            st.caption(f"Last loaded {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        with right:
            st.markdown("##### Recent predictions")
            render_prediction_history_table(history_rows)
            st.markdown("##### Watchlist snapshot")
            render_watchlist_snapshot(watchlist_rows, current_symbol=symbol, horizon=horizon)

    with tab_data:
        render_raw_data_summary(df, symbol=symbol, timeframe=timeframe)
        render_raw_data_table(df, limit=100)
        csv_bytes = (df.to_csv(index=False) if not df.empty else "").encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"{symbol}_{timeframe}_{horizon}.csv",
            mime="text/csv",
            disabled=df.empty,
            use_container_width=False,
        )


main()
