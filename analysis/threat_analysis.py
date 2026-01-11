"""
Competitive Threat Analysis - All 6 Questions
Data Scientist Agent performing statistical analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class ThreatAnalyzer:
    """Comprehensive threat analysis for all case study questions"""
    
    def __init__(self, clean_data_path):
        self.df = pd.read_csv(clean_data_path)
        self.df['month'] = pd.to_datetime(self.df['month'])
        self.results = {}
        
    def question_1_threat_evolution(self):
        """Q1: How has competitive threat evolved? Choose and justify metric"""
        print("="*80)
        print("QUESTION 1: COMPETITIVE THREAT EVOLUTION")
        print("="*80)
        
        # Aggregate by month
        monthly = self.df.groupby('month').agg({
            'estimated_revenue_lost': 'sum',
            'revenue_euro': 'sum',
            'competitor_clicks': 'sum',
            'criteo_clicks': 'sum',
            'client_id': 'nunique'
        }).reset_index()
        
        # Calculate candidate metrics
        monthly['revenue_lost_pct'] = (monthly['estimated_revenue_lost'] / monthly['revenue_euro']) * 100
        monthly['competitor_click_share'] = (monthly['competitor_clicks'] / 
                                             (monthly['competitor_clicks'] + monthly['criteo_clicks'])) * 100
        
        # Calculate trends
        first_month = monthly.iloc[0]
        last_month = monthly.iloc[-1]
        months_diff = len(monthly) - 1
        
        metrics_comparison = {
            'Absolute Revenue Lost (€)': {
                'first_month': first_month['estimated_revenue_lost'],
                'last_month': last_month['estimated_revenue_lost'],
                'change': last_month['estimated_revenue_lost'] - first_month['estimated_revenue_lost'],
                'change_pct': ((last_month['estimated_revenue_lost'] / first_month['estimated_revenue_lost']) - 1) * 100,
                'total': monthly['estimated_revenue_lost'].sum(),
                'pros': ['Easy to understand', 'Direct financial impact', 'Aligns with CEO priorities'],
                'cons': ['Affected by business growth', 'May hide relative impact']
            },
            'Revenue Lost as % of Total Revenue': {
                'first_month': first_month['revenue_lost_pct'],
                'last_month': last_month['revenue_lost_pct'],
                'change': last_month['revenue_lost_pct'] - first_month['revenue_lost_pct'],
                'change_pct': ((last_month['revenue_lost_pct'] / first_month['revenue_lost_pct']) - 1) * 100,
                'avg': monthly['revenue_lost_pct'].mean(),
                'pros': ['Controls for business size', 'Shows relative threat intensity', 'Better for cross-period comparison'],
                'cons': ['Less intuitive than absolute numbers']
            },
            'Competitor Click Share (%)': {
                'first_month': first_month['competitor_click_share'],
                'last_month': last_month['competitor_click_share'],
                'change': last_month['competitor_click_share'] - first_month['competitor_click_share'],
                'change_pct': ((last_month['competitor_click_share'] / first_month['competitor_click_share']) - 1) * 100,
                'avg': monthly['competitor_click_share'].mean(),
                'pros': ['Measures market share loss', 'Leading indicator', 'Operational metric'],
                'cons': ['Indirect financial impact', 'Calculation based on estimates']
            }
        }
        
        print("\n📊 METRIC COMPARISON:")
        for metric, data in metrics_comparison.items():
            print(f"\n{metric}:")
            print(f"  First month: {data['first_month']:,.2f}")
            print(f"  Last month: {data['last_month']:,.2f}")
            print(f"  Change: {data['change']:,.2f} ({data['change_pct']:,.1f}%)")
        
        # RECOMMENDED METRIC
        recommended = "Revenue Lost as % of Total Revenue"
        print(f"\n🎯 RECOMMENDED METRIC: {recommended}")
        print(f"\nJustification:")
        print(f"  ✓ Controls for business growth/seasonality")
        print(f"  ✓ Enables apples-to-apples comparison across time")
        print(f"  ✓ Shows true competitive pressure intensity")
        print(f"  ✓ Can be benchmarked across markets/verticals")
        
        # Trend analysis
        monthly['trend_ma3'] = monthly['revenue_lost_pct'].rolling(window=3).mean()
        
        # Calculate CAGR-like growth
        n_months = len(monthly) - 1
        cagr = ((last_month['revenue_lost_pct'] / first_month['revenue_lost_pct']) ** (1/n_months) - 1) * 100
        
        print(f"\n📈 THREAT EVOLUTION:")
        print(f"  Monthly growth rate: {cagr:.2f}%")
        print(f"  Total increase: {last_month['revenue_lost_pct'] - first_month['revenue_lost_pct']:.2f} percentage points")
        print(f"  Peak threat: {monthly['revenue_lost_pct'].max():.2f}% ({monthly[monthly['revenue_lost_pct'] == monthly['revenue_lost_pct'].max()]['month'].values[0]})")
        
        self.results['q1'] = {
            'metrics_comparison': metrics_comparison,
            'recommended_metric': recommended,
            'monthly_data': monthly.to_dict('records'),
            'key_findings': {
                'monthly_growth_rate': cagr,
                'total_increase_pp': last_month['revenue_lost_pct'] - first_month['revenue_lost_pct'],
                'peak_threat_pct': monthly['revenue_lost_pct'].max(),
                'current_threat_pct': last_month['revenue_lost_pct']
            }
        }
        
        return monthly
    
    def question_2_competitor_launches(self):
        """Q2: How do competitor launches evolve over time?"""
        print("\n" + "="*80)
        print("QUESTION 2: COMPETITOR LAUNCH DYNAMICS")
        print("="*80)
        
        # Identify first appearance of competitor for each client
        # Competitor present = competitor_clicks > 0
        df_with_competitor = self.df[self.df['competitor_clicks'] > 0].copy()
        
        # Find first month with competitor for each client
        first_appearance = df_with_competitor.groupby('client_id')['month'].min().reset_index()
        first_appearance.columns = ['client_id', 'first_competitor_month']
        
        # Count launches by month
        launches_by_month = first_appearance.groupby('first_competitor_month').size().reset_index()
        launches_by_month.columns = ['month', 'new_launches']
        
        # Calculate cumulative launches
        launches_by_month = launches_by_month.sort_values('month')
        launches_by_month['cumulative_launches'] = launches_by_month['new_launches'].cumsum()
        
        # Calculate moving average
        launches_by_month['ma3'] = launches_by_month['new_launches'].rolling(window=3, min_periods=1).mean()
        
        print(f"\n📊 COMPETITOR LAUNCH STATISTICS:")
        print(f"  Total clients with competitor: {len(first_appearance):,}")
        print(f"  Total clients: {self.df['client_id'].nunique():,}")
        print(f"  Penetration rate: {(len(first_appearance) / self.df['client_id'].nunique()) * 100:.1f}%")
        print(f"\n  First launch detected: {launches_by_month['month'].min()}")
        print(f"  Latest launch detected: {launches_by_month['month'].max()}")
        print(f"  Average launches per month: {launches_by_month['new_launches'].mean():.1f}")
        print(f"  Peak month: {launches_by_month[launches_by_month['new_launches'] == launches_by_month['new_launches'].max()]['month'].values[0]} ({launches_by_month['new_launches'].max()} launches)")
        
        # Acceleration analysis
        first_half = launches_by_month.head(len(launches_by_month)//2)
        second_half = launches_by_month.tail(len(launches_by_month)//2)
        
        acceleration = (second_half['new_launches'].mean() / first_half['new_launches'].mean() - 1) * 100
        print(f"\n📈 ACCELERATION:")
        print(f"  First half avg: {first_half['new_launches'].mean():.1f} launches/month")
        print(f"  Second half avg: {second_half['new_launches'].mean():.1f} launches/month")
        print(f"  Acceleration: {acceleration:+.1f}%")
        
        self.results['q2'] = {
            'total_clients_with_competitor': len(first_appearance),
            'penetration_rate': (len(first_appearance) / self.df['client_id'].nunique()) * 100,
            'avg_launches_per_month': launches_by_month['new_launches'].mean(),
            'peak_launches': int(launches_by_month['new_launches'].max()),
            'acceleration_pct': acceleration,
            'launches_by_month': launches_by_month.to_dict('records')
        }
        
        return launches_by_month
    
    def question_3_segment_analysis(self):
        """Q3: Which Markets/Verticals/Segments are most threatened?"""
        print("\n" + "="*80)
        print("QUESTION 3: SEGMENT RISK ANALYSIS")
        print("="*80)
        
        results = {}
        
        for dimension in ['market', 'vertical', 'segment']:
            print(f"\n📊 {dimension.upper()} ANALYSIS:")
            
            segment_stats = self.df.groupby(dimension).agg({
                'estimated_revenue_lost': 'sum',
                'revenue_euro': 'sum',
                'competitor_clicks': 'sum',
                'criteo_clicks': 'sum',
                'client_id': 'nunique'
            }).reset_index()
            
            # Calculate threat metrics
            segment_stats['revenue_lost_pct'] = (segment_stats['estimated_revenue_lost'] / 
                                                  segment_stats['revenue_euro']) * 100
            segment_stats['competitor_share'] = (segment_stats['competitor_clicks'] / 
                                                 (segment_stats['competitor_clicks'] + segment_stats['criteo_clicks'])) * 100
            
            # Calculate threat score (composite)
            # Normalize metrics to 0-100 scale
            segment_stats['revenue_lost_pct_norm'] = (segment_stats['revenue_lost_pct'] / 
                                                       segment_stats['revenue_lost_pct'].max()) * 100
            segment_stats['competitor_share_norm'] = (segment_stats['competitor_share'] / 
                                                      segment_stats['competitor_share'].max()) * 100
            
            # Weighted threat score (60% revenue lost, 40% competitor share)
            segment_stats['threat_score'] = (segment_stats['revenue_lost_pct_norm'] * 0.6 + 
                                             segment_stats['competitor_share_norm'] * 0.4)
            
            # Sort by threat score
            segment_stats = segment_stats.sort_values('threat_score', ascending=False)
            
            # Calculate average
            avg_revenue_lost_pct = segment_stats['revenue_lost_pct'].mean()
            avg_threat_score = segment_stats['threat_score'].mean()
            
            # Flag high-risk segments (above average)
            segment_stats['risk_level'] = segment_stats.apply(
                lambda x: 'HIGH' if x['threat_score'] > avg_threat_score * 1.2 
                else ('MEDIUM' if x['threat_score'] > avg_threat_score * 0.8 else 'LOW'),
                axis=1
            )
            
            high_risk = segment_stats[segment_stats['risk_level'] == 'HIGH']
            
            print(f"\n  Average Revenue Lost: {avg_revenue_lost_pct:.2f}%")
            print(f"  High-Risk {dimension}s: {len(high_risk)}")
            print(f"\n  Top 5 Most Threatened:")
            for idx, row in segment_stats.head(5).iterrows():
                print(f"    {row[dimension]}: {row['revenue_lost_pct']:.2f}% revenue lost, "
                      f"Threat Score: {row['threat_score']:.1f}/100, Risk: {row['risk_level']}")
            
            results[dimension] = segment_stats.to_dict('records')
        
        self.results['q3'] = results
        return results
    
    def question_4_client_attention(self):
        """Q4: Which clients need particular attention?"""
        print("\n" + "="*80)
        print("QUESTION 4: HIGH-RISK CLIENT IDENTIFICATION")
        print("="*80)
        
        # Aggregate by client
        client_stats = self.df.groupby('client_id').agg({
            'estimated_revenue_lost': 'sum',
            'revenue_euro': 'sum',
            'competitor_clicks': 'sum',
            'criteo_clicks': 'sum',
            'month': ['min', 'max', 'nunique']
        }).reset_index()
        
        client_stats.columns = ['client_id', 'revenue_lost', 'revenue', 'competitor_clicks', 
                                'criteo_clicks', 'first_month', 'last_month', 'months_active']
        
        # Calculate risk factors
        client_stats['revenue_lost_pct'] = (client_stats['revenue_lost'] / client_stats['revenue']) * 100
        client_stats['competitor_share'] = (client_stats['competitor_clicks'] / 
                                            (client_stats['competitor_clicks'] + client_stats['criteo_clicks'])) * 100
        
        # Revenue concentration (% of total Criteo revenue)
        total_revenue = client_stats['revenue'].sum()
        client_stats['revenue_concentration'] = (client_stats['revenue'] / total_revenue) * 100
        
        # Trend analysis - compare first 3 months vs last 3 months
        def calculate_trend(client_id):
            client_data = self.df[self.df['client_id'] == client_id].sort_values('month')
            if len(client_data) < 6:
                return 0
            
            first_3 = client_data.head(3)['estimated_revenue_lost'].sum()
            last_3 = client_data.tail(3)['estimated_revenue_lost'].sum()
            
            if first_3 == 0:
                return 100 if last_3 > 0 else 0
            
            return ((last_3 / first_3) - 1) * 100
        
        client_stats['trend_pct'] = client_stats['client_id'].apply(calculate_trend)
        
        # Multi-factor risk score
        # Normalize each component
        client_stats['revenue_lost_norm'] = (client_stats['revenue_lost'] / client_stats['revenue_lost'].max()) * 100
        client_stats['revenue_lost_pct_norm'] = (client_stats['revenue_lost_pct'] / client_stats['revenue_lost_pct'].max()) * 100
        client_stats['concentration_norm'] = (client_stats['revenue_concentration'] / client_stats['revenue_concentration'].max()) * 100
        client_stats['trend_norm'] = np.clip((client_stats['trend_pct'] / 100) * 100, 0, 100)  # Cap at 100
        
        # Weighted risk score
        # 40% absolute revenue lost, 30% revenue concentration, 20% trend, 10% revenue lost %
        client_stats['risk_score'] = (
            client_stats['revenue_lost_norm'] * 0.40 +
            client_stats['concentration_norm'] * 0.30 +
            client_stats['trend_norm'] * 0.20 +
            client_stats['revenue_lost_pct_norm'] * 0.10
        )
        
        # Sort by risk score
        client_stats = client_stats.sort_values('risk_score', ascending=False)
        
        # Top 20 clients
        top_20 = client_stats.head(20)
        
        print(f"\n📊 CLIENT RISK OVERVIEW:")
        print(f"  Total clients analyzed: {len(client_stats):,}")
        print(f"  Average revenue lost per client: €{client_stats['revenue_lost'].mean():,.2f}")
        print(f"  Median revenue lost %: {client_stats['revenue_lost_pct'].median():.2f}%")
        
        print(f"\n🚨 TOP 20 HIGH-RISK CLIENTS:")
        print(f"{'Rank':<6}{'Client ID':<15}{'Revenue Lost':<18}{'Lost %':<10}{'Concentration':<15}{'Trend':<12}{'Risk Score':<12}")
        print("-" * 95)
        
        for idx, (i, row) in enumerate(top_20.iterrows(), 1):
            print(f"{idx:<6}{row['client_id']:<15}€{row['revenue_lost']:>10,.0f}     "
                  f"{row['revenue_lost_pct']:>6.1f}%    {row['revenue_concentration']:>6.2f}%        "
                  f"{row['trend_pct']:>+6.0f}%      {row['risk_score']:>6.1f}/100")
        
        # Insights
        high_concentration = top_20[top_20['revenue_concentration'] > 1.0]
        deteriorating = top_20[top_20['trend_pct'] > 50]
        
        print(f"\n📌 KEY INSIGHTS:")
        print(f"  • {len(high_concentration)} of top 20 are high-value clients (>1% of total revenue)")
        print(f"  • {len(deteriorating)} showing rapid deterioration (>50% trend increase)")
        print(f"  • Top 20 represent €{top_20['revenue_lost'].sum():,.2f} in lost revenue")
        
        self.results['q4'] = {
            'top_20_clients': top_20.to_dict('records'),
            'total_clients': len(client_stats),
            'high_concentration_count': len(high_concentration),
            'deteriorating_count': len(deteriorating),
            'top_20_revenue_lost': top_20['revenue_lost'].sum()
        }
        
        return top_20
    
    def save_results(self, filepath='analysis_results.json'):
        """Save all analysis results"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n✅ Results saved to {filepath}")

if __name__ == "__main__":
    analyzer = ThreatAnalyzer('CASE_STUDY_CLEAN.csv')
    
    # Run all analyses
    q1 = analyzer.question_1_threat_evolution()
    q2 = analyzer.question_2_competitor_launches()
    q3 = analyzer.question_3_segment_analysis()
    q4 = analyzer.question_4_client_attention()
    
    # Save results
    analyzer.save_results('analysis_results.json')
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
