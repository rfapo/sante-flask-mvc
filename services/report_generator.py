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
    
    def process_kepler_data(self, raw_data, city, indicator):
        """Process epidemiological data with OpenAI to enhance it for Kepler.gl visualization"""
        try:
            # Prepare data summary for OpenAI
            data_summary = {
                'city_name': city.name,
                'state': city.state,
                'country': city.country,
                'rt': indicator.rt,
                'r0': indicator.r0,
                'hospitalization_rate': indicator.hospitalization_rate,
                'data_points': len(raw_data),
                'coordinate_range': {
                    'lat_min': min(d['latitude'] for d in raw_data),
                    'lat_max': max(d['latitude'] for d in raw_data),
                    'lon_min': min(d['longitude'] for d in raw_data),
                    'lon_max': max(d['longitude'] for d in raw_data)
                }
            }
            
            # Create prompt for OpenAI
            prompt = self._create_kepler_prompt(raw_data, data_summary)
            
            # Generate enhanced data with OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data scientist specializing in geospatial data visualization. Your task is to enhance epidemiological data for optimal display in Kepler.gl mapping software."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Parse the response and return enhanced data
            enhanced_data = self._parse_kepler_response(response.choices[0].message.content, raw_data)
            return enhanced_data, None
            
        except Exception as e:
            return None, f"Error processing data with OpenAI: {str(e)}"
    
    def _create_kepler_prompt(self, raw_data, data_summary):
        """Create a prompt for OpenAI to enhance Kepler.gl data"""
        prompt = f"""
You are processing epidemiological data for visualization in Kepler.gl, a powerful geospatial mapping tool.

Current Data Summary:
- City: {data_summary['city_name']}, {data_summary['state']}, {data_summary['country']}
- R(t): {data_summary['rt']} (transmission rate)
- R0: {data_summary['r0']} (basic reproduction number)
- Hospitalization Rate: {data_summary['hospitalization_rate']}%
- Data Points: {data_summary['data_points']} weeks
- Coordinate Range: Lat {data_summary['coordinate_range']['lat_min']:.4f} to {data_summary['coordinate_range']['lat_max']:.4f}, Lon {data_summary['coordinate_range']['lon_min']:.4f} to {data_summary['coordinate_range']['lon_max']:.4f}

Raw Data Sample (first 3 entries):
{raw_data[:3]}

Your Task:
Enhance this data for optimal visualization in Kepler.gl by:

1. **Data Validation**: Ensure all coordinates are valid and within reasonable ranges
2. **Data Enhancement**: Add derived fields that would be useful for mapping:
   - risk_level: "HIGH" (R(t) > 1.2), "MEDIUM" (R(t) > 1.0), "LOW" (R(t) ≤ 1.0)
   - case_density: cases per week normalized to a 0-1 scale
   - trend_indicator: "increasing", "stable", or "decreasing" based on case trends
   - severity_score: combined score based on R(t), R0, and hospitalization rate
3. **Geospatial Optimization**: Ensure coordinates are precise and suitable for mapping
4. **Data Consistency**: Verify all required fields are present and properly formatted

Return the enhanced data as a JSON array with the same structure as the input, plus the new derived fields. Maintain the exact same data types and ensure all coordinates are valid decimal degrees.

Example output format:
[
  {{
    "week": "Week 1",
    "cases": 150,
    "city_name": "City Name",
    "state": "State",
    "country": "Country",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "rt": 1.15,
    "r0": 2.5,
    "hospitalization_rate": 3.2,
    "risk_level": "MEDIUM",
    "case_density": 0.75,
    "trend_indicator": "increasing",
    "severity_score": 0.68
  }}
]

Ensure the response is valid JSON that can be parsed directly.
        """
        return prompt.strip()
    
    def _parse_kepler_response(self, openai_response, original_data):
        """Parse OpenAI response and merge with original data"""
        try:
            import json
            
            # Try to extract JSON from the response
            response_text = openai_response.strip()
            
            # Find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                enhanced_data = json.loads(json_str)
                
                # Validate and merge with original data
                if len(enhanced_data) == len(original_data):
                    return enhanced_data
                else:
                    # If parsing fails, return original data with basic enhancements
                    return self._enhance_data_basic(original_data)
            else:
                # If no JSON found, return original data with basic enhancements
                return self._enhance_data_basic(original_data)
                
        except (json.JSONDecodeError, KeyError, IndexError):
            # If parsing fails, return original data with basic enhancements
            return self._enhance_data_basic(original_data)
    
    def _enhance_data_basic(self, original_data):
        """Add basic enhancements to data if OpenAI processing fails"""
        enhanced_data = []
        
        for i, entry in enumerate(original_data):
            # Calculate basic derived fields
            risk_level = "HIGH" if entry['rt'] > 1.2 else "MEDIUM" if entry['rt'] > 1.0 else "LOW"
            
            # Calculate case density (normalized to 0-1 scale)
            max_cases = max(d['cases'] for d in original_data)
            case_density = entry['cases'] / max_cases if max_cases > 0 else 0
            
            # Determine trend indicator
            if i > 0:
                trend = "increasing" if entry['cases'] > original_data[i-1]['cases'] else "decreasing" if entry['cases'] < original_data[i-1]['cases'] else "stable"
            else:
                trend = "stable"
            
            # Calculate severity score (0-1 scale)
            rt_score = min(entry['rt'] / 3.0, 1.0)  # Normalize R(t) to 0-1
            r0_score = min(entry['r0'] / 5.0, 1.0)  # Normalize R0 to 0-1
            hosp_score = min(entry['hospitalization_rate'] / 10.0, 1.0)  # Normalize hospitalization to 0-1
            severity_score = (rt_score + r0_score + hosp_score) / 3
            
            enhanced_entry = entry.copy()
            enhanced_entry.update({
                'risk_level': risk_level,
                'case_density': round(case_density, 3),
                'trend_indicator': trend,
                'severity_score': round(severity_score, 3)
            })
            
            enhanced_data.append(enhanced_entry)
        
        return enhanced_data
