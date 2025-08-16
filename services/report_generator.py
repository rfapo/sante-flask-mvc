import os
from openai import OpenAI
from flask import current_app
from models import City, Indicator, Observation

class ReportGenerator:
    def __init__(self):
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not configured")
        
        self.client = OpenAI(api_key=api_key)
        self.model = current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')
    
    def generate_dispatch_report(self, city_id):
        """Generate an executive dispatch report for a city using OpenAI"""
        try:
            # Get city data
            city = City.query.get(city_id)
            if not city:
                return None, "City not found"
            
            # Get latest indicators
            indicator = Indicator.query.filter_by(city_id=city_id).order_by(Indicator.id.desc()).first()
            if not indicator:
                return None, "No indicators found for this city"
            
            # Get recent observations
            observations = Observation.query.filter_by(city_id=city_id).order_by(Observation.week_label.desc()).limit(10).all()
            
            # Prepare data for OpenAI
            city_data = {
                'name': city.name,
                'state': city.state,
                'country': city.country,
                'rt': indicator.rt,
                'r0': indicator.r0,
                'hospitalization_rate': indicator.hospitalization_rate,
                'recent_cases': [obs.cases for obs in observations],
                'recent_weeks': [obs.week_label for obs in observations]
            }
            
            # Create prompt for OpenAI
            prompt = self._create_prompt(city_data)
            
            # Generate report with OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert epidemiologist and public health analyst. Generate concise, professional executive reports for health officials and stakeholders."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            report = response.choices[0].message.content
            return report, None
            
        except Exception as e:
            return None, f"Error generating report: {str(e)}"
    
    def _create_prompt(self, city_data):
        """Create a detailed prompt for OpenAI based on city data"""
        risk_level = "HIGH" if city_data['rt'] > 1.2 else "MEDIUM" if city_data['rt'] > 1.0 else "LOW"
        trend = "increasing" if city_data['rt'] > 1 else "decreasing"
        
        prompt = f"""
Generate an executive dispatch report for {city_data['name']}, {city_data['state']}, {city_data['country']}.

Current Situation:
- Risk Level: {risk_level}
- R(t): {city_data['rt']} (transmission rate is {trend})
- R0: {city_data['r0']}
- Hospitalization Rate: {city_data['hospitalization_rate']}%
- Recent case trend: {city_data['recent_cases'][:5]} cases in last 5 weeks

Requirements:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-4 bullet points)
3. Risk Assessment
4. Recommendations for Public Health Officials
5. Next Steps

Format the report professionally for distribution to health authorities and stakeholders. Keep it concise but comprehensive.
        """
        return prompt.strip()
