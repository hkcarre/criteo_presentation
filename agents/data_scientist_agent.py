"""
Data Scientist Agent - Comprehensive Data Analysis
Performs statistical analysis, anomaly detection, and predictive modeling
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataScientistAgent:
    """Senior Data Scientist Agent for competitive threat analysis"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.clean_df = None
        self.anomalies = []
        self.quality_report = {}
        
    def load_and_profile_data(self):
        """Load data and perform comprehensive profiling"""
        print("="*80)
        print("DATA SCIENTIST AGENT - DATA PROFILING")
        print("="*80)
        
        # Load data
        self.df = pd.read_csv(self.data_path)
        
        # Basic info
        print(f"\n📊 Dataset Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        print(f"\n📋 Columns: {self.df.columns.tolist()}")
        
        # Data types
        print(f"\n🔍 Data Types:")
        print(self.df.dtypes)
        
        # Missing values
        print(f"\n❓ Missing Values:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing'] > 0])
        
        # Unique values
        print(f"\n🔢 Unique Values per Column:")
        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            print(f"  {col}: {unique_count:,} unique values")
        
        # Date range
        if 'month' in self.df.columns:
            self.df['month'] = pd.to_datetime(self.df['month'])
            print(f"\n📅 Date Range: {self.df['month'].min()} to {self.df['month'].max()}")
            print(f"   Total months: {self.df['month'].nunique()}")
        
        # Categorical breakdowns
        categorical_cols = ['Market', 'Vertical', 'Segment']
        for col in categorical_cols:
            if col in self.df.columns:
                print(f"\n📊 {col} Distribution:")
                print(self.df[col].value_counts().head(10))
        
        return self.df
    
    def detect_anomalies(self):
        """Detect anomalies using statistical methods"""
        print("\n" + "="*80)
        print("ANOMALY DETECTION")
        print("="*80)
        
        anomalies_detected = []
        
        # Check for negative revenues
        if 'revenue' in self.df.columns:
            neg_revenue = self.df[self.df['revenue'] < 0]
            if len(neg_revenue) > 0:
                anomaly = {
                    'type': 'Negative Revenue',
                    'count': len(neg_revenue),
                    'severity': 'HIGH',
                    'action': 'EXCLUDE',
                    'details': f"Found {len(neg_revenue)} records with negative revenue"
                }
                anomalies_detected.append(anomaly)
                print(f"\n⚠️  {anomaly['details']}")
        
        # Check for zero or negative clicks
        for col in ['criteo_clicks', 'competitor_clicks']:
            if col in self.df.columns:
                zero_clicks = self.df[self.df[col] < 0]
                if len(zero_clicks) > 0:
                    anomaly = {
                        'type': f'Negative {col}',
                        'count': len(zero_clicks),
                        'severity': 'HIGH',
                        'action': 'EXCLUDE',
                        'details': f"Found {len(zero_clicks)} records with negative {col}"
                    }
                    anomalies_detected.append(anomaly)
                    print(f"\n⚠️  {anomaly['details']}")
        
        # Check for outliers using IQR method
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['Unnamed: 0', 'client_id']:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                if len(outliers) > 0:
                    outlier_pct = (len(outliers) / len(self.df)) * 100
                    if outlier_pct > 0.1:  # Report if > 0.1%
                        anomaly = {
                            'type': f'Outliers in {col}',
                            'count': len(outliers),
                            'severity': 'MEDIUM',
                            'action': 'INVESTIGATE',
                            'details': f"{len(outliers)} outliers ({outlier_pct:.2f}%) in {col}"
                        }
                        anomalies_detected.append(anomaly)
                        print(f"\n📊 {anomaly['details']}")
        
        # Check for data consistency
        if 'revenue' in self.df.columns and 'revenue_per_click' in self.df.columns and 'criteo_clicks' in self.df.columns:
            # Calculate expected revenue
            self.df['expected_revenue'] = self.df['revenue_per_click'] * self.df['criteo_clicks']
            # Allow 1% tolerance for rounding
            inconsistent = self.df[
                (self.df['revenue'] > 0) & 
                (abs(self.df['revenue'] - self.df['expected_revenue']) / self.df['revenue'] > 0.01)
            ]
            if len(inconsistent) > 0:
                anomaly = {
                    'type': 'Revenue Calculation Inconsistency',
                    'count': len(inconsistent),
                    'severity': 'HIGH',
                    'action': 'INVESTIGATE',
                    'details': f"{len(inconsistent)} records where revenue ≠ RPC × clicks"
                }
                anomalies_detected.append(anomaly)
                print(f"\n⚠️  {anomaly['details']}")
        
        self.anomalies = anomalies_detected
        
        print(f"\n📋 Total Anomalies Detected: {len(anomalies_detected)}")
        return anomalies_detected
    
    def clean_data(self):
        """Clean data based on anomaly detection"""
        print("\n" + "="*80)
        print("DATA CLEANING")
        print("="*80)
        
        self.clean_df = self.df.copy()
        original_count = len(self.clean_df)
        
        # Remove negative revenues
        if 'revenue' in self.clean_df.columns:
            self.clean_df = self.clean_df[self.clean_df['revenue'] >= 0]
            print(f"✓ Removed {original_count - len(self.clean_df)} records with negative revenue")
        
        # Remove negative clicks
        for col in ['criteo_clicks', 'competitor_clicks']:
            if col in self.clean_df.columns:
                before = len(self.clean_df)
                self.clean_df = self.clean_df[self.clean_df[col] >= 0]
                removed = before - len(self.clean_df)
                if removed > 0:
                    print(f"✓ Removed {removed} records with negative {col}")
        
        # Remove rows with critical missing values
        critical_cols = ['month', 'client_id', 'Market', 'revenue']
        for col in critical_cols:
            if col in self.clean_df.columns:
                before = len(self.clean_df)
                self.clean_df = self.clean_df[self.clean_df[col].notna()]
                removed = before - len(self.clean_df)
                if removed > 0:
                    print(f"✓ Removed {removed} records with missing {col}")
        
        # Fill missing values in non-critical numeric columns with 0
        numeric_cols = self.clean_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.clean_df[col].isnull().sum() > 0:
                self.clean_df[col].fillna(0, inplace=True)
                print(f"✓ Filled missing values in {col} with 0")
        
        final_count = len(self.clean_df)
        removed_total = original_count - final_count
        removed_pct = (removed_total / original_count) * 100
        
        print(f"\n📊 Cleaning Summary:")
        print(f"   Original records: {original_count:,}")
        print(f"   Clean records: {final_count:,}")
        print(f"   Removed: {removed_total:,} ({removed_pct:.2f}%)")
        
        self.quality_report['original_records'] = original_count
        self.quality_report['clean_records'] = final_count
        self.quality_report['removed_records'] = removed_total
        self.quality_report['removed_percentage'] = removed_pct
        
        return self.clean_df
    
    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        print("\n" + "="*80)
        print("SUMMARY STATISTICS (CLEAN DATA)")
        print("="*80)
        
        print("\n📊 Numeric Columns:")
        print(self.clean_df.describe())
        
        # Revenue statistics
        if 'revenue' in self.clean_df.columns:
            print(f"\n💰 Revenue Statistics:")
            print(f"   Total Revenue: €{self.clean_df['revenue'].sum():,.2f}")
            print(f"   Mean Revenue: €{self.clean_df['revenue'].mean():,.2f}")
            print(f"   Median Revenue: €{self.clean_df['revenue'].median():,.2f}")
        
        # Estimated revenue lost
        if 'estimated_revenue_lost' in self.clean_df.columns:
            print(f"\n⚠️  Estimated Revenue Lost:")
            print(f"   Total: €{self.clean_df['estimated_revenue_lost'].sum():,.2f}")
            print(f"   Mean: €{self.clean_df['estimated_revenue_lost'].mean():,.2f}")
            print(f"   Median: €{self.clean_df['estimated_revenue_lost'].median():,.2f}")
        
        # Time range
        if 'month' in self.clean_df.columns:
            print(f"\n📅 Time Period:")
            print(f"   Start: {self.clean_df['month'].min()}")
            print(f"   End: {self.clean_df['month'].max()}")
            print(f"   Duration: {self.clean_df['month'].nunique()} months")
        
        # Dimensions
        print(f"\n📊 Dimensions:")
        for col in ['Market', 'Vertical', 'Segment']:
            if col in self.clean_df.columns:
                print(f"   {col}: {self.clean_df[col].nunique()} unique values")
        
        print(f"\n👥 Clients:")
        if 'client_id' in self.clean_df.columns:
            print(f"   Total unique clients: {self.clean_df['client_id'].nunique():,}")
        
        return self.clean_df.describe()

if __name__ == "__main__":
    # Initialize agent
    agent = DataScientistAgent('CASE_STUDY_RAW.csv')
    
    # Step 1: Load and profile
    df = agent.load_and_profile_data()
    
    # Step 2: Detect anomalies
    anomalies = agent.detect_anomalies()
    
    # Step 3: Clean data
    clean_df = agent.clean_data()
    
    # Step 4: Summary statistics
    stats = agent.generate_summary_stats()
    
    # Save clean data
    clean_df.to_csv('CASE_STUDY_CLEAN.csv', index=False)
    print(f"\n✅ Clean data saved to CASE_STUDY_CLEAN.csv")
    
    # Save quality report
    import json
    with open('data_quality_report.json', 'w') as f:
        json.dump({
            'quality_metrics': agent.quality_report,
            'anomalies': agent.anomalies
        }, f, indent=2)
    print(f"✅ Quality report saved to data_quality_report.json")
