"""LLM-backed report generator.

Supports OpenAI and Gemini. Provider chosen via app.config["LLM_PROVIDER"]
(values: "openai" or "gemini", defaults to "openai" if not set).
API keys + models are loaded from the Settings DB table by app.py at boot.
"""
from flask import current_app
from models import City, Indicator, Observation


class ReportGenerator:
    def __init__(self):
        self.provider = (current_app.config.get("LLM_PROVIDER") or "openai").lower()

        if self.provider == "openai":
            api_key = current_app.config.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not configured")
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = current_app.config.get("OPENAI_MODEL") or "gpt-4o-mini"

        elif self.provider == "gemini":
            api_key = current_app.config.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API key not configured")
            try:
                import google.generativeai as genai
            except ImportError as e:
                raise ValueError(
                    "google-generativeai package not installed. "
                    "Run: pip install google-generativeai"
                ) from e
            genai.configure(api_key=api_key)
            self.model = current_app.config.get("GEMINI_MODEL") or "gemini-1.5-flash"
            self.client = genai.GenerativeModel(self.model)

        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    def generate_dispatch_report(self, city_id):
        """Generate an executive dispatch report for a city."""
        try:
            city = City.query.get(city_id)
            if not city:
                return None, "City not found"

            indicator = Indicator.query.filter_by(city_id=city_id).order_by(Indicator.id.desc()).first()
            if not indicator:
                return None, "No indicators found for this city"

            observations = (
                Observation.query.filter_by(city_id=city_id)
                .order_by(Observation.week_label.desc())
                .limit(10)
                .all()
            )

            city_data = {
                "name": city.name,
                "state": city.state,
                "country": city.country,
                "rt": indicator.rt,
                "r0": indicator.r0,
                "hospitalization_rate": indicator.hospitalization_rate,
                "recent_cases": [obs.cases for obs in observations],
                "recent_weeks": [obs.week_label for obs in observations],
            }

            prompt = self._create_prompt(city_data)
            report_text = self._call_llm(prompt)
            return report_text, None

        except Exception as exc:
            return None, str(exc)

    # ----- provider-specific calls --------------------------------------

    def _call_llm(self, prompt: str) -> str:
        system_msg = (
            "You are a senior epidemiologist preparing an executive briefing "
            "for a city public-health director. Be concise, action-oriented, "
            "and grounded in the supplied indicators."
        )
        if self.provider == "openai":
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return resp.choices[0].message.content.strip()

        # gemini
        resp = self.client.generate_content(
            [system_msg, prompt],
            generation_config={"temperature": 0.4},
        )
        return resp.text.strip() if hasattr(resp, "text") else str(resp)

    # ----- prompt -------------------------------------------------------

    def _create_prompt(self, d: dict) -> str:
        lines = [
            f"City: {d['name']} ({d.get('state', 'n/a')}, {d.get('country', 'n/a')})",
            f"Effective reproduction number Rt: {d.get('rt')}",
            f"Basic reproduction number R0: {d.get('r0')}",
            f"Hospitalization rate: {d.get('hospitalization_rate')}",
            "Recent weekly cases:",
        ]
        for wk, c in zip(d.get("recent_weeks", []), d.get("recent_cases", [])):
            lines.append(f"  - {wk}: {c}")
        lines.append("")
        lines.append(
            "Produce a 4-section dispatch report: (1) current state, "
            "(2) trajectory in 7-14 days, (3) recommended actions for the "
            "next 72h, (4) what to monitor."
        )
        return "\n".join(lines)
