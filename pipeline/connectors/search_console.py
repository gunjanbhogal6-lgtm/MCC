"""
Google Search Console API Connector
Authenticates and fetches data from Google Search Console
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from .base_connector import BaseConnector


class SearchConsoleConnector(BaseConnector):
    """Connector for Google Search Console API"""
    
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    API_SERVICE_NAME = 'searchconsole'
    API_VERSION = 'v1'
    
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        """
        Initialize Search Console connector.
        
        Args:
            credentials_path: Path to OAuth credentials JSON
            token_path: Path to store token JSON
        """
        super().__init__()
        self.credentials_path = credentials_path or os.getenv('GSC_CREDENTIALS_PATH', 'credentials.json')
        self.token_path = token_path or os.getenv('GSC_TOKEN_PATH', 'token.json')
        self.service = None
        
    def authenticate(self) -> bool:
        """Authenticate with Google Search Console"""
        try:
            creds = None
            
            # Load existing token if available
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if os.path.exists(self.credentials_path):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, self.SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                    else:
                        raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")
                
                # Save credentials
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
            
            # Build service
            self.service = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                credentials=creds
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Search Console authentication failed: {e}")
            return False
    
    def get_sites(self) -> List[str]:
        """Get list of all verified sites in Search Console"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            sites_response = self.service.sites().list().execute()
            sites = sites_response.get('siteEntry', [])
            
            # Extract site URLs
            site_urls = [site['siteUrl'] for site in sites]
            
            self.logger.info(f"Found {len(site_urls)} sites in Search Console")
            return site_urls
            
        except Exception as e:
            self.logger.error(f"Failed to get sites: {e}")
            return []
    
    def get_analytics_data(
        self,
        site_url: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        search_type: str = 'web',
        data_state: str = 'all',
        aggregation_type: str = 'auto'
    ) -> List[Dict]:
        """
        Fetch analytics data from Search Console.
        
        Args:
            site_url: Site URL (e.g., https://example.com)
            start_date: Start date in YYYY-MM-DD format (default: 28 days ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            dimensions: Dimensions to retrieve (e.g., ['query', 'page'])
            search_type: 'web', 'image', 'video', 'news', etc.
            data_state: 'all' or 'final'
            aggregation_type: 'auto', 'byProperty', or 'byPage'
        
        Returns:
            List of data rows
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        # Default date range: last 28 days
        if not start_date:
            start_date = (datetime.now() - timedelta(days=28)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Default dimensions
        if not dimensions:
            dimensions = ['query', 'page', 'country', 'device']
        
        try:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions,
                'searchType': search_type,
                'dataState': data_state,
                'aggregationType': aggregation_type,
                'rowLimit': 25000  # Maximum per request
            }
            
            response = self.service.searchanalytics().query(
                siteUrl=site_url,
                body=request
            ).execute()
            
            rows = response.get('rows', [])
            
            # Convert to list of dictionaries
            data = []
            for row in rows:
                data_point = {
                    'impressions': row.get('impressions', 0),
                    'clicks': row.get('clicks', 0),
                    'ctr': row.get('ctr', 0),
                    'position': row.get('position', 0),
                }
                
                # Add dimensions
                for i, dim in enumerate(dimensions):
                    if i < len(row.get('keys', [])):
                        data_point[dim] = row['keys'][i]
                
                data.append(data_point)
            
            self.logger.info(f"Retrieved {len(data)} rows from GSC for {site_url}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to fetch analytics data: {e}")
            return []
    
    def get_keyword_performance(
        self,
        site_url: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_clicks: int = 0,
        min_impressions: int = 0
    ) -> List[Dict]:
        """
        Get keyword-level performance data.
        
        Args:
            site_url: Site URL
            start_date: Start date
            end_date: End date
            min_clicks: Minimum clicks filter
            min_impressions: Minimum impressions filter
        
        Returns:
            List of keyword performance data
        """
        data = self.get_analytics_data(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['query', 'page']
        )
        
        # Apply filters
        filtered = [
            item for item in data
            if item.get('clicks', 0) >= min_clicks
            and item.get('impressions', 0) >= min_impressions
        ]
        
        # Group by keyword (keep the best-ranking page)
        keyword_data = {}
        for item in filtered:
            keyword = item.get('query', '')
            if not keyword:
                continue
            
            if keyword not in keyword_data:
                keyword_data[keyword] = item
            else:
                # Aggregate if multiple pages
                existing = keyword_data[keyword]
                existing['impressions'] += item.get('impressions', 0)
                existing['clicks'] += item.get('clicks', 0)
                # Keep the better position
                if item.get('position', 99) < existing.get('position', 99):
                    existing['position'] = item.get('position', 99)
                    existing['page'] = item.get('page', '')
                # Recalculate CTR
                if existing['impressions'] > 0:
                    existing['ctr'] = existing['clicks'] / existing['impressions']
        
        return list(keyword_data.values())
    
    def get_page_performance(
        self,
        site_url: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get page-level performance data.
        
        Args:
            site_url: Site URL
            start_date: Start date
            end_date: End date
        
        Returns:
            List of page performance data
        """
        data = self.get_analytics_data(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['page', 'query']
        )
        
        # Group by page
        page_data = {}
        for item in data:
            page = item.get('page', '')
            if not page:
                continue
            
            if page not in page_data:
                page_data[page] = {
                    'page': page,
                    'impressions': 0,
                    'clicks': 0,
                    'position': 999,
                    'ctr': 0,
                    'keywords': []
                }
            
            page_data[page]['impressions'] += item.get('impressions', 0)
            page_data[page]['clicks'] += item.get('clicks', 0)
            page_data[page]['keywords'].append(item.get('query', ''))
            
            # Track best position
            if item.get('position', 999) < page_data[page]['position']:
                page_data[page]['position'] = item.get('position', 999)
        
        # Calculate CTR and remove duplicates
        for page in page_data.values():
            if page['impressions'] > 0:
                page['ctr'] = page['clicks'] / page['impressions']
            page['keywords'] = list(set(page['keywords']))
        
        return list(page_data.values())
    
    def get_trending_keywords(
        self,
        site_url: str,
        days_back: int = 7
    ) -> List[Dict]:
        """
        Get keywords with significant performance changes.
        
        Args:
            site_url: Site URL
            days_back: Number of days to compare
        
        Returns:
            List of trending keywords
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        mid_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back * 2)).strftime('%Y-%m-%d')
        
        # Get recent data
        recent_data = self.get_keyword_performance(
            site_url=site_url,
            start_date=mid_date,
            end_date=end_date
        )
        
        # Get previous period data
        previous_data = self.get_keyword_performance(
            site_url=site_url,
            start_date=start_date,
            end_date=mid_date
        )
        
        # Map for easy lookup
        recent_by_keyword = {k['query']: k for k in recent_data}
        previous_by_keyword = {k['query']: k for k in previous_data}
        
        # Calculate trends
        trending = []
        for keyword in set(list(recent_by_keyword.keys()) + list(previous_by_keyword.keys())):
            recent = recent_by_keyword.get(keyword, {})
            previous = previous_by_keyword.get(keyword, {})
            
            if not recent or not previous:
                continue
            
            clicks_change = recent.get('clicks', 0) - previous.get('clicks', 0)
            clicks_percent = (
                (clicks_change / previous.get('clicks', 1)) * 100
                if previous.get('clicks', 0) > 0 else 0
            )
            
            position_change = previous.get('position', 99) - recent.get('position', 99)
            
            trending.append({
                'keyword': keyword,
                'clicks_change': clicks_change,
                'clicks_percent_change': clicks_percent,
                'position_change': position_change,
                'recent_position': recent.get('position', 0),
                'recent_clicks': recent.get('clicks', 0),
                'recent_impressions': recent.get('impressions', 0)
            })
        
        # Sort by percentage change (descending)
        trending.sort(key=lambda x: abs(x['clicks_percent_change']), reverse=True)
        
        return trending[:100]  # Top 100 trending
    
    def get_mobile_vs_desktop(
        self,
        site_url: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Compare mobile vs desktop performance.
        
        Args:
            site_url: Site URL
            start_date: Start date
            end_date: End date
        
        Returns:
            Dictionary with mobile and desktop metrics
        """
        data = self.get_analytics_data(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['device', 'query']
        )
        
        mobile_data = [d for d in data if d.get('device', '') == 'MOBILE']
        desktop_data = [d for d in data if d.get('device', '') == 'DESKTOP']
        
        def aggregate(device_list):
            total_impressions = sum(d.get('impressions', 0) for d in device_list)
            total_clicks = sum(d.get('clicks', 0) for d in device_list)
            avg_position = (
                sum(d.get('position', 0) for d in device_list) / len(device_list)
                if device_list else 0
            )
            
            return {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'ctr': total_clicks / total_impressions if total_impressions > 0 else 0,
                'avg_position': avg_position,
                'keyword_count': len(device_list)
            }
        
        return {
            'mobile': aggregate(mobile_data),
            'desktop': aggregate(desktop_data)
        }
    
    def export_to_csv(self, data: List[Dict], filename: str) -> bool:
        """Export data to CSV file"""
        if not data:
            return False
        
        import csv
        
        try:
            keys = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"Exported {len(data)} rows to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {e}")
            return False