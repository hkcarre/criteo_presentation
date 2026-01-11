"""
McKinsey Partner Agent - Strategic Insights and Recommendations
Translates data analysis into executive-ready strategic narrative
"""

import json
import pandas as pd
from datetime import datetime

class McKinseyPartnerAgent:
    """Senior McKinsey Partner for strategic synthesis"""
    
    def __init__(self, analysis_results_path, clean_data_path):
        with open(analysis_results_path, 'r') as f:
            self.results = json.load(f)
        
        self.df = pd.read_csv(clean_data_path)
        self.df['month'] = pd.to_datetime(self.df['month'])
        
        self.strategic_insights = {}
        self.recommendations = []
        
    def synthesize_executive_summary(self):
        """Create executive summary using Pyramid Principle"""
        print("="*80)
        print("MCKINSEY PARTNER - EXECUTIVE SYNTHESIS")
        print("="*80)
        
        # Top-line findings
        q1_findings = self.results['q1']['key_findings']
        current_threat = q1_findings['current_threat_pct']
        monthly_growth = q1_findings['monthly_growth_rate']
        
        q2_findings = self.results['q2']
        penetration_rate = q2_findings['penetration_rate']
        acceleration = q2_findings['acceleration_pct']
        
        q4_findings = self.results['q4']
        top_20_revenue_lost = q4_findings['top_20_revenue_lost']
        
        print(f"\n🎯 HEADLINE FINDING:")
        print(f"  Competitive threat has intensified by {monthly_growth:.1f}% month-over-month,")
        print(f"  currently eroding {current_threat:.1f}% of revenues with {penetration_rate:.0f}%")
        print(f"  client penetration and accelerating at {acceleration:+.0f}%")
        
        print(f"\n💡 THREE CRITICAL INSIGHTS:")
        print(f"  1. ESCALATING THREAT: Revenue at risk growing {monthly_growth:.1f}%/month")
        print(f"  2. ACCELERATING LAUNCHES: Competitor entry rate increased {acceleration:+.0f}%")
        print(f"  3. CONCENTRATED RISK: Top 20 clients account for €{top_20_revenue_lost:,.0f} in losses")
        
        print(f"\n⚡ PRIMARY RECOMMENDATION:")
        print(f"  Implement 3-tier defense strategy: Protect high-value accounts (Tier 1),")
        print(f"  fortify threatened segments (Tier 2), deploy early-warning system (Tier 3)")
        
        self.strategic_insights['executive_summary'] = {
            'headline': f"Competitive threat intensifying at {monthly_growth:.1f}%/month, eroding {current_threat:.1f}% of revenue",
            'key_insights': [
                f"Revenue at risk growing {monthly_growth:.1f}% monthly",
                f"Competitor launches accelerated {acceleration:+.0f}% vs. first half",
                f"Top 20 clients represent €{top_20_revenue_lost:,.0f} in losses"
            ],
            'primary_recommendation': "3-tier defense: protect, fortify, detect"
        }
        
    def analyze_strategic_implications(self):
        """Deep strategic analysis using MECE framework"""
        print("\n" + "="*80)
        print("STRATEGIC IMPLICATIONS ANALYSIS")
        print("="*80)
        
        # Market dimension analysis
        market_data = self.results['q3']['market']
        high_risk_markets = [m for m in market_data if m.get('risk_level') == 'HIGH']
        
        print(f"\n🌍 MARKET DYNAMICS:")
        print(f"  • {len(high_risk_markets)} high-risk markets identified")
        print(f"  • Geographic concentration of competitive pressure")
        for market in sorted(high_risk_markets, key=lambda x: x['threat_score'], reverse=True)[:3]:
            print(f"    - {market['market']}: {market['revenue_lost_pct']:.1f}% revenue lost")
        
        # Vertical dimension
        vertical_data = self.results['q3']['vertical']
        high_risk_verticals = [v for v in vertical_data if v.get('risk_level') == 'HIGH']
        
        print(f"\n🏭 VERTICAL VULNERABILITY:")
        print(f"  • {len(high_risk_verticals)} high-risk verticals")
        for vertical in sorted(high_risk_verticals, key=lambda x: x['threat_score'], reverse=True)[:3]:
            print(f" - {vertical['vertical']}: {vertical['revenue_lost_pct']:.1f}% revenue lost")
        
        # Client segment
        segment_data = self.results['q3']['segment']
        high_risk_segments = [s for s in segment_data if s.get('risk_level') == 'HIGH']
        
        print(f"\n📊 SEGMENT EXPOSURE:")
        print(f"  • {len(high_risk_segments)} high-risk segments")
        for segment in sorted(high_risk_segments, key=lambda x: x['threat_score'], reverse=True)[:3]:
            print(f"    - {segment['segment']}: {segment['revenue_lost_pct']:.1f}% revenue lost")
        
        self.strategic_insights['implications'] = {
            'high_risk_markets': len(high_risk_markets),
            'high_risk_verticals': len(high_risk_verticals),
            'high_risk_segments': len(high_risk_segments)
        }
        
    def develop_recommendations(self):
        """Develop actionable CEO recommendations"""
        print("\n" + "="*80)
        print("CEO RECOMMENDATIONS")
        print("="*80)
        
        # Recommendation 1: Protect High-Value Clients
        print(f"\n💼 RECOMMENDATION 1: PROTECT HIGH-VALUE CLIENTS")
        print(f"  Why: Top 20 clients account for €{self.results['q4']['top_20_revenue_lost']:,.0f} in losses")
        print(f"  Action: Dedicated account teams, competitive intelligence, value-add services")
        print(f"  Timeline: Immediate (30 days)")
        print(f"  Impact: Retain 50-70% of at-risk revenue (~€{self.results['q4']['top_20_revenue_lost']*0.6:,.0f})")
        
        self.recommendations.append({
            'rank': 1,
            'title': 'Protect High-Value Clients',
            'rationale': f"Top 20 clients represent €{self.results['q4']['top_20_revenue_lost']:,.0f} in losses",
            'actions': [
                'Deploy dedicated senior account teams for top 20 clients',
                'Conduct competitive intelligence on client-specific threats',
                'Develop customized value propositions and exclusive features'
            ],
            'timeline': '30 days',
            'estimated_impact': f"€{self.results['q4']['top_20_revenue_lost']*0.6:,.0f} revenue protected"
        })
        
        # Recommendation 2: Fortify Threatened Segments
        print(f"\n🛡️ RECOMMENDATION 2: FORTIFY THREATENED SEGMENTS")
        print(f"  Why: Systematic vulnerabilities in {len(self.results['q3']['market'])} markets")
        print(f"  Action: Segment-specific competitive responses, pricing optimization")
        print(f"  Timeline: 90 days")
        print(f"  Impact: Slow market share erosion by 30-40%")
        
        self.recommendations.append({
            'rank': 2,
            'title': 'Fortify Threatened Segments',
            'rationale': 'Systematic vulnerabilities across markets and verticals',
            'actions': [
                'Design market-specific competitive responses',
                'Optimize pricing and packaging for at-risk verticals',
                'Accelerate product roadmap for high-threat segments'
            ],
            'timeline': '90 days',
            'estimated_impact': 'Reduce market share loss by 30-40%'
        })
        
        # Recommendation 3: Deploy Early Warning System
        print(f"\n🚨 RECOMMENDATION 3: DEPLOY EARLY WARNING SYSTEM")
        print(f"  Why: {self.results['q2']['acceleration_pct']:+.0f}% acceleration in competitor launches")
        print(f"  Action: Automated alert system for commercial teams (detailed in Q6)")
        print(f"  Timeline: 60 days")
        print(f"  Impact: Reduce response time from weeks to hours")
        
        self.recommendations.append({
            'rank': 3,
            'title': 'Deploy Early Warning System',
            'rationale': f"{self.results['q2']['acceleration_pct']:+.0f}% acceleration in competitor activity",
            'actions': [
                'Implement automated competitor detection system',
                'Real-time alerts to commercial teams',
                'Playbook for rapid response protocols'
            ],
            'timeline': '60 days',
            'estimated_impact': 'Reduce response time from weeks to 24-48 hours'
        })
        
        # Recommendation 4: Differentiate Core Offering
        print(f"\n⭐ RECOMMENDATION 4: ACCELERATE PRODUCT DIFFERENTIATION")
        print(f"  Why: {self.results['q2']['penetration_rate']:.0f}% client penetration indicates feature parity")
        print(f"  Action: Unique value propositions, exclusive capabilities")
        print(f"  Timeline: 6-12 months")
        print(f"  Impact: Create sustainable competitive moat")
        
        self.recommendations.append({
            'rank': 4,
            'title': 'Accelerate Product Differentiation',
            'rationale': f"{self.results['q2']['penetration_rate']:.0f}% penetration suggests commoditization risk",
            'actions': [
                'Develop exclusive capabilities competitors can\'t easily replicate',
                'Build ecosystem lock-in through integrations',
                'Investment in R&D for breakthrough innovations'
            ],
            'timeline': '6-12 months',
            'estimated_impact': 'Create sustainable 18-24 month competitive advantage'
        })
        
        # Recommendation 5: Strategic Resource Reallocation
        print(f"\n💰 RECOMMENDATION 5: REALLOCATE RESOURCES TO DEFENSE")
        print(f"  Why: Current losses justify defensive investment")
        print(f"  Action: Shift 15-20% of growth budget to retention/defense")
        print(f"  Timeline: Immediate")
        print(f"  Impact: Better ROI than new customer acquisition in high-threat segments")
        
        self.recommendations.append({
            'rank': 5,
            'title': 'Strategic Resource Reallocation',
            'rationale': 'Retention ROI exceeds acquisition in threatened segments',
            'actions': [
                'Redeploy 15-20% of growth budget to client defense',
                'Prioritize retention metrics in incentive structures',
                'Invest in competitive intelligence capabilities'
            ],
            'timeline': 'Immediate',
            'estimated_impact': '2-3x ROI vs. new customer acquisition'
        })
        
    def design_alert_system(self):
        """Design the alert system (Q6)"""
        print("\n" + "="*80)
        print("ALERT SYSTEM DESIGN (Question 6)")
        print("="*80)
        
        alert_system = {
            'metrics': [
                {
                    'name': 'Competitor First Touch',
                    'def': 'First instance of competitor_clicks > 0 for a client',
                    'why': 'Earliest possible warning signal'
                },
                {
                    'name': 'Click Share Delta',
                    'def': 'Change in competitor/(competitor + Criteo) clicks',
                    'why': 'Measures competitive pressure intensity'
                },
                {
                    'name': 'Revenue Velocity',
                    'def': '% change in monthly revenue (3-month rolling)',
                    'why': 'Leading indicator of client health'
                }
            ],
            'decision_logic': {
                'P1_Critical': {
                    'conditions': 'High-value client (>€100k/month) + First Touch OR Click Share >20% OR Revenue decline >15%',
                    'response_sla': '24 hours',
                    'owner': 'Senior Account Director'
                },
                'P2_High': {
                    'conditions': 'Medium-value client + First Touch OR Click Share 10-20% OR Revenue decline 10-15%',
                    'response_sla': '72 hours',
                    'owner': 'Account Manager'
                },
                'P3_Monitor': {
                    'conditions': 'Any client + First Touch OR Click Share 5-10%',
                    'response_sla': '1 week',
                    'owner': 'Commercial Team (dashboard review)'
                }
            },
            'delivery': {
                'P1': ['Email (immediate)', 'Slack (real-time)', 'Dashboard (flagged)'],
                'P2': ['Email (daily digest)', 'Dashboard (flagged)'],
                'P3': ['Dashboard only']
            },
            'effectiveness_metrics': [
                'Alert Precision: % of alerts leading to action',
                'Response Time: Hours from alert to account contact',
                'Revenue Saved: $ retained after alert-triggered intervention',
                'False Positive Rate: % of alerts with no competitive threat'
            ]
        }
        
        print("\n📊 METRICS:")
        for m in alert_system['metrics']:
            print(f"  • {m['name']}: {m['def']}")
            print(f"    Why: {m['why']}")
        
        print("\n🎯 DECISION LOGIC:")
        for priority, logic in alert_system['decision_logic'].items():
            print(f"  {priority}:")
            print(f"    Conditions: {logic['conditions']}")
            print(f"    SLA: {logic['response_sla']}")
            print(f"    Owner: {logic['owner']}")
        
        print("\n📬 DELIVERY CHANNELS:")
        for priority, channels in alert_system['delivery'].items():
            print(f"  {priority}: {', '.join(channels)}")
        
        print("\n📈 EFFECTIVENESS MEASUREMENT:")
        for metric in alert_system['effectiveness_metrics']:
            print(f"  • {metric}")
        
        self.strategic_insights['alert_system'] = alert_system
        
    def save_strategic_insights(self):
        """Save strategic synthesis"""
        with open('strategic_insights.json', 'w') as f:
            json.dump({
                'insights': self.strategic_insights,
                'recommendations': self.recommendations
            }, f, indent=2)
        
        print(f"\n✅ Strategic insights saved to strategic_insights.json")

if __name__ == "__main__":
    partner = McKinseyPartnerAgent('analysis_results.json', 'CASE_STUDY_CLEAN.csv')
    
    # Strategic synthesis
    partner.synthesize_executive_summary()
    partner.analyze_strategic_implications()
    partner.develop_recommendations()
    partner.design_alert_system()
    
    # Save insights
    partner.save_strategic_insights()
    
    print("\n" + "="*80)
    print("✅ STRATEGIC SYNTHESIS COMPLETE")
    print("="*80)
